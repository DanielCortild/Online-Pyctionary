import pygame
from random import *


class Board:
    ROWS = COLS = 80
    CELL_SIZE = 6
    HEIGHT = ROWS * CELL_SIZE
    WIDTH = COLS * CELL_SIZE
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

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.compressed_board = []
        self.board = self.create_board()

    def create_board(self):
        return [[(255, 255, 255) for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def translate_board(self):
        for y, _ in enumerate(self.compressed_board):
            for x, c in enumerate(self.compressed_board[y]):
                self.board[y][x] = self.COLORS[c]

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x-self.BORDER_THICKNESS/2, self.y-self.BORDER_THICKNESS/2, self.WIDTH+self.BORDER_THICKNESS, self.HEIGHT+self.BORDER_THICKNESS), self.BORDER_THICKNESS)
        for y, _ in enumerate(self.board):
            for x, c in enumerate(self.board[y]):
                pygame.draw.rect(win, c, (self.x+x*self.CELL_SIZE, self.y+y*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)

    def click(self, x, y):
        """
        Returns pixel which is clicked
        :param x: float
        :param y: float
        :return: (int, int) or None
        """
        row = int((x - self.x)/self.CELL_SIZE)
        col = int((y - self.y)/self.CELL_SIZE)
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return row, col
        return None

    def update(self, x, y, color, thickness=1):
        for i in range(max(0, y-thickness), min(y+thickness, self.COLS+1)):
            for j in range(max(0, x-thickness), min(x+thickness, self.ROWS+1)):
                self.board[i][j] = color

    def clear(self):
        self.board = self.create_board()
