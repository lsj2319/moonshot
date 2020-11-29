# using pygame to create a sidescroller game moon_dog_frisbee.py based on a tutorial by Christopher Baily from realpython.com
# artwork, including background and sprite images are created by me (Lee Jordan) and under Creative Commons fair use for non-commercial districution.
import pygame, sys

from pygame.locals import (
    RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT,
)

import pygame.freetype

import random

#SCREEN CONSTANTS for width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1800
# hoist the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
lightgray = (242, 241, 241)
green = (88, 181, 130)
darkgray = (169, 169, 169)

#load the background for the game
bg = pygame.image.load("images/background.png")

# extend pygame sprite to create a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.score = 0
        self.surf = pygame.image.load("images/dog.png").convert()
        #used a white background for the png, need to use convert alpha next time.
        self.surf.set_colorkey(white, RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# keep player on the screen
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <=0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# create enemy objects
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # enemy size
        self.surf = pygame.image.load("images/small-space-frisbee.png").convert()
        self.surf.set_colorkey(white, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    #move the enemy sprite and remove it when it passed off edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right <0:
            self.kill()



pygame.init()

#screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# Game On Screen Title Text
title_obj = pygame.font.Font('freesansbold.ttf', 48)
title_surface_obj = title_obj.render('Moon Dog Frisbee', True, white)
title_rect_obj = title_surface_obj.get_rect()
title_rect_obj.center = (400, 30)

# text setting success message
font_obj = pygame.font.Font('freesansbold.ttf', 32)
text_surface_obj = font_obj.render('You Caught a Space Frisbee!', True, red)
text_rect_obj = text_surface_obj.get_rect()
text_rect_obj.center = (400, 500)

# text for score message
score_value = 0
score_obj = pygame.font.Font('freesansbold.ttf', 21)
scoreX = 650
scoreY = 50

def show_score(x,y):
    score = score_obj.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# create the player
player = Player()
# create groups for the enemy sprites and manage other sprites in game
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# game loop
running = True
while running:
    # look at every event...
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # What key?
            if event.key == K_ESCAPE:
                running = False


        elif  event.type ==   QUIT:
                running = False

        elif event.type == ADDENEMY:
            #create enemy and add
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed() # boolean return of keys pressed
    player.update(pressed_keys)
    enemies.update()



    # fill background with a color
    screen.fill((0,0,0))
    screen.blit(bg, (0, 0))
    screen.blit(title_surface_obj, title_rect_obj)
    show_score(scoreX, scoreY)

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        #screen.blit(player.surf, (600,600))

    #check if enemies collide with player
    if pygame.sprite.spritecollideany(player, enemies):
        #player.kill()
        #enemy.kill()
        screen.blit(text_surface_obj, text_rect_obj)
        #player.score +=1
        score_value = score_value + 1
        #running = False

    pygame.display.flip()

pygame.quit()
