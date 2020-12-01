class Player(object):
    def __init__(self, ip, name):
        """
        Init player object
        :param ip: str
        :param name: str
        """
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game):
        """
        Sets the players game to the one it is in
        :param game: Game
        :return: None
        """
        self.game = game

    def update_score(self, x):
        """
        Updates a players score
        :param x: int
        :return: None
        """
        self.score += x

    def guess(self, wrd):
        """
        Makes a player guess
        :param wrd: str
        :return: bool
        """
        return self.game.player_guess(self, wrd)

    def disconnect(self):
        """
        Call to disconnect player
        :return:
        """
        self.game.player_disconnected(self, wrd)

    def get_ip(self):
        """
        Gets player ip
        :return: str
        """
        return self.ip

    def get_name(self):
        """
        Gets player name
        :return: str
        """
        return self.name

    def get_score(self):
        """
        Gets player score
        :return: int
        """
        return self.score
