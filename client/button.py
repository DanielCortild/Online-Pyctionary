import pygame


class Button:
    def __init__(self, x, y, width, height, color=(128, 128, 128)):
        """
        :param x: int
        :param y: int
        :param width: int
        :param height: int
        :param color: (int, int, int)
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color

        self.BORDER_WIDTH = 2

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(win, self.color,
                         (self.x + self.BORDER_WIDTH, self.y + self.BORDER_WIDTH,
                          self.width - self.BORDER_WIDTH * 2,self.height - self.BORDER_WIDTH * 2), 0)

    def click(self, x, y):
        """
        If user clicked button
        :param x: float
        :param y: float
        :return: bool
        """
        if self.x <= x <= self.x+self.width and self.y <= y <= self.y+self.height:
            return True
        return False


class TextButton(Button):
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height)
        self.text = text
        self.text_font = pygame.font.SysFont("comicsans", 30)

    def change_font_size(self, size):
        self.text_font = pygame.font.SysFont("comicsans", size)

    def draw(self, win):
        super().draw(win)
        text = self.text_font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))

