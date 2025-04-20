import pygame 

class Settings:
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's settings."""
        pygame.init()

        # Colors
        self.GREEN = (0, 255, 0)

         # Get screen size
        info = pygame.display.Info()
        self.width, self.height = int(info.current_w * 0.75), int(info.current_h * 0.75)  

         # Icons & Background & Caption
        self.icon = pygame.image.load("images/icon.jpg")
        self.background = pygame.image.load("images/background.jpg")
        self.caption = "Alien Invasion"

        # Title setting
        self.title = pygame.image.load("images/Title.png")
        self.title_rect = self.title.get_rect(center=(self.width // 2, self.height // 2.5))

        # Button setting
        self.play_rect = pygame.Rect(self.width // 2 - 75 , self.height // 2 + 150, 180, 60) # left top width height 

        # icon size 
        self.icon_size =  (70, 70)

        # Sound settings
        self.sound_icon_on = pygame.transform.scale(pygame.image.load("images/volume.png"), self.icon_size )
        self.sound_icon_off = pygame.transform.scale(pygame.image.load("images/mute.png"), self.icon_size )
        self.sound_rect = self.sound_icon_on.get_rect(topleft=(self.width - 180, self.height - 90))

        self.sound_on = True  # Sound is on by default  
        pygame.mixer.music.load("images/audio.mp3")  

        # help settings 
        self.help_icon = pygame.transform.scale(pygame.image.load("images/help.png"), self.icon_size)
        self.back_icon = pygame.transform.scale(pygame.image.load("images/back.png"), self.icon_size)
        self.help_rect = self.help_icon.get_rect(topleft=(self.width - 90, self.height - 90))


        # ship setting 
        self.ship = pygame.transform.scale(pygame.image.load("images/ship.png"), (70, 70))
        self.ship_speed = 3.0

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 0)
        self.bullets_allowed = 6

        # icon size 
        self.alien_size =  (52, 52)

        # Alien settings
        self.green_alien_image = pygame.transform.scale(pygame.image.load("images/green.png"),  self.alien_size)
        self.red_alien_image =  pygame.transform.scale(pygame.image.load("images/red.png"),  self.alien_size)
        self.blue_alien_image =  pygame.transform.scale(pygame.image.load("images/blue.png"),  self.alien_size)
        self.alien_speed = 2.0
        self.fleet_drop_speed = 30
        self.fleet_direction = 1
        self.alien_shoot_interval = 2000  # milliseconds
        self.alien_bullet_speed = 2.0

        # Game settings
        self.ship_hit = False
        self.ship_hit_time = None
        self.pause_duration = 1000  # 2 seconds pause
        self.game_paused = False
        self.aliens_paused = False  # 2 seconds pause for aliens

        self.score = 0
        self.high_score = 0  