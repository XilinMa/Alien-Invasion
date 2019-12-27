import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """ship initialization and set initial location"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load ship image and get external rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # put ship on the central bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # moving flag
        self.moving_right = False
        self.moving_left = False

        # int2float
        self.center = float(self.rect.centerx)

    def update(self):
        """adjust ship by moving_right flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """display ship in certain location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center ship in the screen"""
        self.center = self.screen_rect.centerx
