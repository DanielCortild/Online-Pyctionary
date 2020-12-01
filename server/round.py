import time as t
from _thread import *
from chat import Chat

class Round(object):
    def __init__(self, word, player_drawing, players, game):
        """
        init object
        :param word: str
        :param player_drawing: Player
        :param players: Player[]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.player_scores = {player:0 for player in players}
        self.time = 75
        self.game = game
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self):
        """
        Returns bool deciding whether skipping round or not
        :return: bool
        """
        self.skips += 1
        if self.skips > len(self.players) - 2:
            return True
        return False

    def get_scores(self):
        """
        Returns all the player scores
        :return:
        """
        return self.scores

    def get_score(self, player):
        """
        Get a specific players score
        :param player: Player
        :return: int
        """
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        """
        Runs in different thread to keep track of time
        :return: None
        """
        while self.time > 0:
            t.sleep(1000)
            self.time -= 1
        self.end_round("Time is up")

    def guess(self, player, wrd):
        """
        :returns whether the player guessed right
        :param player: Player
        :param wrd: str
        :return: bool
        """
        correct = wrd == self.word
        if correct:
            self.player_guessed.append(player)

            # IMPLEMENT SCORING SYSTEM

    def player_left(self, player):
        """
        removes player that left from scores and list
        :param player: Player
        :return: None
        """
        # Not sure if works...
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.end_round("Drawing player left")

    def end_round(self, msg):
        for player in self.players:
            player.update_score(self.player_scores[player])
        self.game.round_ended()

