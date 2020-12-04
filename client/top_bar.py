import pygame
from config import *


class TopBar:
    def __init__(self, x, y, width, height, game):
        """
        :param x: int
        :param y: int
        :param width: int
        :param height: int
        :param game: Game object
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game

        self.word = ""
        self.round = 1
        self.font = pygame.font.SysFont("comicsans", 50)
        self.time = 0

    def draw(self, win):
        text = self.font.render(f"Round {self.round} of {len(self.game.players)}", True, (0, 0, 0))
        win.blit(text, (self.x+self.height/2-text.get_height()/2, self.y+self.height/2-text.get_height()/2))

        text = self.font.render(self.underscore_text(self.word, self.game.is_drawing), True, (0, 0, 0))
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))

        pygame.draw.circle(win, (0, 0, 0), (self.x+self.width-50, self.y+self.height/2), 30, BORDER_THICKNESS)
        time = self.font.render(str(self.time), True, (0, 0, 0))
        win.blit(time, (self.x+self.width-50-time.get_width()/2, self.y+self.height/2-time.get_height()/2))

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), BORDER_THICKNESS)

    def change_word(self, word):
        self.word = word

    def change_round(self, rnd):
        self.round = rnd

    @staticmethod
    def underscore_text(text, is_drawing):
        new_str = ""
        for char in text:
            if char == "-":
                new_str += "-"
            elif char != " ":
                if is_drawing:
                    new_str += char
                else:
                    new_str += "_"
            else:
                new_str += "  "
            new_str += " "
        return new_str
