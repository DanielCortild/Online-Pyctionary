import pygame
from network import Network
from game import Game
from player import Player


class MainMenu:
    BG = (255, 255, 255)

    def __init__(self):
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ""
        self.waiting = False
        pygame.font.init()
        self.name_font = pygame.font.SysFont("comicsans", 80)
        self.title_font = pygame.font.SysFont("comicsans", 120)
        self.enter_font = pygame.font.SysFont("comicsans", 60)

    def draw(self):
        self.win.fill(self.BG)

        title = self.title_font.render("Pictionary!", 1, (0, 0, 0))
        self.win.blit(title, (self.WIDTH/2-title.get_width()/2, 50))

        name = self.name_font.render(f"Type your name: {self.name}", 1, (0, 0, 0))
        self.win.blit(name, (self.WIDTH/2-title.get_width()/2, 200))

        if self.waiting:
            name = self.enter_font.render("In queue...", 1, (0, 0, 0))
            self.win.blit(name, (self.WIDTH / 2 - title.get_width() / 2, 800))
        else:
            name = self.enter_font.render("Press enter to join a room", 1, (0, 0, 0))
            self.win.blit(name, (self.WIDTH / 2 - title.get_width() / 2, 800))

        clock = pygame.time.Clock()

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            self.draw()
            if self.waiting:
                response = self.n.send({-1: []})
                if response:
                    pygame.font.init()
                    g = Game(self.win, self.n)
                    for player in response:
                        g.add_player(Player(player))
                    g.run()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.name) > 0:
                            self.waiting = True
                            self.n = Network(self.name)
                            break
                    else:
                        key_name = pygame.key.name(event.key)
                        self.type(key_name)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

    def type(self, char):
        if char.upper() == "BACKSPACE" and len(self.name):
            self.name = self.name[:-1]
        elif char.upper() == "SPACE":
            self.name += " "
        elif len(char) == 1 and len(self.name) <= 20:
            self.name += char

if __name__ == "__main__":
    main = MainMenu()
    main.run()