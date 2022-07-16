import pygame

w, h = 600, 600

pygame.init()
screen = pygame.display.set_mode((w, h))
blue = [0, 0, 255]
red = [255, 0, 0]
white = [255, 255, 255]
screen.fill(white)
pygame.display.update()
pygame.display.set_caption('SNAKE')
running = True
# pygame.draw.rect(screen, red, [100, 100, 200, 200], width=20)
pygame.display.update()
x, y = 200, 200
step = 0.2
vector = [1, 0]
while running:
    screen.fill(white)
    x = x + vector[0] * step
    y = y + vector[1] * step
    pygame.draw.rect(screen, blue, [x, y, 50, 50], width=20)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                vector = [0, -1]
            if event.key == pygame.K_DOWN:
                vector = [0, 1]
            if event.key == pygame.K_LEFT:
                vector = [-1, 0]
            if event.key == pygame.K_RIGHT:
                vector = [1, 0]









