import pygame
from button import Button, TextButton
from config import *


class BottomBar:
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

        self.clear_button = TextButton(self.x + self.width - 125, self.y+self.height/2-25, 100, 50, "Clear")
        self.eraser_button = TextButton(self.x + self.width - 250, self.y+self.height/2-25, 100, 50, "Erase")
        self.color_buttons = [Button(self.x+25+50*i, self.y+self.height/2-25, 50, 50, c) for i, c in enumerate(COLORS)]

    def draw(self, win):
        """
        Draws the bottom bar
        :param win: Window object
        :return: None
        """
        self.clear_button.draw(win)
        self.eraser_button.draw(win)

        for color_button in self.color_buttons:
            color_button.draw(win)

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), BORDER_THICKNESS)

    def handle_click(self, mouse):
        """
        Handle button clicks
        :return: None
        """
        if self.clear_button.click(*mouse):
            self.game.connection.send({11: []})

        if self.eraser_button.click(*mouse):
            self.game.draw_color = COLORS[0]

        for i, color_button in enumerate(self.color_buttons):
            if color_button.click(*mouse):
                self.game.draw_color = COLORS[i]
