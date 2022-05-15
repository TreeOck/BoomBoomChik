import random
import sys
import math

import pygame as pg
import pygame.draw

pg.init()
display = pg.display.set_mode((1880, 1040))
clock = pg.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRASS = (24, 164, 86)
WHITE = (255, 255, 255)

player_walk_horizontal = [pg.image.load("right_frame1.png"), pg.image.load("right_frame2.png"), pg.image.load(
    "right_frame3.png"), pg.image.load("right_frame4.png")]

player_walk_up = [pg.image.load("up_frame1.png"), pg.image.load("up_frame2.png"), pg.image.load("up_frame3.png"),
                  pg.image.load("up_frame4.png")]

player_walk_down = [pg.image.load("down_frame1.png"), pg.image.load("down_frame2.png"),
                    pg.image.load("down_frame3.png"),
                    pg.image.load("down_frame4.png")]

player_weapon = pg.image.load("rifle.png").convert()
player_weapon.set_colorkey(BLACK)


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anim_count = 0
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def weapons(self, display):
        mouse_x, mouse_y = pg.mouse.get_pos()

        rel_x, rel_y = mouse_x - player.x, mouse_y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pg.transform.rotate(player_weapon, angle)
        player_weapon_copy = pg.transform.scale(player_weapon_copy, (self.width + 10, self.height + 10))

        display.blit(player_weapon_copy, (self.x + 15 - int(player_weapon_copy.get_width() / 2), self.y + 30 - int(
            player_weapon_copy.get_height() / 2)))

    def main(self, display):
        if self.anim_count + 1 >= 16:
            self.anim_count = 0
        self.anim_count += 1

        if self.moving_right:
            display.blit(pg.transform.scale(player_walk_horizontal[self.anim_count // 4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
            display.blit(
                pg.transform.scale(pg.transform.flip(player_walk_horizontal[self.anim_count // 4], True, False),
                                   (32, 42)), (self.x, self.y))
        elif self.moving_up:
            display.blit(pg.transform.scale(player_walk_up[self.anim_count // 4], (32, 42)), (self.x, self.y))
        elif self.moving_down:
            display.blit(pg.transform.scale(player_walk_down[self.anim_count // 4], (32, 42)), (self.x, self.y))
        else:
            display.blit(pg.transform.scale(pg.image.load("standing_player.png"), (32, 42)), (self.x, self.y))

        self.weapons(display)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


class EnemyPumpkin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_images = [pg.image.load("pumpkin_frame1.png"), pg.image.load("pumpkin_frame2.png"), pg.image.load(
            "pumpkin_frame3.png"), pg.image.load("pumpkin_frame4.png"), pg.image.load("pumpkin_frame5.png"),
                            pg.image.load("pumpkin_frame6.png")]
        self.anim_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)

    def main(self, display):
        if self.anim_count + 1 >= 24:
            self.anim_count = 0
        self.anim_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-100, 100)
            self.offset_y = random.randrange(-100, 100)
            self.reset_offset = random.randrange(80, 100)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x - display_scroll[0]:
            self.x += 3
        elif player.x + self.offset_x < self.x - display_scroll[0]:
            self.x -= 3

        if player.y + self.offset_y > self.y - display_scroll[1]:
            self.y += 3
        elif player.y + self.offset_y < self.y - display_scroll[1]:
            self.y -= 3

        display.blit(pg.transform.scale(self.anim_images[self.anim_count // 6], (32, 30)), (self.x - display_scroll[
            0], self.y - display_scroll[1]))


class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

    def main(self, display):
        self.x -= int(self.vel_x)
        self.y -= int(self.vel_y)

        pygame.draw.circle(display, BLACK, (self.x + 15, self.y + 15), 5)


player = Player(940, 520, 32, 32)
enemies = [EnemyPumpkin(400, 300), EnemyPumpkin(200, 200)]
player_bullets = []

display_scroll = [0, 0]

while True:
    display.fill(GRASS)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pg.key.get_pressed()
    pg.draw.rect(display, WHITE, (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))
    pg.draw.rect(display, WHITE, (150 - display_scroll[0], 150 - display_scroll[1], 16, 16))

    if keys[pg.K_a] or keys[pg.K_LEFT]:
        display_scroll[0] -= 8
        player.moving_left = True
        for bullet in player_bullets:
            bullet.x += 8

    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        display_scroll[0] += 8
        player.moving_right = True
        for bullet in player_bullets:
            bullet.x -= 8

    if keys[pg.K_w] or keys[pg.K_UP]:
        display_scroll[1] -= 8
        player.moving_up = True
        for bullet in player_bullets:
            bullet.y += 8

    if keys[pg.K_s] or keys[pg.K_DOWN]:
        display_scroll[1] += 8
        player.moving_down = True
        for bullet in player_bullets:
            bullet.y -= 8

    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    for enemy in enemies:
        enemy.main(display)

    clock.tick(60)
    pg.display.update()
