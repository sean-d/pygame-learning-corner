# find or make a font
# write text on a surface
# blit the text surface


import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill('Red')

pygame.display.set_caption("test text")
clock = pygame.time.Clock()

# font_type, font_size
#none = default font in pygame. 50 is size
#main_font = pygame.font.Font(None, 50)
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
#score_surface = main_font.render(text, anti-alias (smooth it out), color)
score_surface = main_font.render("GAME TEXT", False, 'white')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(score_surface, (0,0))
    pygame.display.update()
    clock.tick(60)
