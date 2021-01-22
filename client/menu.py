#!/usr/bin/env python3


import pygame
from network import Network
from game import Game
from player import Player
from config import *


class MainMenu:
    def __init__(self):
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ""
        self.waiting = False
        self.n = None
        self.queue = (0, 0)
        pygame.font.init()
        self.name_font = pygame.font.SysFont("comicsans", 80)
        self.title_font = pygame.font.SysFont("comicsans", 120)
        self.enter_font = pygame.font.SysFont("comicsans", 60)
        self.no_connection = False

    def draw(self):
        self.win.fill(COLORS[0])

        title = self.title_font.render("Pyctionary!", True, (0, 0, 0))
        self.win.blit(title, (self.WIDTH/2-title.get_width()/2, 100))

        type = self.name_font.render(f"Type your name:", True, (0, 0, 0))
        self.win.blit(type, (self.WIDTH/2-type.get_width()/2, 250))

        name = self.name_font.render(f"{self.name}", True, (0, 0, 0))
        self.win.blit(name, (self.WIDTH / 2 - name.get_width() / 2, 350))

        if self.waiting:
            message = self.enter_font.render(f"In queue... ({self.queue[0]}/{self.queue[1]})", True, (0, 0, 0))
        elif self.no_connection:
            message = self.enter_font.render(f"No Connection, Trying to reconnect", True, (0, 0, 0))
        else:
            message = self.enter_font.render("Press enter to join a room", True, (0, 0, 0))
        self.win.blit(message, (self.WIDTH / 2 - message.get_width() / 2, 600))

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            self.draw()
            if self.waiting:
                try:
                    response = self.n.send({-2: []})
                    self.queue = (response[1], response[2])
                    if response[0]:
                        pygame.font.init()
                        g = Game(self.win, self.n)
                        for player in response:
                            g.players.append(Player(player))
                        g.run()
                except:
                    pass

            for event in pygame.event.get():
                if not self.waiting:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(self.name) > 0:
                                self.waiting = True
                                self.n = Network(self.name)
                        else:
                            key_name = pygame.key.name(event.key)
                            self.type(key_name)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

    def type(self, char):
        if char.upper() == "BACKSPACE" and len(self.name):
            self.name = self.name[:-1]
        elif char.upper() == "SPACE":
            self.name += " "
        elif len(char) == 1 and len(self.name) <= 20:
            self.name += char


if __name__ == "__main__":
    MainMenu().run()
