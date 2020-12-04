import pygame
from config import *


class PersonIsDrawing:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("comicsans", 30)

    def draw(self, win, drawer):
        text = self.font.render(f"{drawer} is drawing", True, (0, 0, 0))
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))
