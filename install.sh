#!/bin/bash
set -e

BEATBUGGING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== BeatBugging Installer ==="
echo ""

# Check Python version
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found. Install Python 3.10 or higher."
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    echo "Error: Python 3.10+ required (found $PY_VERSION)."
    exit 1
fi

echo "Python $PY_VERSION detected."

# Create venv if it doesn't exist
if [ ! -d "$BEATBUGGING_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$BEATBUGGING_DIR/venv"
fi

# Install dependencies
echo "Installing dependencies..."
"$BEATBUGGING_DIR/venv/bin/pip" install -r "$BEATBUGGING_DIR/requirements.txt" -q
echo "Dependencies installed."

# Create wrapper script
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/beatbugging" << EOF
#!/bin/bash
exec "$BEATBUGGING_DIR/venv/bin/python" "$BEATBUGGING_DIR/main.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/beatbugging"
echo "Created ~/.local/bin/beatbugging"

# Add ~/.local/bin to PATH in shell config if missing
ADDED_TO=()
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc" ] && ! grep -q '\.local/bin' "$rc"; then
        echo '' >> "$rc"
        echo '# Added by BeatBugging installer' >> "$rc"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
        ADDED_TO+=("$rc")
    fi
done

echo ""
echo "Done! BeatBugging is installed."

if [ ${#ADDED_TO[@]} -gt 0 ]; then
    echo ""
    echo "~/.local/bin was added to PATH in: ${ADDED_TO[*]}"
    echo "Restart your terminal or run:"
    for rc in "${ADDED_TO[@]}"; do
        echo "  source $rc"
    done
fi

echo ""
echo "Run from anywhere with:"
echo "  beatbugging"
