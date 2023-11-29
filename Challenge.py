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
    os.path.join('imgs', 'red-car.png')), 0.4)
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
        self.accel = 0.3

    def rotate(self, left=False, right=False):
        if left and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle += self.rot_vel

        if left and self.vel == self.max_vel:
            self.angle += (self.rot_vel / 1.3)

        if right and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle -= self.rot_vel

        if right and self.vel == self.max_vel:
            self.angle -= (self.rot_vel / 1.3)

    def draw(self, screen):
        blit_rotate_center(screen, self.IMG, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.accel, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def drag(self, force):
        self.vel = max(self.vel - force, 0)
        self.move()


class PlayerCar(MainCar):
    IMG = RED_CAR
    START_POS = (30, 350)


def draw(screen, images, player_car):
    for img, pos in images:
        screen.blit(img, pos)

    player_car.draw(screen)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()

    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)

    if keys[pygame.K_d]:
        player_car.rotate(right=True)

    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    if not moved:
        player_car.drag(force=0.03)

    if keys[pygame.K_s]:
        player_car.drag(force=0.09)


images = [(GRASS, (0, 0)), (RACE_TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

playing = True
while playing:
    clock.tick(FPS)

    draw(SCREEN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    move_player(player_car)


pygame.quit()
