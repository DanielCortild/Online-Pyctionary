class Board(object):
    ROWS = COLS = 80

    def __init__(self):
        """
        Init the board
        """
        self.data = self._create_empty_board()

    def update(self, x, y, color):
        """
        Updates a single pixel
        :param x: int
        :param y: int
        :param color: 0-8
        :return: None
        """
        self.data[y][x] = color

    def clear(self):
        """
        Clear board to all white
        :return: None
        """
        self.data = self._create_empty_board()

    def fill(self, x, y):
        """
        Fills in specific shape or area using recursion
        :param x: int
        :param y: int
        :return: None
        """
        pass

    def get_board(self):
        """
        Gets data of the board
        :return: (int, int, int)[]
        """
        return self.data

    def _create_empty_board(self):
        """
        Creates an all white board (Empty)
        :return:
        """
        return [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]


