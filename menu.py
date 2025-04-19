import pygame

class Menu:
    def __init__(self, game):
        """Initialize menu settings."""
        self.game = game  # Reference to the main game instance
        self.settings = game.settings
        self.screen = game.screen

    def draw_menu(self):
        """Draw the main menu of the game."""
        # Draw the background
        self.screen.blit(self.settings.background, (0, 0))

        # Draw the sound icon
        sound_icon = self.settings.sound_icon_on if self.settings.sound_on else self.settings.sound_icon_off
        self.screen.blit(sound_icon, self.settings.sound_rect)

        # Draw the help icon
        self.screen.blit(self.settings.help_icon, self.settings.help_rect)

        # Draw the title
        self.screen.blit(self.settings.title, self.settings.title_rect)

        # Draw the Play button with hover effect
        if self.settings.play_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, self.settings.GREEN, self.settings.play_rect, 3)  # Thicker border when hovered
        else:
            pygame.draw.rect(self.screen, self.settings.GREEN, self.settings.play_rect, 2)  # Normal border

        # Initialize font
        font = pygame.font.Font(None, 55)
        play_text = font.render("PLAY", True, self.settings.GREEN)

        # Center the text within the button
        text_x = self.settings.play_rect.centerx - (play_text.get_width() // 2)
        text_y = self.settings.play_rect.centery - (play_text.get_height() // 2)

        # Draw Play text
        self.screen.blit(play_text, (text_x, text_y))

    def handle_events(self, event):
        """Handle menu events (button clicks)."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.settings.play_rect.collidepoint(event.pos):
                self.game.previous_state = "menu"
                self.game.start_new_game()  # Start a new game
                self.game.state = "game" # Switch to game screen
            elif self.settings.help_rect.collidepoint(event.pos):  # Help button clicked
                self.game.previous_state = "menu"
                self.game.state = "tutorial"  # Switch to tutorial
