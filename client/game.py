import pygame
from button import Button, TextButton
from board import Board
from top_bar import TopBar
from leaderboard import Leaderboard
from player import Player
from bottom_bar import BottomBar
from chat import Chat
from network import Network


class Game:
    BG = (255, 255, 255)

    def __init__(self, win, connection=None):
        self.connection = connection
        self.win = win
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.leaderboard = Leaderboard(20, 120)
        self.skip_button = TextButton(150, 700, 100, 50, (255, 128, 0), "Skip")
        self.board = Board(350, 120)
        self.bottom_bar = BottomBar(10, 700, self)
        self.chat = Chat(1000, 110)
        self.top_bar.change_round(1)
        self.players = []
        for player in self.players:
            self.leaderboard.add_player(player)

        self.draw_color = (0, 0, 0)

    def add_player(self, player):
        self.players.append(player)
        self.leaderboard.add_player(player)

    def draw(self):
        self.win.fill(self.BG)

        self.top_bar.draw(self.win)
        self.leaderboard.draw(self.win)
        self.skip_button.draw(self.win)
        self.board.draw(self.win)
        self.bottom_bar.draw(self.win)
        self.chat.draw(self.win)

        pygame.display.update()

    def check_clicks(self):
        """
        Handles clicks on buttons on screen
        :return: None
        """
        mouse = pygame.mouse.get_pos()
        if self.skip_button.click(*mouse):
            print("Clicked skip button")

        clicked_board = self.board.click(*mouse)
        if clicked_board:
            self.board.update(*clicked_board, self.draw_color)

        clicked_buttons = self.bottom_bar.button_events(mouse)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            response = self.connection.send({3: []})
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.chat.update_chat()
                        self.connection.send({0: [self.chat.typing]})
                        self.chat.typing = ""
                    else:
                        key_name = pygame.key.name(event.key).upper()
                        self.chat.type(key_name)



        pygame.quit()