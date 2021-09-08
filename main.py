import pygame
import time
from pygame import mixer
from levels import Level
from button import Button
from TileTypes import Enemy, Spike, Door, MovingPlatform

# initializing things
mixer.init()
pygame.init()
clock = pygame.time.Clock()

# establishing variables
tile_size = 25
player_size = 40
main_menu = True
screen_width = 800
screen_height = 600
current_level = 1

# screen stuff
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Platformer!")

# loading sounds
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.set_volume(.1)
jump_noise = pygame.mixer.Sound("sounds/jump.wav")
jump_noise.set_volume(0.1)
meow_noise = pygame.mixer.Sound("sounds/spike_death.mp3")
meow_noise.set_volume(0.3)
rat_noise = pygame.mixer.Sound("sounds/rat_death.wav")
rat_noise.set_volume(1)
victory_noise = pygame.mixer.Sound("sounds/victory.wav")
victory_noise.set_volume(0.3)
button_noise = pygame.mixer.Sound("sounds/buttonclick.wav")
button_noise.set_volume(0.3)
final_victory_noise = pygame.mixer.Sound("sounds/final_victory.mp3")
final_victory_noise.set_volume(0.3)

# loading images
title_image = pygame.image.load("Images/title_image.png")
background = pygame.image.load("Images/city_sunset.webp")
restart_button = pygame.image.load("Images/restartbutton.xcf")
menu_button = pygame.image.load("Images/menubutton.xcf")
start_button = pygame.image.load("Images/startimage.png")
exit_button = pygame.image.load("Images/exitimage.png")
level_button = pygame.image.load("Images/levelsimage.png")
level1_button = pygame.image.load("Images/number1.xcf")
level2_button = pygame.image.load("Images/number2.xcf")
level3_button = pygame.image.load("Images/number3.xcf")
level4_button = pygame.image.load("Images/number4.xcf")
level5_button = pygame.image.load("Images/number5.xcf")
level6_button = pygame.image.load("Images/number6.xcf")
level7_button = pygame.image.load("Images/number7.xcf")
level8_button = pygame.image.load("Images/number8.xcf")
level9_button = pygame.image.load("Images/number9.xcf")


# resets level
def reset_level(level):
    player.reset(0, screen_height - 200)
    enemy_group.empty()
    spike_group.empty()
    door_group.empty()
    platform_group.empty()


class Sprite:
    def __init__(self, x, y):
        self.reset(x, y)
        # creating rest below for the purpose of reset

    def update(self, game_over):
        # variables for movement/animation/collision
        dx = 0
        dy = 0
        walk_cooldown = 5
        collision_thresh = 26

        if game_over == 0:
            # key presses for player movement
            key = pygame.key.get_pressed()

            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
                if self.rect.x < 0:
                    dx = 0
            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
                if self.rect.x > screen_width - 50:
                    dx = 0
            if key[pygame.K_w] and self.jumped == False:
                jump_noise.play()
                self.vel_y = -13
                self.jumped = True
            if key[pygame.K_w] == False:
                self.jumped = False
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                # if direction was left or right last, leave player facing corresponding direction
                self.image = self.images_right[self.index]
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel = 10
            dy += self.vel_y

            # check for collision
            for tile in world.tile_list:
                # x axis collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y axis collisions
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # check for enemy collision
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
                rat_noise.play()
            # check for spike collision
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1
                meow_noise.play()

            # check for door collision
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1
                victory_noise.play()
            # check for moving platform collision
            for platform in platform_group:
                # x collision
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y collision
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < collision_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collision_thresh:
                        self.vel_y = 0
                        dy = 0
                        self.rect.bottom = platform.rect.top
                        self.jumped = False
                        if platform.move_y != 0:
                            self.rect.bottom = platform.rect.top - 1

                    # move sideways with platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

                if self.vel_y < 0 or self.vel_y > 0:
                    self.jumped = True
                elif self.vel_y == 0 and self.collide == True:
                    self.jumped = False

            # checking if jumping
            if self.vel_y < 0 or self.vel_y > 0:
                self.jumped = True
            elif self.vel_y == 0 and self.collide == True:
                self.jumped = False

            # update player cords
            self.rect.x += dx
            self.rect.y += dy

            # sprite walking animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

        # makes player turn in to ghost on death
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 0:
                self.rect.y -=5

        screen.blit(self.image, self.rect)
        return game_over

    # sets initial position of sprite for level
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"Images/sprite{num}.xcf")
            img_right = pygame.transform.scale(img_right, (player_size, player_size))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load("Images/ghost.xcf")
        self.image = self.images_right[self.index]
        self.sprite = pygame.image.load("Images/sprite1.xcf")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.collide = False


