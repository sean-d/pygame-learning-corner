import pygame
from sys import exit

pygame.init()

def get_score():
    current_time = int(pygame.time.get_ticks() /  1000) - start_time
    score_surface = main_font.render(f"Score: {current_time}", False, 'Black')
    score_rect = score_surface.get_rect(center = (WIDTH/2, 50))
    screen.blit(score_surface, score_rect)
    return current_time

WIDTH, HEIGHT = 800, 600
GROUND = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snail go brrrrr")
clock = pygame.time.Clock()

start_time = 0
score = 0
game_active = True

main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
scorsese_font = pygame.font.Font('font/Pixeltype.ttf', 150)

# we convert all images to a format pygame works with more easily...more easy more performant
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface = pygame.transform.smoothscale(sky_surface, screen.get_size()) # scale to window size

ground_surface = pygame.image.load('graphics/ground.png').convert()


scorsese_surface = scorsese_font.render("SCORSESE RED", False, 'Black')
scorsese_rect = scorsese_surface.get_rect(center = (WIDTH/2, 100))

restart_surface = main_font.render("press y to restart", False, 'Black')
restart_rect = scorsese_surface.get_rect(center = (WIDTH/2, 400))


# use conver_alpha() to handle the alpha values...with only covert() the bg of the snail shows on the surfaces behind it
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (800, GROUND))


player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# create a rect around the player_surface where the x,y are measured to the middle bottom of the rect.
# 80 is a good place to start the player from the left. GROUND is well, global ground. :)
player_rect = player_surface.get_rect(midbottom = (80, GROUND))
player_gravity = 0
player_gameover_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_gameover_surface = pygame.transform.rotozoom(player_gameover_surface, 0, 2) # scale the player, at 0 angle, 2x scale
player_gameover_rect = player_gameover_surface.get_rect(midbottom = (500, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN and game_active == False:
                if event.key == pygame.K_y:
                    start_time = int(pygame.time.get_ticks() / 1000) # set this to what the get_score has so when the game restarts, the score resets to 0.
                    game_active = True
                    snail_rect.left = 800
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= GROUND: # single-jump only
                        player_gravity = -20
            # mouse_position = pygame.mouse.get_pos()
            # if player_rect.collidepoint(mouse_position):
            # print(pygame.mouse.get_pressed()) # returns a tuple (False|True, False|True, False|True) that represents left, middle, right buttons if true
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= GROUND: # single-jump only
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20
    if game_active:
    # pygame will lay out the surfaces in the order you call them. so we have the ground overlaying the sky
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, GROUND))
        # screen.blit(score_surface, score_rect) # replacing with a score timer
        score = get_score()

        snail_rect.right -= 5
        screen.blit(snail_surface, snail_rect)
        if snail_rect.right <= 0: # if the right side of the snail passes the left side of the screen, giving the visual of exiting stage left
            snail_rect.left = 800 # put the left side of the snail at the right edge of the screen so it appears to be entering the screen


        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= GROUND: player_rect.bottom = GROUND
        if player_rect.top <= 0: player_rect.top = 0 # if single-jump is removed, the player is ceiling'd at the ceiling

        screen.blit(player_surface, player_rect) # using the player_rect to determine placement of the player surface

        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        final_score_surface = main_font.render(f"Score: {score}", False, 'Black')
        final_score_rect = final_score_surface.get_rect(center = (WIDTH/2, 500))

        screen.fill("Dark Red")
        screen.blit(scorsese_surface, scorsese_rect)
        screen.blit(player_gameover_surface, player_gameover_rect)
        print(score)
        screen.blit(final_score_surface, final_score_rect)
        screen.blit(restart_surface, restart_rect)


    pygame.display.update()
    clock.tick(60)
