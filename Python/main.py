import pygame
import time
import sys
from SpokenText import SpokenText as sp

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)


class WhiteLine:
    def __init__(self, area, font, fg_color, bk_color):
        """object to display lines of text scrolled in with a delay between each line
        in font and fg_color with background o fk_color with in the area rect"""

        super().__init__()
        self.rect = area.copy()
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.size = area.size
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.surface.fill(bk_color)
        self.font = font
        self.y = 0
        self.y_delta = self.font.size("M")[1]
        self.dirty = False

    def _update_line(self, line):  # render next line if it's time
        # line does not fit in remaining space
        if self.y + self.y_delta > self.size[1]:
            self.surface.blit(self.surface, (0, -self.y_delta))  # scroll up
            self.y += -self.y_delta  # backup a line
            pygame.draw.rect(self.surface, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))

        text = self.font.render(line, True, self.fg_color)
        # pygame.draw.rect(text, GREY, text.get_rect(), 1)  # for demo show render area
        self.surface.blit(text, (0, self.y))

        self.y += self.y_delta

    # call update from pygame main loop
    def update(self, line):
        self._update_line(line)
        self.dirty = True
        # self.update()

    def draw(self, screen):
        if self.dirty:
            screen.blit(self.surface, self.rect)
            self.dirty = False


def break_line(text):
    tamanho = len(text)
    linhas = []
    if len(text) > 56:
        nLinhas = tamanho // 56 + 1
        nResto = tamanho % 56
        linhas = []
        ultimo = 56
        for i in range(nLinhas):
            if len(text[56:]) > i * 56:
                if text[(i+1)*56-1] == ' ':
                    linhas.append(text[i*56:(i+1)*56])
                else:

                    for y in range(56):
                        if text[(i+1)*56-y] == ' ':
                            ultimo = (i+1)*56-y
                            linhas.append(text[i*56:(i+1)*56-y])
                            break
            else:
                linhas.append(text[ultimo+1:])

    else:
        linhas.append(text)

    return linhas


transcribe = []

# start up pygame
pygame.init()
# print(sorted(pygame.font.get_fonts()))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
x, y = screen.get_size()

font = pygame.font.SysFont("Liberation Sans", 65)

white = WhiteLine(pygame.Rect(0, 0, x, y), font, YELLOW, BLACK)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        else:
            # screen.fill(pygame.color.Color('black'))
            result = sp()
            if (result != False):
                transcribe = break_line(result)
            else:
                transcribe = ['...']

            for y in range(len(transcribe)):
                white.update(transcribe[y])
                white.draw(screen)
            pygame.display.flip()
            clock.tick(60)
