###################################################################################
#                         Welcome to the 5M06 Operation game
# Be part of this operation to save the system from the black hat hackers that are trying to spread their pinkish viruses in the system and ruin the virtual world.
# By collecting as much as possible from the bitcoins and keys you would save the system.
#
#                                   How to play:
# - Use the arrow keys [Right, Left, Up] to move and jump. click [Up] many times to FLY!
# - Make sure to click the small box that has headphones to hear the soundeffects
#
# (C) 2022 TDRA Summer Camp. All Rights Reserved by NA4LK (Noora Alketbi_0532).
###################################################################################

# import -----------------------------------------------------
import pygame
from pygame import mixer
from pygame.locals import *

# initializing -----------------------------------------------------
pygame.mixer.pre_init(44100, -16, 2, 1024)
mixer.init()
pygame.init()

# clock and fps -----------------------------------------------------
clock = pygame.time.Clock()
fps = 60

# scale -----------------------------------------------------
width = 800
height = 500

# screen -----------------------------------------------------
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('  5M06 Operation')

#icon -------
icon = pygame.image.load ('iconrobot.png')
pygame.display.set_icon (icon)

# font -----------------------------------------------------
font = pygame.font.SysFont('pixel.ttf', 70)
font_score = pygame.font.SysFont('pixel.ttf', 20)
font_ins = pygame.font.SysFont('pixel.ttf', 20)
font1_ins = pygame.font.SysFont('pixel.ttf', 15)
font_goal = pygame.font.SysFont('pixel.ttf', 20)

# variables -----------------------------------------------------
tile_size = 30
game_over = 0
main_menu = True
current_level = 0
max_levels = 3
bitcoin_score = 0
greenkey_score = 0

# images & coclors -----------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN1 = (3, 255, 3)
GREEN2 = (4, 164, 4)
restart_img = pygame.image.load('restartbtn.png')
start_img = pygame.image.load('startbtn.png')
exit_img = pygame.image.load('exitbtn.png')
menu_img = pygame.image.load ('menubtn.png')

# sounds -----------------------------------------------------
pygame.mixer.music.load('bgmusicS.wav')
pygame.mixer.music.play (-1, 0.0, 0)

bitcoin_fx = pygame.mixer.Sound ('bitcoinS.wav')
bitcoin_fx.set_volume (0.5)

jump_fx = pygame.mixer.Sound ('jumpS.wav')
jump_fx.set_volume (0.5)

game_over_fx = pygame.mixer.Sound ('gameoverS.wav')
game_over_fx.set_volume (0.5)

greenkey_fx = pygame.mixer.Sound ('greenkeyS.wav')
greenkey_fx.set_volume (0.5)

# text draw -----------------------------------------------------
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# reset levels -----------------------------------------------------
def reset_level(level):
    player.reset(50, 360)

    hacker_group.empty()
    lava_group.empty()
    exit_group.empty()

    if current_level <= max_levels:
        world_data = levels [current_level]
    world = World(world_data)

    return world

#-------------------------------------- CLASSES --------------------------------------#


# button ------------------------------
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #mouse position -------
        pos = pygame.mouse.get_pos()

        #clicking conditions -------
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button -------
        screen.blit(self.image, self.rect)

        return action


