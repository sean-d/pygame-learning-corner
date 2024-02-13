import pygame
from sys import exit
from random import randint

pygame.init()

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == GROUND: screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)
        # remove any obstacle that is beyond the far left wall after it moves....
        obstacle_list = [rect for rect in obstacle_list if rect.x > -100]

        return obstacle_list
    # we return an empty list. when the game starts, the timer has not run yet and there is no obstacle_rect_list list yet. So when it attempts to append to it
    # it will be appending to the returned value of NoneType. So we return an empty list which can then be appended to.
    else:
        return []

def check_colissions(player, obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            if player.colliderect(obstacle): return False
    return True

def get_score():
    current_time = int(pygame.time.get_ticks() /  1000) - start_time
    score_surface = main_font.render(f"Score: {current_time}", False, 'Black')
    score_rect = score_surface.get_rect(center = (WIDTH/2, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def player_animation():
    global player_surf, player_walk_index
    # play walking if on floor
    if player_rect.bottom == GROUND:
        # .1->.9 cast as an int to 0. 1 to 1.9 cast to 1.
        # so we reset the index back to 0 when it hits a length longer than the number of walk animations avaialble
        player_walk_index += 0.1
        if player_walk_index > len(player_walk):
            player_walk_index = 0
        player_surf = player_walk[int(player_walk_index)]
    # play jumping if not on floor
    else:
        player_surf = player_jump

WIDTH, HEIGHT = 800, 600
GROUND = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snail go brrrrr")
clock = pygame.time.Clock()

start_time = 0
score = 0
game_active = False # start at a loading screen rather than jumping straing into the game

main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
scorsese_font = pygame.font.Font('font/Pixeltype.ttf', 150)

# we convert all images to a format pygame works with more easily...more easy more performant
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface = pygame.transform.smoothscale(sky_surface, screen.get_size()) # scale to window size

ground_surface = pygame.image.load('graphics/ground.png').convert()


scorsese_surface = scorsese_font.render("SCORSESE RED", False, 'Black')
scorsese_rect = scorsese_surface.get_rect(center = (WIDTH/2, 100))

restart_surface = main_font.render("press y to play", False, 'Black')
restart_rect = scorsese_surface.get_rect(center = (WIDTH/2, 400))


# OBSTACLES
# use conver_alpha() to handle the alpha values...with only covert() the bg of the snail shows on the surfaces behind it

# snail
## each image is stored as a surface and then kept in a list
## we default to index 0 as the starting off point for the snail surface
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]
# fly_rect = fly_surface.get_rect(midbottom = (900, 100))  # do not use anymore

obstacle_rect_list = []


# PLAYER
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_walk_index = 0 # represents which surface will be shown for the walk animation
player_surf = player_walk[player_walk_index]
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
# create a rect around the player_surface where the x,y are measured to the middle bottom of the rect.
# 80 is a good place to start the player from the left. GROUND is well, global ground. :)
player_rect = player_surf.get_rect(midbottom = (80, GROUND))
player_gravity = 0
player_gameover_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_gameover_surface = pygame.transform.rotozoom(player_gameover_surface, 0, 2) # scale the player, at 0 angle, 2x scale
player_gameover_rect = player_gameover_surface.get_rect(midbottom = (500, 400))


#TIMER
## there are pygame reserved events, so to avoid overlapping, we add a +1 to the event
obstacle_timer = pygame.USEREVENT + 1
snail_timer = pygame.USEREVENT + 2
fly_timer = pygame.USEREVENT + 3

# trigger event in certain intervals
# https://www.pygame.org/docs/ref/time.html?highlight=set_timer#pygame.time.set_timer
pygame.time.set_timer(obstacle_timer, 1400) # triggered event, often to trigger in ms
pygame.time.set_timer(snail_timer, 500)
pygame.time.set_timer(fly_timer, 200)




#GAME LOOP
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
                    # snail_rect.left = 800  # we are no longer using snail_rect and we are handling obstacles in the obstacle movement fn
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= GROUND: # single-jump only
                        player_gravity = -18
            # mouse_position = pygame.mouse.get_pos()
            # if player_rect.collidepoint(mouse_position):
            # print(pygame.mouse.get_pressed()) # returns a tuple (False|True, False|True, False|True) that represents left, middle, right buttons if true
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= GROUND: # single-jump only
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20
            # timer for launching obstacles at the player
            # if randint is 0 (true), a fly gets added to the obstacle list. else a snail
            if event.type == obstacle_timer:
                if randint(0, 2): obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), GROUND)))
                else: obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 290)))

            if event.type == snail_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

            # each time the snail timer runs, the index changes causing the animation to occur

    if game_active:
    # pygame will lay out the surfaces in the order you call them. so we have the ground overlaying the sky
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, GROUND))
        # screen.blit(score_surface, score_rect) # replacing with a score timer
        score = get_score()

        # removed as this is no longer needed as it will live inside the obstacle timer stuff
        # snail_rect.right -= 5
        # screen.blit(snail_surface, snail_rect)
        # if snail_rect.right <= 0: # if the right side of the snail passes the left side of the screen, giving the visual of exiting stage left
        #     snail_rect.left = 800 # put the left side of the snail at the right edge of the screen so it appears to be entering the screen


        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= GROUND: player_rect.bottom = GROUND
        if player_rect.top <= 0: player_rect.top = 0 # if single-jump is removed, the player is ceiling'd at the ceiling
        player_animation() # right before we blip the player is the right place for this
        screen.blit(player_surf, player_rect) # using the player_rect to determine placement of the player surface

        # Collision Detection
        game_active = check_colissions(player_rect, obstacle_rect_list)
        # snail_rect is no longer a thing. we will deal with collisions elsewhere
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
    else:
        obstacle_rect_list.clear() # remove all items so when the game restarts, we are not colliding with what killed us previously
        player_rect.midbottom = (80, GROUND) # same as when the player_rect is initialized. this way we start on the ground if we die in the air
        player_gravity = 0 # initialize this back to 0 as well
        final_score_surface = main_font.render(f"Score: {score}", False, 'Black')
        final_score_rect = final_score_surface.get_rect(center = (WIDTH/2, 500))

        # the load-in screen for having not played yet
        if score == 0:
            screen.fill((94, 129, 162))
            screen.blit(player_gameover_surface, player_gameover_rect)
            screen.blit(restart_surface, restart_rect)

        # for when you die and are asked to play again
        else:
            screen.fill("Dark Red")
            screen.blit(scorsese_surface, scorsese_rect)
            screen.blit(player_gameover_surface, player_gameover_rect)
            screen.blit(final_score_surface, final_score_rect)
            screen.blit(restart_surface, restart_rect)


    pygame.display.update()
    clock.tick(60)
