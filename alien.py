from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, game, alien_type="blue"):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.alien_type = alien_type

        # Set image based on alien type
        if alien_type == "green":
            self.image = self.settings.green_alien_image
        elif alien_type == "red":
            self.image = self.settings.red_alien_image
        else:
            self.image = self.settings.blue_alien_image


        # Load the alien image and set its rect attribute
        # self.image = self.settings.image 
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

