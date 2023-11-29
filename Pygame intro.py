import pygame
import random

width, height = 1280, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GAME')

# kleuren in rgb
LIGHT_GRAY = (155, 155, 155)
RED = (255, 0, 0)


FPS = 60

VELOCITY = 7

CAR_WIDTH, CAR_HEIGHT = 100, 100


class Car:
    car_width, car_height = 70, 80

    def __init__(self) -> None:

        self.hitbox = pygame.Rect(random.randint(
            100, 700), random.randint(100, 700), CAR_WIDTH, CAR_HEIGHT)
        self.color = (random.randint(1, 255), random.randint(
            1, 255), random.randint(1, 255))

    def movement(self, keys_pressed, other_player):
        if keys_pressed[pygame.K_d]:
            self.hitbox.x += VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.x -= VELOCITY

        if keys_pressed[pygame.K_a]:
            self.hitbox.x -= VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.x += VELOCITY

        if keys_pressed[pygame.K_w]:
            self.hitbox.y -= VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.y += VELOCITY

        if keys_pressed[pygame.K_s]:
            self.hitbox.y += VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.y -= VELOCITY


class BotCar:
    car_width, car_height = 70, 80

    def __init__(self) -> None:

        self.hitbox = pygame.Rect(random.randint(
            100, 700), random.randint(100, 700), CAR_WIDTH, CAR_HEIGHT)
        self.color = (random.randint(1, 255), random.randint(
            1, 255), random.randint(1, 255))

    def movement(self, keys_pressed, other_player):
        # Inputs moeten verandert worden zodat het niet tegen de player input werkt
        # Bot moet predetermined inputs hebben zodat hij uit zichzelf beweegt
        if keys_pressed[pygame.K_d]:
            self.hitbox.x += VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.x -= VELOCITY

        if keys_pressed[pygame.K_a]:
            self.hitbox.x -= VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.x += VELOCITY

        if keys_pressed[pygame.K_w]:
            self.hitbox.y -= VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.y += VELOCITY

        if keys_pressed[pygame.K_s]:
            self.hitbox.y += VELOCITY
            if self.hitbox.colliderect(other_player.hitbox):
                self.hitbox.y -= VELOCITY


def draw_window(players):
    screen.fill(LIGHT_GRAY)

    pygame.draw.rect(screen, players[0].color, players[0].hitbox)
    pygame.draw.rect(screen, players[1].color, players[1].hitbox)
    pygame.display.update()


def main():
    Player = Car()
    Player2 = BotCar()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        Players = [Player, Player2]
        draw_window(Players)

        Player.movement(keys_pressed, Player2)

    pygame.quit()


if __name__ == '__main__':

    main()
