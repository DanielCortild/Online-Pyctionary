import pygame
from config import *


class Board:
    def __init__(self, x, y, cell_size):
        """
        :param x: int
        :param y: int
        :param cell_size: int
        """
        self.x = x
        self.y = y
        self.cell_size = cell_size

        self.height = ROWS * self.cell_size
        self.width = COLS * self.cell_size

        self.compressed_board = []
        self.board = [[COLORS[0] for _ in range(COLS)] for _ in range(ROWS)]

    def translate_board(self):
        """
        Decode the compressed board
        :return: None
        """
        for y in range(len(self.compressed_board)):
            for x, color in enumerate(self.compressed_board[y]):
                self.board[y][x] = COLORS[color]

    def draw(self, win):
        """
        Draws the board onto win
        :param win: Window object
        :return: None
        """
        for y in range(len(self.board)):
            for x, color in enumerate(self.board[y]):
                pygame.draw.rect(win, color, (self.x+x*self.cell_size, self.y+y*self.cell_size,
                                              self.cell_size, self.cell_size), 0)

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), BORDER_THICKNESS)

    def click(self, x, y):
        """
        Returns pixel which is clicked
        :param x: float
        :param y: float
        :return: (int, int) or None
        """
        row = int((x - self.x)/self.cell_size)
        col = int((y - self.y)/self.cell_size)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return row, col
        return None
