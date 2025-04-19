import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """ A class to manage bullets fired by aliens (straight downward). """

    def __init__(self, game, alien, ship=None):  # ship is unused now
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = (255, 0 , 0 )  # Red color for alien bullets

        # Create a bullet rect at the alien's current position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet straight down. """
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

        # Remove the bullet if it goes off the screen
        if self.rect.top >= self.settings.height:
            self.kill()

    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        pygame.draw.rect(self.screen, self.color, self.rect)
