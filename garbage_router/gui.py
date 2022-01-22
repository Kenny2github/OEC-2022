import os
import sys
import pygame
from subprocess import DEVNULL, PIPE, Popen
from .ant_pathfinding import run_rounds
from .cmdargs import args
from .enums import NodeType
from .qor import validator
from .data_io import read_data

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
FPS = 30

FONT = pygame.font.SysFont('Courier New', 20)

class Slider(pygame.sprite.Sprite):
    a: float
    b: float

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((100, 120))
        self.rect = self.image.get_rect()
        self.boundrect = self.rect.copy()
        self.boundrect.y += 10
        self.boundrect.h -= 20
        self.a = self.b = 0.5

    def update(self) -> None:
        x, y = pygame.mouse.get_pos()
        if self.boundrect.collidepoint(x, y) and pygame.mouse.get_pressed()[0]:
            if x > self.rect.x + self.rect.w / 2:
                self.b = 1 - (y - self.boundrect.y) / self.boundrect.h
            else:
                self.a = 1 - (y - self.boundrect.y) / self.boundrect.h
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 0), self.rect, 5)
        pygame.draw.rect(self.image, (0, 0, 0), (self.rect.x, self.rect.y
            + self.boundrect.h * (1 - self.a), self.rect.w / 2, 20))
        pygame.draw.rect(self.image, (0, 0, 0), (
            self.rect.x + self.rect.w // 2,
            self.rect.y + self.boundrect.h * (1 - self.b), self.rect.w / 2, 20))

def arrow(screen, from_pos: tuple[float, float], to_pos: tuple[float, float]):
    pygame.draw.line(screen, (0, 0, 0), from_pos, to_pos)
    pygame.draw.line(screen, (0, 0, 0), (
        pygame.math.Vector2(from_pos) + pygame.math.Vector2(to_pos)) / 2,
                     to_pos, 3)

def center(x, y):
    return pygame.Vector2(WIDTH // 2, HEIGHT // 2) + pygame.Vector2(x, y) * 1.5

def pathfind(screen, nodes, a: float, b: float):

    text = FONT.render('a   b', True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text, (20, 130))
    for node in nodes:
        pygame.draw.rect(screen, {
            NodeType.WASTE: (0, 0, 0),
            NodeType.LOCAL: (255, 0, 0),
            NodeType.REGIONAL: (0, 0, 255),
            NodeType.RECYCLING: (255, 0, 255)
        }[node.type], (*center(node.lat, node.long), 10, 10))
    #path, qor = run_rounds(nodes, a, b)
    process = Popen([sys.executable, f'heuristic_appr/find_pairs.py'], stdin=PIPE, stdout=DEVNULL)
    process.communicate((args().input + f'\n{a}\n{b}\n').encode())
    path = read_data("Yoshi_" + os.path.basename(args().input) + "_output.csv")
    qor = validator([node.to_csv_row() for node in nodes],
                    [node.to_csv_row() for node in path], a, b)

    for i in range(len(path) - 1):
        node, to_node = path[i], path[i+1]
        arrow(screen, center(node.lat, node.long),
              center(to_node.lat, to_node.long))
    text2 = FONT.render('QOR: ' + str(qor), True, (0, 0, 0))
    rect = text2.get_rect()
    rect2 = rect.copy()
    rect2.bottomright = SIZE
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    screen.blit(text2, rect2.topleft)

def main(nodes, a: float, b: float):
    screen = pygame.display.set_mode(SIZE)
    pathfind(screen, nodes, a, b)
    group = pygame.sprite.GroupSingle(Slider())
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pathfind(screen, nodes, group.sprite.a, group.sprite.b)
        group.update()
        group.draw(screen)
        pygame.display.flip()
        pygame.time.delay(1000//FPS)
