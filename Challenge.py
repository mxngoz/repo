import pygame
import os
import time
import math
from Challengefuncties import scale_img, blit_rotate_center

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


class MainCar:
    IMG = RED_CAR

    def __init__(self, max_vel, rot_vel) -> None:
        self.max_vel = max_vel
        self.vel = 0
        self.rot_vel = rot_vel
        self.angle = 0
        self.x, self.y = self.START_POS

    def rotate(self, left=False, right=False):
        if left and self.vel > :
            self.angle -= self.rot_vel

        elif right:
            self.angle += self.rot_vel

    def draw(self, screen):
        blit_rotate_center(screen, self.IMG, (self.x, self.y), self.angle)


class PlayerCar(MainCar):
    IMG = RED_CAR
    START_POS = (30, 350)


def draw(screen, images, player_car):
    for img, pos in images:
        screen.blit(img, pos)

    player_car.draw(screen)
    pygame.display.update()


images = [(GRASS, (0, 0)), (RACE_TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

playing = True
while playing:
    clock.tick(FPS)

    draw(SCREEN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_car.rotate(left=True)

    if keys[pygame.K_d]:
        player_car.rotate(right=True)


pygame.quit()
