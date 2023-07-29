# Import the pygame module
import pygame

# Import random for random numbers
import random



# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



pygame.display.set_caption('Du Game')
Icon = pygame.image.load('bondu.png')
pygame.display.set_icon(Icon)
# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Eddie(pygame.sprite.Sprite):
    def __init__(self):
        super(Eddie, self).__init__()
        self.surf = pygame.image.load("eddie.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypressesww
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Bondu(pygame.sprite.Sprite):
    def __init__(self):
        super(Bondu, self).__init__()
        self.surf = pygame.image.load("bondu.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
# class Cloud(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Cloud, self).__init__()
#         self.surf = pygame.image.load("cloud.png").convert()
#         self.surf.set_colorkey((0, 0, 0), RLEACCEL)
#         # The starting position is randomly generated
#         self.rect = self.surf.get_rect(
#             center=(
#                 random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
#                 random.randint(0, SCREEN_HEIGHT),
#             )
#         )

#     # Move the cloud based on a constant speed
#     # Remove it when it passes the left edge of the screen
#     def update(self):
#         self.rect.move_ip(-5, 0)
#         if self.rect.right < 0:
#             self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()


pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops=-1)

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDBONDU = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBONDU, 543)

# Create our 'player'
eddie = Eddie()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
bondu = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(eddie)



running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDBONDU:
            # Create the new enemy, and add it to our sprite groups
            new_bondu = Bondu()
            bondu.add(new_bondu)
            all_sprites.add(new_bondu)


    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    eddie.update(pressed_keys)

    # Update the position of our enemies and clouds
    bondu.update()

    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(eddie, bondu):
        # If so, remove the players
        eddie.kill()
        eddie = Eddie()
        all_sprites.add(eddie)
    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(30)
# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()