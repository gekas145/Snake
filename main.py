import pygame
import random

w, h = 600, 600
tile_dim = 60
tile_thickness = 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
fps = 10

pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("SNAKE")
screen.fill(BLACK)
pygame.display.update()
clock = pygame.time.Clock()

snake = [[tile_dim, 4 * tile_dim], [2 * tile_dim, 4 * tile_dim], [3 * tile_dim, 4 * tile_dim]]
direction = [tile_dim, 0]

apple = []
apple_eaten = True

end_game = False


def spawn_apple():
    global apple
    overlap = True
    while overlap:
        apple = [random.randint(0, w // tile_dim) * tile_dim,
                 random.randint(0, h // tile_dim) * tile_dim]
        snake_head = pygame.Rect(snake[0].copy(), [tile_dim, tile_dim])
        overlap = snake_head.colliderect(pygame.Rect(apple.copy(),
                                                     [tile_dim, tile_dim]))

def eat_apple():
    pass

def draw_tiles():
    for i in range(w // tile_dim):
        for j in range(h // tile_dim):
            pygame.draw.rect(screen, WHITE,
                             (i * tile_dim, j * tile_dim, tile_dim, tile_dim),
                             tile_thickness)


def draw_snake():
    for tile in snake:
        pygame.draw.rect(screen, GREEN, (tile[0], tile[1], tile_dim, tile_dim))


def snake_move():
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = snake[i - 1].copy()
    snake[0] = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

def check_collision():
    if snake[0][0] < 0 or snake[0][0] >= w or snake[0][1] < 0 or snake[0][1] >= h:
        return True
    return False


def main():
    global end_game
    global direction
    global apple_eaten
    while not end_game:
        clock.tick(fps)
        screen.fill(BLACK)
        snake_move()
        end_game = check_collision()
        draw_tiles()
        draw_snake()
        if apple_eaten:
            spawn_apple()
            apple_eaten = False
        pygame.draw.rect(screen, RED, (apple[0], apple[1], tile_dim, tile_dim))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if direction[1] == -tile_dim:
                        break
                    direction = [0, tile_dim]
                elif event.key == pygame.K_UP:
                    if direction[1] == tile_dim:
                        break
                    direction = [0, -tile_dim]
                elif event.key == pygame.K_RIGHT:
                    if direction[0] == -tile_dim:
                        break
                    direction = [tile_dim, 0]
                elif event.key == pygame.K_LEFT:
                    if direction[0] == tile_dim:
                        break
                    direction = [-tile_dim, 0]


if __name__ == "__main__":
    main()
