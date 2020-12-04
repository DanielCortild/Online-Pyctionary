import pygame
from board import Board
from top_bar import TopBar
from leaderboard import Leaderboard
from bottom_bar import BottomBar
from chat import Chat
from person_is_drawing import PersonIsDrawing
from config import *


class Game:
    def __init__(self, win, connection):
        """
        :param win: Window
        :param connection: Connection object
        """
        self.win = win
        self.connection = connection

        self.is_drawing = False
        self.players = []
        self.draw_color = COLORS[1]
        self.game_ended = False
        self.drawer = "No one"

        self.top_bar = TopBar(20, 20, 1040, 80, self)
        self.leaderboard = Leaderboard(20, 120, 270, 60)
        self.board = Board(310, 120, 6)
        self.chat = Chat(810, 120, 250, 580)
        self.bottom_bar = BottomBar(20, 620, 770, 80, self)
        self.person_is_drawing = PersonIsDrawing(310, 620, 480, 80)

    def add_player(self, player):
        self.players.append(player)

    def draw(self):
        """
        Draws Game on window
        :return: None
        """
        self.win.fill(COLORS[0])

        self.top_bar.draw(self.win)
        self.leaderboard.draw(self.win)
        self.board.draw(self.win)
        self.chat.draw(self.win)
        if self.is_drawing:
            self.bottom_bar.draw(self.win)
        else:
            self.person_is_drawing.draw(self.win, self.drawer)

        pygame.display.update()

    def handle_click(self):
        """
        Handles clicks on buttons on screen
        :return: None
        """
        mouse = pygame.mouse.get_pos()

        clicked_board = self.board.click(*mouse)
        if clicked_board and self.is_drawing:
            self.connection.send({8: [*clicked_board, COLORS.index(self.draw_color)]})

        if self.is_drawing:
            self.bottom_bar.handle_click(mouse)

    def get_data(self):
        self.leaderboard.set_players(self.connection.send({-1: []}))
        self.chat.content = self.connection.send({2: []})
        self.board.compressed_board = self.connection.send({3: []})
        self.top_bar.change_round(self.connection.send({5: []}))
        self.top_bar.word = self.connection.send({6: []})
        self.top_bar.time = self.connection.send({9: []})
        self.is_drawing = self.connection.send({10: []})
        self.drawer = self.connection.send({13: []})

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            try:
                clock.tick(60)
                try:
                    self.get_data()
                    self.board.translate_board()
                except:
                    run = False

                self.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break
                    if pygame.mouse.get_pressed()[0]:
                        self.handle_click()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and len(self.chat.typing):
                            self.connection.send({0: [self.chat.typing]})
                            self.chat.update_chat()
                        else:
                            key_name = pygame.key.name(event.key).upper()
                            self.chat.type(key_name, self.is_drawing)
            except Exception as e:
                print(f"Closed because {e}")
                run = False

        pygame.quit()
