import pygame
import random

w, h = 600, 600
white = [255, 255, 255]
black = [0, 0, 0]
green = [0, 255, 0]
red = [255, 0, 0]
thickness = 2
tile_dim = 30

pygame.init()
screen = pygame.display.set_mode([w, h])
clock = pygame.time.Clock()
fps = 10
screen.fill(black)
pygame.display.update()
pygame.draw.rect(screen, white, [[0, 0], [tile_dim, tile_dim]], width=thickness)
pygame.display.update()

snake = [[3 * tile_dim, 4 * tile_dim], [2 * tile_dim, 4 * tile_dim], [tile_dim, 4 * tile_dim]]
direction = [tile_dim, 0]

apple = [0, 0]
apple_eaten = True


def spawn_apple():
    global apple
    overlap = True
    while overlap:
        apple = [random.randint(0, w // tile_dim - 1) * tile_dim,
                 random.randint(0, h // tile_dim - 1) * tile_dim]
        for i in range(len(snake)):
            overlap = snake[i][0] == apple[0] and snake[i][1] == apple[1]
            if overlap:
                break


def draw_apple():
    pygame.draw.rect(screen,
                     red,
                     [apple, [tile_dim, tile_dim]])


def check_collision():
    if snake[0][0] < 0 or snake[0][0] >= w or snake[0][1] < 0 or snake[0][1] >= h:
        return True
    for i in range(1, len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True
    return False


def draw_snake():
    for tile in snake:
        pygame.draw.rect(screen,
                         green,
                         [tile, [tile_dim, tile_dim]])


def move_snake():
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i - 1].copy()
    snake[0] = [snake[0][0] + direction[0], snake[0][1] + direction[1]]


def draw_tiles():
    for i in range(w // tile_dim):
        for j in range(h // tile_dim):
            pygame.draw.rect(screen, white,
                             [[i * tile_dim, j * tile_dim],
                              [tile_dim, tile_dim]],
                             width=thickness)


def eat_apple():
    global apple_eaten
    if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
        apple_eaten = True
        snake.append(snake[-1].copy())


running = True
while running:
    clock.tick(fps)
    screen.fill(black)
    if apple_eaten:
        spawn_apple()
        apple_eaten = False
    move_snake()
    running = not check_collision()
    draw_tiles()
    draw_snake()
    draw_apple()
    eat_apple()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if direction[1] != -tile_dim:
                    direction = [0, tile_dim]
            if event.key == pygame.K_UP:
                if direction[1] != tile_dim:
                    direction = [0, -tile_dim]
            if event.key == pygame.K_RIGHT:
                if direction[0] != -tile_dim:
                    direction = [tile_dim, 0]
            if event.key == pygame.K_LEFT:
                if direction[0] != tile_dim:
                    direction = [-tile_dim, 0]
