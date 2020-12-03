import pygame


class Chat:
    WIDTH = 300
    HEIGHT = 700
    BORDER_THICKNESS = 5
    CHAT_GAP = 30
    TYPING_LIMIT = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content = []
        self.typing = ""
        self.chat_font = pygame.font.SysFont("comicsans", 24)

    def update_chat(self):
        self.content.append(self.typing)
        self.typing = ""

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT), self.BORDER_THICKNESS)

        chat = self.content

        while len(chat) * self.CHAT_GAP > self.HEIGHT - 100:
            chat = chat[:-1]

        for i, chat in enumerate(chat):
            txt = self.chat_font.render(chat, 1, (0, 0, 0))

            win.blit(txt, (self.x+10, self.y+(i+1)*self.CHAT_GAP))

        pygame.draw.rect(win, (220, 220, 220), (self.x, self.y + self.HEIGHT - 100, self.WIDTH, 100))

        type_chat = self.chat_font.render(self.typing, 1, (0, 0, 0))
        win.blit(type_chat, (self.x+5, self.y+50-type_chat.get_height()/2))

    def type(self, char):
        if char == "BACKSPACE":
            if len(self.typing) > 0:
                self.typing = self.typing[:-1]
        elif char == "SPACE":
            self.typing += " "
        elif len(char) == 1 and len(self.typing) <= self.TYPING_LIMIT:
            self.typing += char