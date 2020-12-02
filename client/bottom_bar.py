import pygame
from button import Button, TextButton


class BottomBar:
    BORDER_THICKNESS = 5

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 900
        self.height = 100
        self.game = game
        self.clear_button = TextButton(self.x + self.width - 10, self.y+25, 100, 50, (128, 128, 128), "Clear")
        self.eraser_button = TextButton(self.x + self.width - 300, self.y+25, 100, 50, (128, 128, 128), "Erase")

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), self.BORDER_THICKNESS)
        self.clear_button.draw(win)
        self.eraser_button.draw(win)

    def button_events(self, mouse):
        """
        Handle all button events
        :return: None
        """
        if self.clear_button.click(*mouse):
            print("Pressed clear button")

        if self.eraser_button.click(*mouse):
            print("Pressed erase button")
