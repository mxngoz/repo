import pygame
import os
import time
import math
from Challengefuncties import scale_img

GRASS = scale_img(pygame.image.load(os.path.join('imgs', 'grass.jpg')), 3)

RACE_TRACK = scale_img(pygame.image.load(
    os.path.join('imgs', 'track.png')), 0.8)
RACE_TRACK_BORDER = scale_img(pygame.image.load(
    os.path.join('imgs', 'track-border.png')), 0.8)

FINISH_LINE = pygame.image.load(os.path.join('imgs', 'finish.png'))

RED_CAR = scale_img(pygame.image.load(
    os.path.join('imgs', 'red-car.png')), 0.6)
GREEN_CAR = pygame.image.load(os.path.join('imgs', 'green-car.png'))

WIDTH, HEIGHT = RACE_TRACK.get_width(), RACE_TRACK.get_height()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()


def draw(screen, images):
    for img, pos in images:
        screen.blit(img, pos)


images = [(GRASS, (0, 0)), (RACE_TRACK, (0, 0)), (RED_CAR, (30, 100))]

playing = True
while playing:
    clock.tick(FPS)

    draw(SCREEN, images)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False


pygame.quit()
