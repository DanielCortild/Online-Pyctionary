import pygame


class Leaderboard:
    WIDTH = 300
    HEIGHT_ENTRY = 68
    BORDER_THICKNESS = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.players = []
        self.name_font = pygame.font.SysFont("comicsans", 30)
        self.score_font = pygame.font.SysFont("comicsans", 20)
        self.rank_font = pygame.font.SysFont("comicsans", 50)

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT_ENTRY*len(self.players)), self.BORDER_THICKNESS)
        scores = [(player.name, player.score) for player in self.players]
        scores.sort(key=lambda x: x[1], reverse=True)

        for i, score in enumerate(scores):
            if i%2 == 0:
                color = (255, 255, 255)
            else:
                color = (240, 240, 240)
            pygame.draw.rect(win, color, (self.x, self.y+i*self.HEIGHT_ENTRY, self.WIDTH, self.HEIGHT_ENTRY))

            # Draw text
            rank = self.rank_font.render(f"#{i+1}", 1, (0, 0, 0))
            win.blit(rank, (self.x+10, self.y+i*self.HEIGHT_ENTRY+self.HEIGHT_ENTRY/2-rank.get_height()/2))

            name = self.name_font.render(score[0], 1, (0, 0, 0))
            win.blit(name, (self.x - name.get_width() / 2 + self.WIDTH / 2, self.y + i * self.HEIGHT_ENTRY + self.HEIGHT_ENTRY/2-name.get_height()/2))

            score = self.score_font.render(str(score[1]), 1, (0, 0, 0))
            win.blit(score, (self.x + self.WIDTH - score.get_width() - 30, self.y + i * self.HEIGHT_ENTRY + self.HEIGHT_ENTRY/2-score.get_height()/2))


    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)
