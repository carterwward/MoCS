import pygame
from pygame.locals import *
from pygame.rect import *
from PIL import Image
import sys
from time import sleep, time
import os
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


def screenshot(screen, path, step):
    title = "step" + str(step)
    file_save_as = os.path.join(path, title + ".png")
    pygame.image.save(screen, file_save_as)
    # print(f"step {step} has been screenshotted")


def viz(sim):
    stills = []
    path = os.path.join("assignment_2", "img", "sim_"+str(time()))
    skip = 1
    if not os.path.exists(path):
            os.makedirs(path)

    pygame.init()
    global SCREEN, CLOCK

    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    steps_taken = 0
    while steps_taken < 50:
        sim.step()
        draw(sim, steps_taken)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if steps_taken % skip == 0:
            screenshot(SCREEN, path, steps_taken)
            stills.append(os.path.join(path, "step" + str(steps_taken) + ".png"))
        steps_taken += 1
        # sleep(1)

    img, *imgs = [Image.open(f) for f in stills]
    img.save(fp=os.path.join("assignment_2", "img", str(time())+".gif"), format='gif', append_images=imgs, save_all=True, duration=100, loop=0)
    for im in stills:
        os.remove(im)
    os.rmdir(path)


if __name__ == '__main__':
    sim = Simulation(0.1, 0.1, 0.1, 0.1, 25, 25)
    viz(sim)
