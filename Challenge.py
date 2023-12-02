import pygame
import os
import time
import math


def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)

    return pygame.transform.scale(img, size)


def blit_rotate_center(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    screen.blit(rotated_image, new_rect.topleft)


def blit_text_center(screen, font, text):
    render = font.render(text, 1, (0, 204, 0))
    screen.blit(render, (screen.get_width() / 2 -
                render.get_width() / 2, screen.get_height() / 2 -
                render.get_height() / 2))


GRASS = scale_img(pygame.image.load(os.path.join('imgs', 'grass.jpg')), 3)

RACE_TRACK = scale_img(pygame.image.load(
    os.path.join('imgs', 'new-track.png')), 1)
RACE_TRACK_BORDER = scale_img(pygame.image.load(
    os.path.join('imgs', 'new-track-border.png')), 1.15)
RACE_TRACK_BORDER_POS = (0, 0)
RACE_TRACK_BORDER_MASK = pygame.mask.from_surface(RACE_TRACK_BORDER)

FINISH_LINE = scale_img(pygame.transform.rotate(
    pygame.image.load(os.path.join('imgs', 'finish.png')), 90), 0.6)
FINISH_LINE_POS = (204, 697)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH_LINE)

SCORE_TEXT = scale_img(pygame.image.load(
    os.path.join('imgs', 'Score.png')), 0.6)
WIN_SCREEN = scale_img(pygame.image.load(
    os.path.join('imgs', 'Win.png')), 0.6)
LOSE_SCREEN = scale_img(pygame.image.load(
    os.path.join('imgs', 'Lose.png')), 1.7)


LAP0 = scale_img(pygame.image.load(
    os.path.join('imgs', 'number0.png')), 0.3)
LAP1 = scale_img(pygame.image.load(
    os.path.join('imgs', 'number1.png')), 0.3)
LAP2 = scale_img(pygame.image.load(
    os.path.join('imgs', 'number2.png')), 0.3)
LAP3 = scale_img(pygame.image.load(
    os.path.join('imgs', 'number3.png')), 0.3)
LAP4 = scale_img(pygame.image.load(
    os.path.join('imgs', 'number4.png')), 0.3)
LAPS = [LAP0, LAP1, LAP2, LAP3, LAP4]
LAP_POS = (200, 0)

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

pygame.font.init()
FONT = pygame.font.SysFont('calibri', 44)

COMP_CAR_PATH = [(580, 720), (618, 689), (640, 631), (679, 582), (725, 567), (796, 551), (829, 489), (816, 414), (774, 366), (664, 363), (516, 342), (401, 232), (259, 195), (145, 188), (84, 219), (74, 247), (73, 269), (76, 289), (86, 309),
                 (95, 323), (105, 336), (117, 344), (128, 351), (150, 356), (189, 362), (331, 367), (511, 545), (512, 609), (417, 604), (255, 608), (191, 569), (178, 532), (129, 513), (74, 549), (115, 668), (148, 712), (201, 722), (269, 722), (359, 722)]

WIDTH, HEIGHT = RACE_TRACK.get_width(), RACE_TRACK.get_height()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()


class GameInfo:
    LEVELS = 5

    def __init__(self, level=1) -> None:
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return time.time() - self.level_start_time


class MainCar:
    IMG = GREEN_CAR
    # standaard auto kracht van 2

    def __init__(self, max_vel, rot_vel) -> None:
        self.distance_travelled = 0
        self.max_vel = max_vel
        self.vel = 0
        self.rot_vel = rot_vel
        self.angle = 270
        self.x, self.y = self.START_POS
        self.accel = 0.04

    def rotate(self, left=False, right=False):
        if left and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle += self.rot_vel

        if left and self.vel == self.max_vel:
            self.angle += (self.rot_vel / 1.7)

        if right and self.vel < self.max_vel\
                and self.vel > 0:
            self.angle -= self.rot_vel

        if right and self.vel == self.max_vel:
            self.angle -= (self.rot_vel / 1.7)

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
            self.vel = max(self.vel - self.accel * 1.5, 0)

        elif self.vel < 0:

            self.vel += (self.accel * 3)

        self.move()

    def brake(self):
        self.vel -= self.accel * 2

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.IMG)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)

        return poi

    def reset(self, angle=270):
        self.x, self.y = self.START_POS
        self.angle = angle
        self.vel = 0


class PlayerCar(MainCar):
    IMG = GREEN_CAR
    START_POS = (370, 701)

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

    def bounce_finish(self):
        self.vel = -self.vel / 2

        self.move()


