
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
        # if self.moving_right:
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.x += 1
            # Update the ship's x value, not the rect.
            self.x += self.settings.ship_speed 
        # if self.moving_left:
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    # def center_ship(self):
    #     """Center the ship on the screen."""
    #     self.rect.midbottom = self.screen.get_rect().midbottom
    #     self.x = float(self.rect.x)   

    def blitme(self):
        """ Draw the ship at its current location. """
        if self.visible:
            self.screen.blit(self.settings.ship, self.rect)
        # Uncomment the following line if you want to control visibility with a flag
        # self.image = self.settings.ship if self.visible else None

        # if self.visible:
        #     self.screen.blit(self.image, self.rect)
