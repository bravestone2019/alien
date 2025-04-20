import pygame
class Ship:
    """ A  class to manage the ship. """

    def __init__(self, game):
        """ Initialize the ship and set its starting position. """
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # Load the ship image and get its rect.
        self.rect = self.settings.ship.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag: start with a ship that is not moving.
        self.moving_right = False
        self.moving_left = False

        self.visible = True  # Flag to control ship visibility

    def update(self):
        """ Update the ship's position based on the movement flag. """
        screen_rect = self.screen.get_rect()
        if self.moving_right and self.rect.right < screen_rect.right:
            # Update the ship's x value, not the rect.
            self.x += self.settings.ship_speed 
        # if self.moving_left:
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def center_ship(self):
        """Re-center the ship after resize or restart"""
        # self.rect.midbottom = (self.settings.width // 4, self.settings.height - 20)
        
        screen_rect = self.screen.get_rect()
        self.rect.midbottom = screen_rect.midbottom
        self.rect.y -= 20  # Give a little margin above the bottom

        self.x = float(self.rect.x)


    def blitme(self):
        """ Draw the ship at its current location. """
        if self.visible:
            self.screen.blit(self.settings.ship, self.rect)

    def move_with_mouse(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x

        # Keep ship inside screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.settings.width:
            self.rect.right = self.settings.width

