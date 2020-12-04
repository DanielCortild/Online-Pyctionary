import pygame
from config import *


class Chat:
    def __init__(self, x, y, width, height):
        """
        :param x: int
        :param y: int
        :param width: int
        :param height: int
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.content = []
        self.typing = ""
        self.font = pygame.font.SysFont("comicsans", 24)

    def update_chat(self):
        """
        Update the chat
        :return: None
        """
        self.content.append(self.typing)
        self.typing = ""

    def draw(self, win):
        """
        Draws chat on screen
        :param win: Window
        :return: None
        """
        while len(self.content) * CHAT_GAP > self.height - 100:
            self.content = self.content[:-1]

        for i, chat in enumerate(self.content):
            color = (0, 255, 0) if chat[0] == "g" else (255, 0, 0)
            txt = self.font.render(chat[1:], True, color)
            win.blit(txt, (self.x+10, self.y+(i+1)*CHAT_GAP))

        pygame.draw.rect(win, (220, 220, 220), (self.x, self.y + self.height - 40, self.width, 40))

        type_chat = self.font.render(self.typing, True, (0, 0, 0))
        win.blit(type_chat, (self.x+10, self.y+self.height-type_chat.get_height()/2-20))

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), BORDER_THICKNESS)

    def type(self, char, is_drawing):
        """
        Allows user to type into chat
        :param char: key_name
        :return: None
        """
        if not is_drawing:
            if char == "BACKSPACE":
                if len(self.typing) > 0:
                    self.typing = self.typing[:-1]
            elif char == "SPACE":
                self.typing += " "
            elif len(char) == 1 and len(self.typing) <= 12:
                self.typing += char
        else:
            self.typing = ""
