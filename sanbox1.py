import pygame

w, h = 600, 600
white = [255, 255, 255]
black = [0, 0, 0]
thickness = 2
tile_dim = 30

pygame.init()
screen = pygame.display.set_mode([w, h])
screen.fill(black)
pygame.display.update()
pygame.draw.rect(screen, white, [[0, 0], [tile_dim, tile_dim]], width=thickness)
pygame.display.update()


def draw_tiles():
    for i in range(w // tile_dim):
        for j in range(h // tile_dim):
            pygame.draw.rect(screen, white,
                             [[i * tile_dim, j * tile_dim],
                              [tile_dim, tile_dim]],
                             width=thickness)
running = True
while running:
    draw_tiles()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
