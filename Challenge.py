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
RACE_TRACK_BORDER_MASK = pygame.mask.from_surface(RACE_TRACK_BORDER)

FINISH_LINE = pygame.image.load(os.path.join('imgs', 'finish.png'))

RED_CAR = scale_img(pygame.image.load(
    os.path.join('imgs', 'red-car.png')), 0.03)
GREEN_CAR = scale_img(pygame.image.load(
    os.path.join('imgs', 'green-car.png')), 0.03)

W_KEY = scale_img(pygame.image.load(
    os.path.join('imgs', 'w-key.png')), 0.2)
A_KEY = scale_img(pygame.image.load(
    os.path.join('imgs', 'a-key.png')), 0.2)
S_KEY = scale_img(pygame.image.load(
    os.path.join('imgs', 's-key.png')), 0.2)
D_KEY = scale_img(pygame.image.load(
    os.path.join('imgs', 'd-key.png')), 0.2)


WIDTH, HEIGHT = RACE_TRACK.get_width(), RACE_TRACK.get_height()
print(WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()


class MainCar:
    IMG = GREEN_CAR
    # standaard auto kracht van 2

    def __init__(self, max_vel, rot_vel) -> None:
        self.distance_travelled = 0
        self.max_vel = max_vel
        self.vel = 0
        self.rot_vel = rot_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.accel = 0.012

    def rotate(self, left=False, right=False):
        if left and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle += self.rot_vel

        if left and self.vel == self.max_vel:
            self.angle += (self.rot_vel / 1.5)

        if right and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle -= self.rot_vel

        if right and self.vel == self.max_vel:
            self.angle -= (self.rot_vel / 1.5)

        if left and self.vel < 0:
            self.angle += self.rot_vel / 1.2

        if right and self.vel < 0:
            self.angle -= self.rot_vel / 1.2

    def draw(self, screen):
        blit_rotate_center(screen, self.IMG, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.accel *
                       (abs(self.vel) + 0.5), self.max_vel)
        self.move()

    def move_backwards(self):
        if self.vel > -self.max_vel / 2:
            self.vel -= self.accel

        elif self.vel <= -self.max_vel / 2:
            self.vel = -self.max_vel / 2

        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def drag(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.accel * 2, 0)

        elif self.vel < 0:
            self.vel += self.accel * 2

        self.move()

    def brake(self):
        self.vel -= self.accel * 2

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.IMG)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)

        return poi


class PlayerCar(MainCar):
    IMG = GREEN_CAR
    START_POS = (30, 350)

    def bounce(self):

        if self.vel > 0 and self.vel < self.max_vel / 2:
            self.vel = -(self.vel / 1.7)

        elif self.vel > self.max_vel / 2 and self.vel <= self.max_vel:
            self.vel = -self.vel / 1.5

        elif self.vel < 0:
            self.vel = -self.vel

        if self.vel == 0:
            self.vel -= 0.4

        self.move()


def draw(screen, images, player_car):
    for img, pos in images:
        screen.blit(img, pos)

    player_car.draw(screen)
    pygame.display.update()


def move_player(player_car, image_list):
    keys = pygame.key.get_pressed()

    moving_fw = False
    moving_bw = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
        image_list.append((A_KEY, (0, 720 - 60)))

    if keys[pygame.K_d]:
        player_car.rotate(right=True)
        image_list.append((D_KEY, (98, 720 - 60)))

    if keys[pygame.K_w]:
        moving_fw = True
        player_car.move_forward()
        image_list.append((W_KEY, (30, 720 - 60 - 49)))

    if player_car.vel > 0 and not moving_fw:
        player_car.drag()

    if keys[pygame.K_s]:
        moving_bw = True

        if player_car.vel > 0:
            player_car.brake()

        elif player_car.vel <= 0:
            player_car.move_backwards()

        image_list.append((S_KEY, (50, 720 - 60)))

    if player_car.vel < 0 and not moving_bw:
        player_car.drag()

    return image_list


player_car = PlayerCar(2.5, 2.5)


playing = True
while playing:
    images = [(GRASS, (0, 0)), (RACE_TRACK, (0, 0))]
    images = move_player(player_car, images)

    clock.tick(FPS)

    draw(SCREEN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    if player_car.collide(RACE_TRACK_BORDER_MASK) != None:
        player_car.bounce()

pygame.quit()