# player ------------------------------
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:

            #pressing keys -------
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False:
                jump_fx.play()
                self.vel_y = -13
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 2
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 2
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]

            #player animation -------
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #gravity -------
            self.vel_y += 1
            if self.vel_y > 5:
                self.vel_y = 5
            dy += self.vel_y

            #collisions -------
            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y,
                                       self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy,
                                       self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #collision with enemies -------
            if pygame.sprite.spritecollide(self, hacker_group, False):
                game_over = -1
                game_over_fx.play()

            #collision with lava -------
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            #collision with lava -------
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            #update player coordinates -------
            self.rect.x += dx
            self.rect.y += dy

        #game over -------
        elif game_over == -1:
            draw_text('GAME OVER!', font, WHITE, (width // 2) - 275,
                      (height // 2) - 150)

        screen.blit(self.image, self.rect)

        return game_over

    #when clicked 'resret' . player properties -------
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'robot{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

# world ------------------------------
class World():
    def __init__(self, data):
        self.tile_list = []

        #images -------
        block_img = pygame.image.load('block.png')
        ironbrick_img = pygame.image.load('ironbrick.png')

        #creating the world, using tiles -------
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(ironbrick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    hacker = Enemy(col_count * tile_size, row_count * tile_size + 10)
                    hacker_group.add(hacker)
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    bitcoin = Bitcoin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    bitcoin_group.add(bitcoin)
                if tile == 8:
                    greenkey = Greenkey(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    greenkey_group.add(greenkey)
                if tile == 6:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# enemy ------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('hacker.png')
        self.image = pygame.transform.scale(self.image, (35, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += -3
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


# lava ------------------------------
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# bitcoin ------------------------------
class Bitcoin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('bitcoin.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# key ------
class Greenkey (pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load ('greenkey.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


# exit door ------------------------------
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#-------------------------------------------------------------------------------------#

# world data (how it's look like) -----------------------------------------------------

#level 1 -------
world_data1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 0, 7, 0, 6, 1],
               [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 7, 0, 0, 0, 2, 2, 2, 0, 0, 7, 8, 7, 0, 0, 0, 1],
               [1, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 7, 7, 0, 3, 0, 0, 0, 0, 0, 0, 0, 7, 1],
               [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 1],
               [1, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#level 2 -------
world_data2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 7, 0, 0, 0, 7, 8, 0, 0, 0, 1],
               [1, 7, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 1],
               [1, 2, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 8, 0, 0, 3, 0, 7, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 8, 1],
               [1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 3, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
               [1, 0, 0, 7, 7, 0, 0, 7, 8, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#level 3 -------
world_data3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 8, 7, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 7, 0, 7, 7, 1],
               [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 1],
               [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 2, 0, 0, 0, 0, 0, 0, 8, 7, 0, 3, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 8, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 0, 1],
               [1, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
               [1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#level 4 -------
world_data4 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 6, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 2, 2, 0, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 7, 7, 0, 3, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 1],
               [1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 1],
               [1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# player position -----------------------------------------------------
player = Player(50, 360)

# groups -----------------------------------------------------
hacker_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
bitcoin_group = pygame.sprite.Group()
greenkey_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# score bitcoin and green key -----------------------------------------------------
score_bitcoin = Bitcoin(tile_size // 2, tile_size // 2)
bitcoin_group.add(score_bitcoin)

score_greenkey = Greenkey (tile_size // 2 + 450, tile_size // 2)
greenkey_group.add (score_greenkey)

# level maps in list -----------------------------------------------------
levels = (    
    world_data1,
    world_data2,
    world_data3,
    world_data4,)

# level data and create world -------
if current_level <= max_levels:
    world_data = levels [current_level]
world = World(world_data)


# creating button -----------------------------------------------------
restart_button = Button(width // 2 - 197, height // 2 - 30, restart_img)
start_button = Button(width // 2 - 350, height // 2, start_img)
exit_button = Button(width // 2 + 150, height // 2, exit_img)
menu_button = Button(width // 2 - 197, height // 2 - 50, menu_img)

# main loop -----------------------------------------------------
run = True
while run:

    clock.tick(fps)

    #screen -------
    screen.fill('BLACK')

    #menu -------
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        #collecting coin -------
        if game_over == 0:
            hacker_group.update()
            
        if pygame.sprite.spritecollide(player, bitcoin_group, True):
            bitcoin_score += 6
            bitcoin_fx.play()
        if pygame.sprite.spritecollide(player, greenkey_group, True):
            greenkey_score += 1
            greenkey_fx.play()

        #draw text on the screen -------
        draw_text('X ' + str(bitcoin_score), font_score, WHITE, tile_size + 10, 10)
        draw_text('Use <- | -> to move. To jump use up arrow key*', font_ins, WHITE, tile_size + 100, 10)
        draw_text('*click it many times to FLY!', font1_ins, WHITE, tile_size + 0, 460)
        draw_text('X ' + str(greenkey_score), font_score, WHITE, tile_size + 460, tile_size - 20)
        draw_text ('(C) 2022 TDRA Summer Camp. All Rights Reserved by NA4LK (Noora Alketbi_0532).', font1_ins, BLACK, tile_size + 0, 485)

        ###ISSUE- keep counting### -------
        draw_text ('LEVEl: ' + str(current_level), font1_ins, WHITE, tile_size + 450, 485)


        #draw on the screen -------
        hacker_group.draw(screen)
        lava_group.draw(screen)
        bitcoin_group.draw(screen)
        greenkey_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        #-------conditions for game over -------#
        
        #player dies -------
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(current_level)
                game_over = 0
                bitcoin_score = 0

                
        #player complete level -------
        if game_over == 1:
            current_level += 1
            if current_level <= max_levels:
                world_data = []
                world = reset_level(current_level)
                game_over = 0
                draw_text('YOU WIN!', font, WHITE, (width // 2) - 250, (height // 2) - 150)

            else:
                draw_text('YOU WIN!', font, WHITE, (width // 2) - 250, (height // 2) - 150)
                draw_text('you have saved the system.', font_goal, WHITE, (width // 2) - 230, (height // 2) + 50)
                draw_text('by ' + str(bitcoin_score) + ' Bitcoin', font_goal, WHITE, (width // 2) - 200, (height // 2) + 70)
                draw_text('and ' + str(greenkey_score) + ' Green Keys', font_goal, WHITE, (width // 2) - 200, (height // 2) + 90)
                if menu_button.draw():
                    main_menu = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()




