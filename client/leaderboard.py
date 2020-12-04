import pygame
from config import *


class Leaderboard:

    def __init__(self, x, y, width, entry_height):
        """
        :param x: int
        :param y: int
        :param width: int
        :param entry_height: int
        """
        self.x = x
        self.y = y
        self.width = width
        self.entry_height = entry_height

        self.players = []
        self.name_font = pygame.font.SysFont("comicsans", 30)
        self.score_font = pygame.font.SysFont("comicsans", 20)
        self.rank_font = pygame.font.SysFont("comicsans", 50)

    def draw(self, win):
        scores = [(player, self.players[player]) for player in self.players]
        scores.sort(key=lambda x: x[1], reverse=True)

        for i, score in enumerate(scores):
            color = (255, 255, 255) if i % 2 == 0 else (240, 240, 240)
            pygame.draw.rect(win, color, (self.x, self.y+i*self.entry_height, self.width, self.entry_height))

            rank = self.rank_font.render(f"#{i+1}", True, (0, 0, 0))
            win.blit( rank, ( self.x + self.entry_height / 2 - rank.get_height() / 2,
                              self.y + i * self.entry_height + self.entry_height / 2 - rank.get_height() / 2 ) )

            name = self.name_font.render(score[0], True, (0, 0, 0))
            win.blit(name, (self.x + 70,
                            self.y + i * self.entry_height + self.entry_height/2-name.get_height()/2))

            score = self.score_font.render(str(score[1]), True, (0, 0, 0))
            win.blit(score, (self.x + self.width - score.get_width() - 30,
                             self.y + i * self.entry_height + self.entry_height/2-score.get_height()/2))

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width,
                                          self.entry_height*len(self.players)), BORDER_THICKNESS)

    def set_players(self, players):
        self.players = players
