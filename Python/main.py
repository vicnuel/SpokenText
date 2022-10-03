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
    if len(text) > 50:
        nLinhas = tamanho // 50 + 1
        nResto = tamanho % 50
        linhas = []
        ultimo = 0
        for i in range(nLinhas):
            if len(text[50:]) > i * 50:
                if text[ultimo+50] == ' ':
                    linhas.append(text[ultimo:ultimo+50])
                    ultimo = ultimo+50+1
                    # print(linhas)
                else:
                    for y in range(50):
                        if text[ultimo+50-y] == ' ':
                            linhas.append(text[ultimo:ultimo+50-y])
                            # print(linhas)
                            ultimo = ultimo+50-y+1
                            # print(ultimo)
                            break
            else:
                if len(text[ultimo:]) > 50:
                    if text[ultimo+50] == ' ':
                        linhas.append(text[ultimo:ultimo+50])
                        ultimo = ultimo+50+1
                        # print(linhas)
                        linhas.append(text[ultimo:])
                        # print(linhas)
                    else:
                        for y in range(50):
                            if text[ultimo+50-y] == ' ':
                                linhas.append(text[ultimo:ultimo+50-y])
                                # print(linhas)
                                ultimo = ultimo+50-y+1
                                # print(ultimo)
                                break
                linhas.append(text[ultimo:])
                # print(linhas)

    else:
        linhas.append(text)
        # print(linhas)

    return linhas


transcribe = []

# start up pygame
pygame.init()
# print(sorted(pygame.font.get_fonts()))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
x, y = screen.get_size()

font = pygame.font.SysFont("Liberation Sans", 58)

white = WhiteLine(pygame.Rect(0, 0, x, y), font, YELLOW, BLACK)
#result="o que tem para hoje olhando para os seus dedos minúsculos enquanto você fala de coisas que tem aprendido a valorizar que tem insistido em gravar dentro do meu crânio para que os Olhos enxergam quando se virarem até que o buraco se cubra eu me esqueça como contar 1 2 3 4 e passa a respirar poeira poeira de estrela e da mão não tem nada maior que você aqui importância incomparável emergência te amo como quem acende uma vela no espaço te amo desde a dificuldade de se acender uma vela no espaço na dimensão infinita de um universo sem esquecimentos aqui cheia de sons canto teu codinome"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        else:

            result = sp()

            if (result != False):
                transcribe = break_line(result)
            else:
                transcribe = ['']
            # print("transcribe\n")
            # print(transcribe)
            # print("\n")
            for y in range(len(transcribe)):
                white.update(transcribe[y])
                white.draw(screen)
                pygame.display.flip()
            clock.tick(60)
