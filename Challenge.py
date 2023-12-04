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
BLUE_CAR = scale_img(pygame.image.load(
    os.path.join('imgs', 'blue-car.png')), 0.03)
GREY_CAR = scale_img(pygame.image.load(
    os.path.join('imgs', 'grey-car.png')), 0.3)

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
COMP_CAR_PATH2 = [(621, 712), (634, 679), (647, 631), (693, 574), (757, 557), (817, 504), (822, 441), (832, 393), (771, 353), (545, 337), (480, 280), (399, 199), (130, 172),
                  (76, 225), (109, 324), (316, 358), (466, 469), (508, 588), (411, 598), (201, 577), (182, 526), (111, 504), (78, 532), (67, 574), (87, 621), (136, 719), (167, 728), (209, 735)]

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

    def __init__(self, max_vel, rot_vel, pos=None, IMG=GREEN_CAR) -> None:
        self.IMG = IMG
        if pos == None:
            pos = (370, 701)
        self.START_POS = pos

        super().__init__(max_vel, rot_vel)

    def bounce(self):

        if self.vel > 0.1 and self.vel < self.max_vel / 2:
            self.vel = -(self.vel / 1.4)

        elif self.vel > self.max_vel / 2 and self.vel <= self.max_vel:
            self.vel = -self.vel / 1.5

        elif self.vel < 0:
            self.vel = 0.7

        if self.vel <= 0.1 and self.vel > 0:
            self.vel = -0.4

        self.move()

    def bounce_finish(self):
        self.vel = -self.vel / 2

        self.move()


class Computer(MainCar):

    def __init__(self, max_vel, rot_vel, path=None, START_POS=None, IMG=RED_CAR) -> None:
        if START_POS == None:
            START_POS = (390, 725)

        self.IMG = IMG
        self.START_POS = START_POS
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


def draw(screen, images, player_car, player_car2, comp_car1, comp_car2):
    for img, pos in images:
        screen.blit(img, pos)

    level_text = FONT.render(f'Level {game_info.level}', 1, (153, 0, 0))
    screen.blit(level_text, (10, 20))

    time_text = FONT.render(
        f'Time: {game_info.get_level_time():.0f}s', 1, (153, 0, 0))
    screen.blit(time_text, (700, 860))

    vel_text1 = FONT.render(
        f'Velocity P1: {player_car.vel:.1f}', 1, (153, 0, 0))
    vel_text2 = FONT.render(
        f'Velocity P2: {player_car2.vel:.1f}', 1, (153, 0, 0))
    screen.blit(vel_text2, (650, 800))
    screen.blit(vel_text1, (650, 760))

    player_car.draw(screen)
    player_car2.draw(screen)
    comp_car1.draw(screen)
    comp_car2.draw(screen)
    pygame.display.update()


def move_player1(player_car1, image_list):
    keys = pygame.key.get_pressed()

    moving_fw = False
    moving_bw = False

    if keys[pygame.K_a]:
        player_car1.rotate(left=True)
        image_list.append((A_KEY, (0, 800)))

    if keys[pygame.K_d]:
        player_car1.rotate(right=True)
        image_list.append((D_KEY, (98, 800)))

    if keys[pygame.K_w]:
        moving_fw = True
        player_car1.move_forward()
        image_list.append((W_KEY, (30, 800 - 49)))

    if player_car1.vel > 0 and not moving_fw:
        player_car1.drag()

    if keys[pygame.K_s]:
        moving_bw = True

        if player_car1.vel > 0:
            player_car1.brake()

        elif player_car1.vel <= 0:
            player_car1.move_backwards()

        image_list.append((S_KEY, (50, 800)))

    if player_car1.vel < 0 and not moving_bw:
        player_car1.drag()

    return image_list


def move_player2(player_car2):
    keys = pygame.key.get_pressed()

    moving_fw = False
    moving_bw = False

    if keys[pygame.K_LEFT]:
        player_car2.rotate(left=True)

    if keys[pygame.K_RIGHT]:
        player_car2.rotate(right=True)

    if keys[pygame.K_UP]:
        moving_fw = True
        player_car2.move_forward()

    if player_car2.vel > 0 and not moving_fw:
        player_car2.drag()

    if keys[pygame.K_DOWN]:
        moving_bw = True

        if player_car2.vel > 0:
            player_car2.brake()

        elif player_car2.vel <= 0:
            player_car2.move_backwards()

    if player_car2.vel < 0 and not moving_bw:
        player_car2.drag()


def handle_collision(player_car1: PlayerCar, player_car2: PlayerCar, comp_car1: Computer, comp_car2: Computer, game_info: GameInfo):
    if player_car1.collide(RACE_TRACK_BORDER_MASK, RACE_TRACK_BORDER_POS[0], RACE_TRACK_BORDER_POS[1]) != None:
        player_car1.bounce()
        print(player_car1.vel)

    if player_car2.collide(RACE_TRACK_BORDER_MASK, RACE_TRACK_BORDER_POS[0], RACE_TRACK_BORDER_POS[1]) != None:
        player_car2.bounce()

    player1_finish_line_collision_point = player_car1.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])

    player2_finish_line_collision_point = player_car1.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])

    comp1_finish_line_collision_point = comp_car1.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])
    comp2_finish_line_collision_point = comp_car2.collide(
        FINISH_LINE_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1])

    if player1_finish_line_collision_point != None:

        if player1_finish_line_collision_point[0] not in range(11) or player_car1.vel < 0\
                or (player_car1.angle < 540 and player_car1.angle > 370) is True:
            player_car1.bounce_finish()

        else:
            game_info.next_level()
            player_car1.reset()
            player_car2.reset()
            comp_car1.next_level(game_info.level)
            comp_car2.next_level(game_info.level)

    if player2_finish_line_collision_point != None:

        if player2_finish_line_collision_point[0] not in range(11) or player_car2.vel < 0\
                or (player_car2.angle < 540 and player_car2.angle > 370) is True:
            player_car2.bounce_finish()

        else:
            game_info.next_level()
            player_car1.reset()
            player_car2.reset()
            comp_car1.next_level(game_info.level)
            comp_car2.next_level(game_info.level)

    if comp1_finish_line_collision_point != None:
        SCREEN.blit(LOSE_SCREEN, (250, 500))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        comp_car1.reset_comp(game_info.level)
        comp_car2.reset_comp(game_info.level)
        player_car1.reset()
        player_car2.reset()

    if comp2_finish_line_collision_point != None:
        SCREEN.blit(LOSE_SCREEN, (250, 500))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        comp_car1.reset_comp(game_info.level)
        comp_car2.reset_comp(game_info.level)
        player_car1.reset()
        player_car2.reset()


player_car = PlayerCar(3, 3)
player_car2 = PlayerCar(3, 3, pos=(410, 701), IMG=GREY_CAR)
computer_car = Computer(1.5, 5, COMP_CAR_PATH)
computer_car2 = Computer(1.6, 5, COMP_CAR_PATH2, (424, 725), BLUE_CAR)


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
    move_player2(player_car2)
    images = move_player1(player_car, images)

    computer_car.move()
    computer_car2.move()

    draw(SCREEN, images, player_car, player_car2, computer_car, computer_car2)

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    handle_collision(player_car, player_car2, computer_car,
                     computer_car2, game_info)

    if game_info.game_finished():
        SCREEN.blit(WIN_SCREEN, (200, 200))
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset_comp(game_info.level)
        computer_car2.reset_comp(game_info.level)

pygame.quit()
