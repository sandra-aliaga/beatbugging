import time
import os
import pygame as pg
import numpy as np
import json as js

class LogMusicGenerator:
    
    def __init__(self, log_path="none"):
        self.log_path = log_path
        self.fileState = False
        self.musicState = False
        self.default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs", "default.log")
        self.scale = ""
        self.freq = ""
        self.rate = ""
        self.coords = {}
        
        if self.log_path != "none":
            if os.path.isfile(self.log_path):
                self.fileState = True
                
                with open(self.log_path, "r") as f:
                    self.log_data = f.read()
            else:
                self.log_data = ""
        else:
            self.log_data = ""
    
    def useDefaultLog(self):
        self.log_path = self.default_path
        self.fileState = True
        
        if os.path.isfile(self.log_path):
            with open(self.log_path, "r") as f:
                self.log_data = f.read()
        else:
            self.log_data = ""
            
    def __generate_scale_notes(self):
        
        return []
    
    def __sin_wave(self):
        return []
    def __square_wave(self):
        return []
    def __saw_wave(self):
        return []
    def __triangle_wave(self):
        return []
    
    def generate_music(self, scale="minor", freq=440, rate=44100):
        self.scale = scale
        self.freq = freq
        self.rate = rate
        
        if not self.fileState:
            self.useDefaultLog()
        
        notes = self.__generate_scale_notes()
    
        return notes