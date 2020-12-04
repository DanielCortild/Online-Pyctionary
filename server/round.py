import time as t
from _thread import *
from chat import Chat


class Round(object):
    def __init__(self, word, player_drawing, game):
        """
        init object
        :param word: str
        :param player_drawing: Player
        :param game: Game object
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.time = 20
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.chat = Chat()
        start_new_thread(self.time_thread, ())

    def skip(self):
        """
        Returns bool deciding whether skipping round or not
        :return: bool
        """
        self.skips += 1
        if self.skips > len(self.game.players) - 2:
            return True
        return False

    def time_thread(self):
        """
        Runs in different thread to keep track of time
        :return: None
        """
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round()

    def guess(self, player, wrd):
        """
        :returns whether the player guessed right
        :param player: Player
        :param wrd: str
        :return: bool
        """
        if wrd.lower() == self.word.lower():
            self.player_guessed.append(player)
            self.chat.update_chat(f"g{player.name} guessed correctly")
            return True
        self.chat.update_chat(f"r{player.name}: {wrd}")
        return False

    def end_round(self):
        for player in self.game.players:
            player.has_guessed = False
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.end_round()

