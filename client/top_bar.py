import pygame


class TopBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word = ""
        self.round = 1
        self.max_round = 8
        self.round_font = pygame.font.SysFont("comicsans", 50)
        self.BORDER_THICKNESS = 5

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), self.BORDER_THICKNESS)

        text = self.round_font.render(f"Round {self.round} of {self.max_round}", 1, (0, 0, 0))
        win.blit(text, (self.x+10, self.y+self.height/2-text.get_height()/2))

        text = self.round_font.render(self.underscore_text(self.word), 1, (0, 0, 0))
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2+10))

    def change_word(self, word):
        self.word = word

    def change_round(self, round):
        self.round = round

    @staticmethod
    def underscore_text(text):
        new_str = ""
        for char in text:
            if char != " ":
                new_str += "_"
            else:
                new_str = " "

        return new_str