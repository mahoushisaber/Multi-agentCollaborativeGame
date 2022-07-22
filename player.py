import pygame
import numpy as np

class PlayerObj(pygame.sprite.Sprite):
    def __init__(self, size, posX, posY, speed, control_auto):
        super().__init__()
        self.size = size
        self.posX = posX
        self.posY = posY  
        self.speed = speed  
        self.control_auto = control_auto
        
