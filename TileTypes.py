import pygame

tile_size = 25


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Images/platform.xcf")
        self.image = pygame.transform.scale(img, (26, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    # moves platform left and right
    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if self.move_counter > 25:
            self.move_direction *= -1
            self.move_counter *= -1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/enemy.xcf")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    # moves the enemy character left and right
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 25:
            self.move_direction *= -1
            self.move_counter *= -1
            self.image = pygame.transform.flip(self.image, True, False)


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/spikes.xcf")
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.direction = direction
        if direction == -1:
            self.image = pygame.transform.flip(self.image, False, True)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/door.xcf")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y