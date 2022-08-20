import pygame
import random
import math

w, h = 600, 600
tile_dim = 30
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

snake = [[3 * tile_dim, 4 * tile_dim], [2 * tile_dim, 4 * tile_dim], [tile_dim, 4 * tile_dim]]
direction = [tile_dim, 0]

apple = []
apple_eaten = True

end_game = False

ai_plays = True

possible_moves = [[0, tile_dim], [0, -tile_dim], [tile_dim, 0], [-tile_dim, 0]]


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


def eat_apple():
    global apple_eaten
    global snake
    if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
        apple_eaten = True
        snake.append(snake[-1].copy())


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
    for i in range(1, len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True
    return False


def main():
    global end_game
    global direction
    global apple_eaten
    while not end_game:
        clock.tick(fps)
        screen.fill(BLACK)
        if apple_eaten:
            spawn_apple()
            apple_eaten = False
        snake_move()
        end_game = check_collision()
        draw_tiles()
        draw_snake()
        pygame.draw.rect(screen, RED, (apple[0], apple[1], tile_dim, tile_dim))
        eat_apple()
        pygame.display.update()
        if not ai_plays:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if direction[1] == -tile_dim:
                            break
                        direction = possible_moves[0]
                    elif event.key == pygame.K_UP:
                        if direction[1] == tile_dim:
                            break
                        direction = possible_moves[1]
                    elif event.key == pygame.K_RIGHT:
                        if direction[0] == -tile_dim:
                            break
                        direction = possible_moves[2]
                    elif event.key == pygame.K_LEFT:
                        if direction[0] == tile_dim:
                            break
                        direction = possible_moves[3]
        else:
            chosen_move = possible_moves[0].copy()
            min_dist = math.inf
            old_snake_head = snake[0].copy()
            for move in possible_moves:
                snake[0] = [old_snake_head[0] + move[0], old_snake_head[1] + move[1]]
                is_collision = check_collision()
                if not is_collision:
                    dist = abs(snake[0][0] - apple[0]) + abs(snake[0][1] - apple[1])
                    if dist < min_dist:
                        chosen_move = move.copy()
                        min_dist = dist
            direction = chosen_move.copy()
            snake[0] = old_snake_head.copy()


if __name__ == "__main__":
    main()
