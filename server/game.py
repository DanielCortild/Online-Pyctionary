from board import Board
from round import Round
import random


class Game:
    def __init__(self, players):
        """
        init the game once enough players are connected
        :param players: Player[]
        """
        self.players = players
        self.words_used = set()
        self.board = Board()
        self.player_draw_ind = 0
        self.round_counter = 0
        self.round = None
        self.start_new_round()

    def start_new_round(self):
        """
        start new round with new word
        :return: None
        """
        try:
            if self.round_counter >= 3*len(self.players):
                self.end_game()
            elif self.player_draw_ind == -1:
                self.end_game()
            else:
                self.round = Round(self.get_word(), self.players[self.player_draw_ind], self)
                self.round_counter += 1
                self.player_draw_ind += 1
                if self.player_draw_ind >= len(self.players):
                    self.player_draw_ind -= len(self.players)
        except Exception as e:
            print(f"[EXCEPTION] Game ended because of {e}")
            self.end_game()

    def player_guess(self, player, guess):
        """
        makes the player guess the word
        :param player: Player
        :param guess: str
        :return: bool
        """
        return self.round.guess(player, guess)

    # def player_disconnected(self, player):
    #     """
    #     clean up objects when player leaves
    #     :param player: Player
    #     :raises: Exception()
    #     """
    #     if player in self.players:
    #         player_ind = self.players.index(player)
    #         if player_ind >= self.player_draw_ind:
    #             self.player_draw_ind -= 1
    #         self.players.remove(player)
    #         self.round.player_left(player)
    #     else:
    #         raise Exception("Player not in game")
    #
    #     self.round.chat.update_chat(f"Player {player.name} disconnected!")
    #
    #     if len(self.players) == 0:
    #         self.end_game()

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
            self.round.chat.update_chat(f"Player has voted to skip ({self.round.skips}/{len(self.players)-2})")
            if new_round:
                self.round.chat.update_chat("Round has been skipped.")
                self.end_round()
                return True
            return False
        else:
            raise Exception("No round started yet")

    def end_round(self):
        """
        If rounds ends call this
        :return: None
        """
        self.round.chat.update_chat(f"Round {self.round_counter} has ended")
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
        self.board.update(x, y, color)

    def end_game(self):
        """
        :return:
        """
        print(f"[GAME] Game ended")

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
