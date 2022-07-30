import pygame

w, h = 600, 600
white = [255, 255, 255]
black = [0, 0, 0]
green = [0, 255, 0]
thickness = 2
tile_dim = 30

pygame.init()
screen = pygame.display.set_mode([w, h])
clock = pygame.time.Clock()
fps = 5
screen.fill(black)
pygame.display.update()
pygame.draw.rect(screen, white, [[0, 0], [tile_dim, tile_dim]], width=thickness)
pygame.display.update()

snake = [[3 * tile_dim, 4 * tile_dim], [2 * tile_dim, 4 * tile_dim], [tile_dim, 4 * tile_dim]]
direction = [tile_dim, 0]

def draw_snake():
    for tile in snake:
        pygame.draw.rect(screen,
                         green,
                         [tile, [tile_dim, tile_dim]])

def move_snake():
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i-1].copy()
    snake[0] = [snake[0][0] + direction[0], snake[0][1] + direction[1]]


def draw_tiles():
    for i in range(w // tile_dim):
        for j in range(h // tile_dim):
            pygame.draw.rect(screen, white,
                             [[i * tile_dim, j * tile_dim],
                              [tile_dim, tile_dim]],
                             width=thickness)
running = True
while running:
    clock.tick(fps)
    screen.fill(black)
    move_snake()
    draw_tiles()
    draw_snake()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
