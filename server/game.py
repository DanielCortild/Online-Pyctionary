from .player import Player
from .board import Board
from .round import Round

class Game(object):
    def __init__(self, id, players, thread):
        """
        init the game once enough players are connected
        :param id: int
        :param players: Player[]
        """
        self.id = id
        self.players = players
        self.words_used = []
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.connected_thread = thread

        self.start_new_round()

    def start_new_round(self):
        """
        start new round with new word
        :return: None
        """
        self.round = Round(self.get_word(), self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind += 1
        if self.player_draw_ind >= len(self.players):
            self.round_ended()
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
        pass

    def skip(self):
        """
        Adds a skip, if enough, end round
        :return: None
        """
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()

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
        :param color: (int, int, int)
        :return: None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x,y,color)

    def end_game(self):
        """

        :return:
        """
        # Still to implement
        pass

    def get_word(self):
        """
        gives a word that has not yet been used
        :return: str
        """
        # GET WORD
        pass