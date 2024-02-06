import pygame
from sys import exit

# needed to get pygame going. lots of complicated stuff goes down here that we don't need to worry about for now
pygame.init()

# create a display surface that the player will see when the game loads up. we store this in a variable usually called screen.
# we pass in a tuple that determines the height and width of the window
# screen = pygame.display.set_mode((width,height))

# when we run the below code, it will load a window for a single frame and close
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("TITLE GOES HURRR")

clock = pygame.time.Clock()

# display a surface
test_surface = pygame.Surface((100, 200))
test_surface.fill('Red') #give it color so you can see the surface.


# to keep your window open, we need to have it run forever....so a while true loop.

while True:
    # draw all elements
    # update everything

    #
    # this will update the display surface defined above. without anything else in the code, if we were to run this
    # the window would stay open forever without the player being able to close it. we need to enable player control.
    # we create an event loop to check what is going on...
#    pygame.display.update()

    # for event in pygame.event.get():
    #     # the X ont the window is pygame.QUIT. so if that is pressed, we exit the display surface.
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    # pygame.display.update()

# when you run this, and exit, you will get an error:
#     pygame 2.5.2 (SDL 2.28.3, Python 3.11.7)
# Hello from the pygame community. https://www.pygame.org/contribute.html
# Traceback (most recent call last):
#   File "/Users/sd/dev/python/learning/pygame/ultimate-intro/test.py", line 29, in <module>
#     pygame.display.update()
# pygame.error: video system not initialized

# This is because we are calling pygame.QUIT, which terminates the display surface. but we then continue down
# the code to the pygame.display.update() call and that is where we are getting the pygame.error handle.

# so we add "exit()" after pygame.quit(), and add the sys import to access exit(). This forces the exit of the while
# loop and makes it so pygame never raches the display.update() call. Running the code with exit() and there are no errors. yay.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # block image transfer: blit. fancy way to say you are going to place one surface on another surface
    # screen.blit(surface, position)
    screen.blit(test_surface, (0,0))
    screen.blit(test_surface, (200, 100)) # 200px from left, 100px from the top. 0,0 is top left corner

    pygame.display.update()
    # tells pygame that the while loop should not run faster than 60 times per second...
    # and now we have our max framerate capped at 60fps :)
    clock.tick(60)
