import pygame
from pygame.locals import *
from pygame.rect import *
from PIL import Image
import sys
from time import sleep
from src.simulation import Simulation


SCREEN, CLOCK = None, None
BLACK = (0, 0, 0)
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


def draw(sim, step):
    height_per_block = WINDOW_HEIGHT // sim.rows
    width_per_block = WINDOW_WIDTH // sim.cols

    for x, i in enumerate(range(sim.rows)):
        for y, j in enumerate(range(sim.cols)):
            rect = pygame.Rect(y * height_per_block, x*width_per_block,
                               height_per_block, width_per_block)
            global SCREEN
            pygame.draw.rect(SCREEN, sim.grid[i, j].color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 4)


def viz(sim):
    pygame.init()
    global SCREEN, CLOCK

    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    steps_taken = 0
    while steps_taken < 100:
        sim.step()
        draw(sim, steps_taken)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        steps_taken += 1
        sleep(0.5)



if __name__ == '__main__':
    sim = Simulation(0.05, 0.05, 0.05, 0.05, 100, 100)
    viz(sim)