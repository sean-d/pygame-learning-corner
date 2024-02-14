import pygame
from sys import exit
from random import randint
from random import choice


pygame.init()



##########################
# GAME INIT DECLARATIONS #
##########################

WIDTH, HEIGHT = 800, 600
GROUND = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snail go brrrrr")
clock = pygame.time.Clock()

start_time = 0
score = 0
game_active = False

# FONTS
main_font = pygame.font.Font('font/Pixeltype.ttf', 50)
scorsese_font = pygame.font.Font('font/Pixeltype.ttf', 150)

# SKY
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface = pygame.transform.smoothscale(sky_surface, screen.get_size()) # scale to window size

# GROUND
ground_surface = pygame.image.load('graphics/ground.png').convert()

# BG MUSIC
# loops -1 means forever
bg_music = pygame.mixer.Sound('audio/bg-music.wav')
bg_music.play(loops = -1)

# GAMEOVER
obstacle_impact_sound = pygame.mixer.Sound('audio/obstacle-impact.wav')
scorsese_surface = scorsese_font.render("SCORSESE RED", False, 'Black')
scorsese_rect = scorsese_surface.get_rect(center = (WIDTH/2, 100))
restart_surface = main_font.render("press y to play", False, 'Black')
restart_rect = scorsese_surface.get_rect(center = (WIDTH/2, 400))

player_gameover_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_gameover_surface = pygame.transform.rotozoom(player_gameover_surface, 0, 2) # scale the player, at 0 angle, 2x scale
player_gameover_rect = player_gameover_surface.get_rect(midbottom = (500, 400))



##################
# SPRITE CLASSES #
##################

class Player(pygame.sprite.Sprite):
    def __init__(self, ground=GROUND) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.walk = [player_walk_1, player_walk_2]
        self.walk_index = 0 # represents which surface will be shown for the walk animation
        self.jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(.2)

        self.image = self.walk[self.walk_index]
        self.rect = self.image.get_rect(midbottom = (80, GROUND))
        self.gravity = 0


    def player_input(self):
        '''player_input() takes what is pressed and saves that as keys, of type list.
        The list is checked to see if the spacebar is there and if the player is grounded.
        If both are true, gravity changes and the jump happens.
        By checking for the ground, we prevent more than a single jump.'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=GROUND:
            self.jump_sound.play()
            self.gravity = -18

    def apply_gravity(self):
        '''When the player is above the ground, the gravity becomes -18 as set in the player_input method.
        This method increases the gravity, emulating a faster falling to the ground....gravity.
        We also check to make sure that the player cannot fall through the ground.'''
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND: self.rect.bottom = GROUND

    def player_animation(self):
        '''Used to animate the player. Will be wakling if grounded, otherwise jumping.
        .1->.9 cast as an int to 0. 1 to 1.9 cast to 1.
        so we reset the index back to 0 when it hits a length longer than the number of walk animations avaialble'''
        if self.rect.bottom == GROUND:
            self.walk_index += 0.1
            if self.walk_index > len(self.walk):
                self.walk_index = 0
            self.image = self.walk[int(self.walk_index)]
        # play jumping if not on floor
        else:
            self.image = self.jump

    def update(self):
        '''The update method called by the main game loop. Anything we want to run each frame goes in here.'''
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type, ground=GROUND):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.movement_speed = 10
            y_pos = 310
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.movement_speed = 5
            y_pos = GROUND

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def obstacle_animation(self):
        '''The animations of the obstacles. If the type is a fly, the animations will run 4 times faster to make it look like flapping windows.'''
        if type == "fly":
            self.animation_index += .2
        else:
            self.animation_index += .1

        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def self_desctruction(self):
        '''self destruction...heh'''
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.obstacle_animation()
        self.rect.x -= self.movement_speed
        self.self_desctruction()



##########
# GROUPS #
##########

## group single for player
player = pygame.sprite.GroupSingle()
player.add(Player())

## group many for obstacles
# since this is a group, we need to add members elsewhere.
# we will use the game loop to add them where we were adding them to the obstacle list before
obstacle_group = pygame.sprite.Group()



##########
# TIMERS #
##########

# timers
## there are pygame reserved events, so to avoid overlapping, we add a +1 to the event
obstacle_timer = pygame.USEREVENT + 1
snail_timer = pygame.USEREVENT + 2
fly_timer = pygame.USEREVENT + 3

# triggers event in certain intervals
# https://www.pygame.org/docs/ref/time.html?highlight=set_timer#pygame.time.set_timer
pygame.time.set_timer(obstacle_timer, 1400) # triggered event, often to trigger in ms




#############
# FUNCTIONS #
#############

def collision_sprite():
    '''Checks to see if the player sprite collides with any member of the obstacle group.
    If it collides, then the obstacle member would be delete or not depending on the bool.
    The obstacle group is also purged upon collision so when the game restarts, the player starts with a blank screen.
    This returns a list. So we are going to check to see if there is anything in the list and return True/False accordingly.
    False if there is something in the list, True if not. This will be what informs game_active if the game should continue.'''
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        obstacle_impact_sound.play()
        return False
    else: return True

def get_score():
    current_time = int(pygame.time.get_ticks() /  1000) - start_time
    score_surface = main_font.render(f"Score: {current_time}", False, 'Black')
    score_rect = score_surface.get_rect(center = (WIDTH/2, 50))
    screen.blit(score_surface, score_rect)
    return current_time



#############
# GAME LOOP #
#############

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
        else:
            if event.type == obstacle_timer:
                # using choice, we can have weighted results on the frequency of spawned obstacles
                obstacle_group.add(Obstacles(choice(["snail", "snail", "snail", "fly"])))

    if game_active:
    # pygame will lay out the surfaces in the order you call them. so we have the ground overlaying the sky
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0, GROUND))
        # screen.blit(score_surface, score_rect) # replacing with a score timer
        score = get_score()

        player.draw(screen) # draw method was inherited from pygame.sprite.Sprite. screen is just the name of the surface to be drawn on.
        player.update() # what we run each frame to account for gravity and check for player input. better than calling each method one by one

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision Detection
        game_active = collision_sprite()

    else:
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