class World():
    def __init__(self, data):
        self.tile_list = []

        floor_img = pygame.image.load("Images/platform.xcf")

        row_count = 0
        # checking which tile is where, and adding those tiles to its respective group
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = column_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    enemy = Enemy(column_count * tile_size, row_count * tile_size - 3)
                    enemy_group.add(enemy)
                if tile == 3:
                    spikes = Spike(column_count * tile_size, row_count * tile_size, 1)
                    spike_group.add(spikes)
                if tile == 4:
                    door = Door(column_count * tile_size, row_count * tile_size - 24)
                    door_group.add(door)
                if tile == 5:
                    platform = MovingPlatform(column_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 6:
                    platform = MovingPlatform(column_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 7:
                    spikes = Spike(column_count * tile_size, row_count * tile_size, -1)
                    spike_group.add(spikes)
                column_count += 1
            row_count += 1

    # drawing the tiles
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# making instances of classes/groups
level = Level(1)
player = Sprite(0, screen_height - 200)
enemy_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
world = World(level.get_level())
restart = Button(70, 10, restart_button)
menu = Button(10, 10, menu_button)
start = Button(297, 300, start_button)
exit = Button(323, 500, exit_button)
levels = Button(280, 400, level_button)
level_1 = Button(10, 275, level1_button)
level_2 = Button(100, 275, level2_button)
level_3 = Button(190, 275, level3_button)
level_4 = Button(280, 275, level4_button)
level_5 = Button(370, 275, level5_button)
level_6 = Button(460, 275, level6_button)
level_7 = Button(550, 275, level7_button)
level_8 = Button(640, 275, level8_button)
level_9 = Button(730, 275, level9_button)

game_over = False
level_select = False


# stuff for splash screen
time_final = time.time()
splash_screen = 0
played_sound = False

# executing splash screen
while splash_screen < 150:
    dt = time.time() - time_final
    dt *= 60
    time_final = time.time()
    splash_screen += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if played_sound == False:
        victory_noise.play()
        played_sound = True
    background = pygame.image.load("Images/city_sunset.webp")
    myname = pygame.image.load("Images/myname.png")
    screen.blit(background, (0, 0))
    screen.blit(myname, (screen.get_width() / 2 - myname.get_width() / 2, screen.get_height() / 2 - myname.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(10)

pygame.mixer.music.play(-1)

run = True
while run:

    # lock at 60 fps
    clock.tick(60)

    #draw background
    screen.blit(background, (0, 0))

    # establishing main menu actions
    if main_menu == True:
        current_level = 1
        screen.blit(title_image, (125, 50))
        if exit.draw():
            run = False
        if start.draw():
            reset_level(level)
            current_level = 1
            level = Level(1)
            world = World(level.get_level())
            button_noise.play()

            main_menu = False
            game_over = 0
        # level select button
        if levels.draw():
            level_select = True
            main_menu = False
            button_noise.play()

    # establishing level select actions
    if main_menu == False and level_select == True:
        # menu select button
        if menu.draw():
            reset_level(level)
            main_menu = True
            level_select = False
            button_noise.play()
        # all the level buttons in level selector
        if level_1.draw():
            reset_level(level)
            level = Level(1)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_2.draw():
            current_level = 2
            reset_level(level)
            level = Level(2)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_3.draw():
            current_level = 3
            reset_level(level)
            level = Level(3)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_4.draw():
            current_level = 4
            reset_level(level)
            level = Level(4)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_5.draw():
            current_level = 5
            reset_level(level)
            level = Level(5)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_6.draw():
            current_level = 6
            reset_level(level)
            level = Level(6)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_7.draw():
            current_level = 7
            reset_level(level)
            level = Level(7)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_8.draw():
            current_level = 8
            reset_level(level)
            level = Level(8)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

        if level_9.draw():
            current_level = 9
            reset_level(level)
            level = Level(9)
            world = World(level.get_level())
            main_menu = False
            level_select = False
            game_over = 0
            button_noise.play()

    # start of game
    if main_menu == False and level_select == False:

        world.draw()

        # game not over, nor won
        if game_over == 0:
            enemy_group.update()
            platform_group.update()
            if menu.draw():
                main_menu = True
                game_over = 0
                player.reset(0, screen_height - 200)
                button_noise.play()

        enemy_group.draw(screen)
        spike_group.draw(screen)
        door_group.draw(screen)
        platform_group.draw(screen)
        game_over = player.update(game_over)

        # game lost
        if game_over == -1:
            if restart.draw():
                player.reset(0, screen_height - 200)
                game_over = 0
                button_noise.play()

            if menu.draw():
                main_menu = True
                player.reset(0, screen_height - 200)
                game_over = 0
                button_noise.play()

        # level complete
        if game_over == 1:
            current_level += 1
            # if they complete a level, and theres another it will send them there
            if current_level <= 9:
                reset_level(level)
                level = Level(current_level)
                world = World(level.get_level())
                game_over = 0
            else:
                # making a win message if person completes all levels, sends them back to menu after
                victory_noise.stop()
                pygame.mixer.music.pause()
                final_victory_noise.play()
                time_final = time.time()
                win_screen = 0
                while win_screen < 350:
                    dt = time.time() - time_final
                    dt *= 60
                    time_final = time.time()
                    win_screen += dt

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()

                    win_message = pygame.image.load("Images/youwin.png")
                    screen.blit(win_message, (screen.get_width() / 2 - win_message.get_width() / 2, screen.get_height() / 2 - win_message.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(10)

                pygame.mixer.music.unpause()
                main_menu = True
                game_over = False

        # closing game
        if game_over == True:
            run = False

    # closing game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # updates screen
    pygame.display.update()

pygame.quit()