class Computer(MainCar):
    IMG = RED_CAR
    START_POS = (390, 725)

    def __init__(self, max_vel, rot_vel, path=None) -> None:
        super().__init__(max_vel, rot_vel)
        if path == None:
            path = []

        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, screen):
        for point in self.path:
            pygame.draw.circle(screen, (255, 255, 0), point, 5)

    def draw(self, screen):
        super().draw(screen)

    def calc_angle(self):
        target_x, target_y = self.path[self.current_point]
        dx = target_x - self.x
        dy = target_y - self.y

        if dy == 0:
            radian_angle = math.pi / 2

        else:
            radian_angle = math.atan(dx / dy)

        if target_y > self.y:
            radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rot_vel, abs(difference_in_angle))

        else:
            self.angle += min(self.rot_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.IMG.get_width(), self.IMG.get_height())

        if rect.collidepoint(target[0], target[1]):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calc_angle()
        self.update_path_point()
        super().move()

    def reset_comp(self, level, angle=270):
        self.x, self.y = self.START_POS
        self.angle = angle
        self.vel = self.max_vel + (level - 1) * 0.3
        self.current_point = 0

    def next_level(self, level):
        self.reset_comp(level)
        self.vel = self.max_vel + (level - 1) * 0.3
        self.current_point = 0


def draw(screen, images, player_car, comp_car):
    for img, pos in images:
        screen.blit(img, pos)

    level_text = FONT.render(f'Level {game_info.level}', 1, (153, 0, 0))
    screen.blit(level_text, (10, 20))

    time_text = FONT.render(
        f'Time: {game_info.get_level_time():.0f}s', 1, (153, 0, 0))
    screen.blit(time_text, (700, 860))

    vel_text = FONT.render(
        f'Velocity: {player_car.vel:.1f}', 1, (153, 0, 0))
    screen.blit(vel_text, (700, 800))

    player_car.draw(screen)
    comp_car.draw(screen)
    pygame.display.update()


def move_player(player_car, image_list):
    keys = pygame.key.get_pressed()

    moving_fw = False
    moving_bw = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
        image_list.append((A_KEY, (0, 800)))

    if keys[pygame.K_d]:
        player_car.rotate(right=True)
        image_list.append((D_KEY, (98, 800)))

    if keys[pygame.K_w]:
        moving_fw = True
        player_car.move_forward()
        image_list.append((W_KEY, (30, 800 - 49)))

    if player_car.vel > 0 and not moving_fw:
        player_car.drag()

    if keys[pygame.K_s]:
        moving_bw = True

        if player_car.vel > 0:
            player_car.brake()

        elif player_car.vel <= 0:
            player_car.move_backwards()

        image_list.append((S_KEY, (50, 800)))

    if player_car.vel < 0 and not moving_bw:
        player_car.drag()

    return image_list


def handle_collision(player_car: PlayerCar, comp_car: Computer, game_info: GameInfo):
    if player_car.collide(RACE_TRACK_BORDER_MASK, RACE_TRACK_BORDER_POS[0], RACE_TRACK_BORDER_POS[1]) != None:
        player_car.bounce()

    player_finish_line_collision_point = player_car.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])

    comp_finish_line_collision_point = computer_car.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])

    if player_finish_line_collision_point != None:

        if player_finish_line_collision_point[0] not in range(12) or player_car.vel < 0\
                or (player_car.angle < 540 and player_car.angle > 370) is True:
            player_car.bounce_finish()

        else:
            game_info.next_level()
            player_car.reset()
            comp_car.next_level(game_info.level)

    if comp_finish_line_collision_point != None:
        SCREEN.blit(LOSE_SCREEN, (250, 400))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        comp_car.reset_comp(game_info.level)
        player_car.reset()


player_car = PlayerCar(3, 3)
computer_car = Computer(1.5, 5, COMP_CAR_PATH)


playing = True

game_info = GameInfo()

while playing:

    while not game_info.started:

        blit_text_center(
            SCREEN, FONT, f'Press Any Key To Start: Level {game_info.level}')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    images = [(GRASS, (0, 0)), (RACE_TRACK, (0, 0)),
              (FINISH_LINE, FINISH_LINE_POS), (RACE_TRACK_BORDER, RACE_TRACK_BORDER_POS)]

    images = move_player(player_car, images)
    computer_car.move()

    draw(SCREEN, images, player_car, computer_car)

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            player_car.x = pygame.mouse.get_pos()[0]
            player_car.y = pygame.mouse.get_pos()[1]
            player_car.vel = 0.5

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        SCREEN.blit(WIN_SCREEN, (200, 200))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset_comp(game_info.level)


pygame.quit()
