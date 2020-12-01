from board import Board
from round import Round

import random


class Game(object):
    def __init__(self, id, players):
        """
        init the game once enough players are connected
        :param id: int
        :param players: Player[]
        """
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_counter = 0
        self.start_new_round()

    def start_new_round(self):
        """
        start new round with new word
        :return: None
        """
        try:
            round_word = self.get_word()
            self.round = Round(round_word, self.players[self.player_draw_ind], self)
            self.round_counter += 1

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1
        except Exception as e:
            self.end_game()

    def player_guess(self, player, guess):
        """
        makes the player guess the word
        :param player: Player
        :param guess: str
        :return: bool
        """
        return self.round.guess(player, guess)

    def player_disconnected(self, player):
        """
        clean up objects when player leaves
        :param player: Player
        :raises: Exception()
        """
        # STILL TO bE CHECKED
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
        else:
            raise Exception("Player not in game")

        if len(self.players) <= 2:
            self.end_game()

    def get_player_scores(self):
        """
        Returns a dict of player scores
        :return: dict
        """
        scores = {player.get_name(): player.get_score() for player in self.players}
        return scores

    def skip(self):
        """
        Adds a skip, if enough, end round
        :return: None
        """
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
                return True
            return False
        else:
            raise Exception("No round started yet")

    def round_ended(self):
        """
        If rounds ends call this
        :return: None
        """
        self.start_new_round()
        self.board.clear()

    def update_board(self, x, y, color):
        """
        Calls update method on board
        :param x: int
        :param y: int
        :param color: 0-8
        :return: None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x,y,color)

    def end_game(self):
        """

        :return:
        """
        print(f"[GAME] Game {self.id} ended")
        # for player in self.players:
        #     self.round.player_left(player)
        for player in self.players:
            player.game = None

    def get_word(self):
        """
        gives a word that has not yet been used
        :return: str
        """
        with open("words.txt", "r") as f:
            words = []
            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)
            r = random.randint(0, len(words)-1)
            wrd = words[r]
            self.words_used.add(wrd)
            return wrd
