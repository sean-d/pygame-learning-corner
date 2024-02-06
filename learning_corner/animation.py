import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

snail_surface = pygame.image.load('snail1.png')
snail_x_pos = 700

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # this is always going to be drawn at the same place. nothing dynamic about this
    # screen.blit(snail_surface, (700, 250))
    #now each time the while loop goes, the snail moves 1 along the X coord
    screen.blit(snail_surface,(snail_x_pos, 250))
    snail_x_pos -= 10
    pygame.display.update()
    clock.tick(60)
