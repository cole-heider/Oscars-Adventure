import pygame

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False

    def draw(self):
        action = False
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # check mouseover and click conditions
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                action = True
                self.click = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        # draw button
        screen.blit(self.image, self.rect)

        return action