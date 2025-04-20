import sys
import pygame
from menu import Menu
from game import Game
from game_stats import GameStats
from over import GameOverScreen
from tutorial import Tutorial
from settings import Settings

class AlienInvasion:
    """Main class to manage game and its behavior."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Create screen
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height), pygame.RESIZABLE)
        pygame.display.set_icon(self.settings.icon)
        pygame.display.set_caption(self.settings.caption)

        # Initial game state
        self.state = "menu"
        self.fullscreen = False

        # Initialize state classes
        self.menu = Menu(self)
        self.game = Game(self)
        self.tutorial = Tutorial(self)
        self.over = GameOverScreen(self)
        self.game_stats = GameStats(self)

        # Background resize + position UI
        self._resize()

        # Music
        if self.settings.sound_on:
            try:
                pygame.mixer.init()
                pygame.mixer.music.play(-1, 0)
            except pygame.error:
                print("Error initializing sound system.")

    def _resize(self):
        self.settings.width, self.settings.height = self.screen.get_size()

        self.settings.old_width = self.settings.width
        self.settings.old_height = self.settings.height


        self.settings.background = pygame.transform.scale(
            self.settings.background, (self.settings.width, self.settings.height)
        )

        self.settings.sound_rect.topleft = (self.settings.width - 180, 20)
        self.settings.help_rect.topleft = (self.settings.width - 90, 20)
        self.settings.title_rect.center = (self.settings.width // 2, self.settings.height // 2.5)
        self.settings.play_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 165)

        if hasattr(self, 'game') and hasattr(self.game, 'ship'):
            self.game.ship.screen = self.screen
            self.game.ship.center_ship()

        if self.state == "game":
            width_ratio = self.settings.width / self.settings.old_width
            height_ratio = self.settings.height / self.settings.old_height

            for alien in self.game.aliens:
                alien.rect.x = int(alien.rect.x * width_ratio)
                alien.rect.y = int(alien.rect.y * height_ratio)
                alien.x = float(alien.rect.x)
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.settings.width, self.settings.height = event.w, event.h
                self._resize()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                elif event.key == pygame.K_RETURN and self.state == "menu":
                    self.state = "game"
                else:
                    self._handle_state_events(event)

            elif event.type == pygame.KEYUP:
                self._handle_state_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_state_events(self, event):
        if self.state == "menu":
            self.menu.handle_events(event)
        elif self.state == "game":
            self.game.handle_events(event)
        elif self.state == "tutorial":
            self.tutorial.handle_events(event)
        elif self.state == "game_over":
            self.over.handle_events(event)

    def _handle_mouse_click(self, event):
        if self.settings.play_rect.collidepoint(event.pos):
            self.start_new_game()  
        elif self.settings.sound_rect.collidepoint(event.pos):
            self._toggle_sound()
        elif self.settings.help_rect.collidepoint(event.pos):
            if self.state != "tutorial":
                self.previous_state = self.state
                self.state = "tutorial"
            elif hasattr(self, 'previous_state'):
                self.state = self.previous_state
        else:
            self._handle_state_events(event)

    def _toggle_sound(self):
        self.settings.sound_on = not self.settings.sound_on
        if pygame.mixer.get_init():
            if self.settings.sound_on:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        self._redraw_screen()

    def _redraw_screen(self):
        """Redraw the screen and update UI elements."""
        # score = self.game_stats.score
        # high_score = self.game_stats.high_score
        if self.state == "menu":
            self.menu.draw_menu()
        elif self.state == "game":
            self.game.draw_game()
        elif self.state == "tutorial":
            self.tutorial.draw_tutorial()
        elif self.state == "game_over":
            self.over.draw()

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.settings.width, self.settings.height), pygame.RESIZABLE)
        self._resize()

    def start_new_game(self):
        self.game_stats.reset_stats()
        self.game = Game(self)
        self._resize() 
        self.state = "game"

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()
            self._redraw_screen()
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
