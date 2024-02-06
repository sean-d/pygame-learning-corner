import pygame
from sys import exit

pygame.init()

WIDTH, HEIGHT = 800, 600
GROUND = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snail go brrrrr")
clock = pygame.time.Clock()

main_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# we convert all images to a format pygame works with more easily...more easy more performant
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface = pygame.transform.smoothscale(sky_surface, screen.get_size()) # scale to window size

ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surface = main_font.render("SNAIL FORT", False, 'Black')
score_rect = score_surface.get_rect(center = (WIDTH/2, 50))

# use conver_alpha() to handle the alpha values...with only covert() the bg of the snail shows on the surfaces behind it
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800, GROUND))


player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# create a rect around the player_surface where the x,y are measured to the middle bottom of the rect.
# 80 is a good place to start the player from the left. 300 is where the ground_surface is blit'd so this
# puts the player rect on the ground
player_rect = player_surface.get_rect(midbottom = (80, GROUND))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION: print(player_rect.collidepoint(event.pos))

# pygame will lay out the surfaces in the order you call them. so we have the ground overlaying the sky
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0, GROUND))
    screen.blit(score_surface, score_rect)
    snail_rect.right -= 5
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect) # using the player_rect to determine placement of the player surface

    if snail_rect.right <= 0: # if the right side of the snail passes the left side of the screen, giving the visual of exiting stage left
        snail_rect.left = 800 # put the left side of the snail at the right edge of the screen so it appears to be entering the screen

    # mouse_position = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_position):
    #     print(pygame.mouse.get_pressed()) # returns a tuple (False|True, False|True, False|True) that represents left, middle, right buttons if true

    pygame.draw.line(screen, "Pink", (0, 0), (800, 600))
    pygame.display.update()
    clock.tick(60)
