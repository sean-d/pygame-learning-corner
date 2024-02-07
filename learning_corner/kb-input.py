import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("kb input sandbox")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("JUMP")
        if event.type == pygame.KEYUP:
            print("key up")

# this can be in the game loop which makes more sense. it also wont register a billion key strokes when you pressed one due to the FPS ticking
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print("JUMP")

    pygame.display.update()
    clock.tick(60)
