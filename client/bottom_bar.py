import pygame
from button import Button, TextButton


class BottomBar:
    BORDER_THICKNESS = 5
    COLORS = {
        0: (255, 255, 255),
        1: (0, 0, 0),
        2: (128, 128, 128),
        3: (255, 0, 0),
        4: (255, 128, 0),
        5: (255, 255, 0),
        6: (0, 255, 0),
        7: (0, 255, 255),
        8: (0, 0, 255)
    }

    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 900
        self.height = 100
        self.game = game
        self.clear_button = TextButton(self.x + self.width - 10, self.y+25, 100, 50, (128, 128, 128), "Clear")
        self.eraser_button = TextButton(self.x + self.width - 300, self.y+25, 100, 50, (128, 128, 128), "Erase")
        self.color_buttons = [
            Button(self.x+10, self.y, 50, 50, (255, 255, 255)),
            Button(self.x + 60, self.y, 50, 50, (0, 0, 0)),
            Button(self.x + 110, self.y, 50, 50, (128, 128, 128)),
            Button(self.x + 160, self.y, 50, 50, (255, 0, 0)),
            Button(self.x + 210, self.y, 50, 50, (255, 128, 0)),
            Button(self.x + 260, self.y, 50, 50, (255, 255, 0)),
            Button(self.x + 310, self.y, 50, 50, (0, 255, 0)),
            Button(self.x + 360, self.y, 50, 50, (0, 255, 128)),
            Button(self.x + 410, self.y, 50, 50, (0, 255, 255)),
        ]

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), self.BORDER_THICKNESS)
        self.clear_button.draw(win)
        self.eraser_button.draw(win)

        for color_button in self.color_buttons:
            color_button.draw(win)

    def button_events(self, mouse):
        """
        Handle all button events
        :return: None
        """
        if self.clear_button.click(*mouse):
            print("Pressed clear button")
            self.game.board.clear()

        if self.eraser_button.click(*mouse):
            print("Pressed erase button")
            self.game.draw_color = (255, 255, 255)

        for i, color_button in enumerate(self.color_buttons):
            if color_button.click(*mouse):
                self.game.draw_color = self.COLORS[i]
