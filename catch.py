import pygame
from random import randint

import debug
import settings

pygame.init()
pygame.font.init()


class Door:
    def __init__(self, sprite, lane_number):
        self.sprite = sprite
        self.state = 0
        self.lane_number = lane_number

        self.x = settings.LANES[self.lane_number] + settings.LANE_SIZE // 2 - 32
        self.y = settings.HEIGHT - 64
        self.position = (self.x, self.y)

    def draw_door(self, window):
        window.blit(self.sprite, self.position, (64 * self.state, 32, 64, 32))

    def collide_with(self, item):
        _is_collide = pygame.Rect(
            self.position[0], self.position[1], 64, 32
        ).colliderect(item)
        return _is_collide and self.state == 3

    def open_door(self):
        self.state = 3

    def close_door(self):
        self.state = 0


window = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption(settings.TITLE)

running = True
is_debug_mode = False
clock = pygame.time.Clock()

door = pygame.image.load(settings.DOOR_IMAGE)
gold_item = pygame.image.load(settings.ITEMS_IMAGE)

doors = [Door(door, n) for n in range(4)]
items = []
gravity = 12
door_opened = None
spawn_timer = 60
difficulity = 0
spawn_cooldown = 0
score = 0
lives = 5


def generate_item():
    _lane = randint(-1, 3)
    if _lane < 0:
        return
    _x = settings.LANES[_lane] + settings.LANE_SIZE // 2 - 8
    items.append([_x, 0, 3, 1, _lane])


def controls():
    global door_opened
    key_pressed = pygame.key.get_pressed()
    if door_opened == None:
        if key_pressed[pygame.K_q]:
            doors[0].open_door()
            door_opened = 0
        elif key_pressed[pygame.K_w]:
            doors[1].open_door()
            door_opened = 1
        elif key_pressed[pygame.K_e]:
            doors[2].open_door()
            door_opened = 2
        elif key_pressed[pygame.K_r]:
            doors[3].open_door()
            door_opened = 3
    else:
        if not key_pressed[pygame.K_q] and door_opened == 0:
            doors[0].close_door()
            door_opened = None
        elif not key_pressed[pygame.K_w] and door_opened == 1:
            doors[1].close_door()
            door_opened = None
        elif not key_pressed[pygame.K_e] and door_opened == 2:
            doors[2].close_door()
            door_opened = None
        elif not key_pressed[pygame.K_r] and door_opened == 3:
            doors[3].close_door()
            door_opened = None


def draw_score(window):
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(str(score), False, (255, 255, 255))
    window.blit(text, (10, 10))


def draw_ui(window):
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Lives: {lives}", False, (255, 255, 255))
    window.blit(text, (74, 10))


while running:
    # TODO: Main menu
    dt = clock.tick(60) / 100
    window.fill((0, 0, 0))

    if lives == 0:
        running = False

    if score // 20 != difficulity:
        difficulity = score // 20
        gravity += difficulity

    spawn_cooldown += 1
    if spawn_cooldown >= spawn_timer:
        spawn_cooldown = 0 + (score // 10 * 3)
        generate_item()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                is_debug_mode = not is_debug_mode

            if event.key == pygame.K_l:
                generate_item()

    controls()

    if is_debug_mode:
        debug.draw_lane_line(window)
        debug.draw_door_collision(window)
        debug.draw_fall_line(window)

    for item in items:
        item[1] += gravity * dt
        _position = (item[0], item[1])
        _item_sprite = (16 * item[2], 16 * item[3], 16, 16)
        _sprite = pygame.Surface((16, 16))
        _sprite.blit(gold_item, (0, 0), _item_sprite)
        _sprite = pygame.transform.scale(_sprite, (32, 32))
        window.blit(_sprite, _position)

        _item_rect = (_position[0], _position[1], 32, 32)
        if doors[item[4]].collide_with(_item_rect):
            items.remove(item)
            score += 1

        if item[1] >= settings.HEIGHT + 64:
            items.remove(item)
            lives -= 1

    for door in doors:
        door.draw_door(window)

    draw_score(window)
    draw_ui(window)
    # TODO: End game screen
    pygame.display.update()

pygame.quit()
