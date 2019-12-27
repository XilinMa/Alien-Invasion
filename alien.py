import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen):
        """alien initialization and set initial location"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load alien image and get its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # put alien on left top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # alien location
        self.x = float(self.rect.x)

    def check_edges(self):
        """if aliens are out of vision return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """move aliens right or left"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """display alien in certain location"""
        self.screen.blit(self.image, self.rect)
