import pygame 

class Tutorial:
    def __init__(self, game):
        """Initialize the tutorial screen."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

    def draw_tutorial(self):
        """Draw the tutorial screen."""
        self.screen.blit(self.settings.background, (0, 0))  # Tutorial content

        # Draw a separate dark section for the tutorial content
        tutorial_rect = pygame.Rect(50, 120, self.settings.width - 100, self.settings.height - 200)
        pygame.draw.rect(self.screen, (10, 10, 30), tutorial_rect)  # Dark blue section


        # Draw tutorial text
        font = pygame.font.Font(None, 65)  # Default font, size 48
        title_text = font.render("TUTORIAL", True, self.settings.GREEN)  # Green text
        self.screen.blit(title_text, (self.settings.width // 2 - title_text.get_width() // 2, 150))


        # Option 1
        subfont = pygame.font.Font(None, 50)
        option1_text = subfont.render("Option 1", True, (255, 200, 50))
        self.screen.blit(option1_text, (self.settings.width // 2 - option1_text.get_width() // 2, 220))

        option1_desc = subfont.render("Arrow keys or [A-D] to move. Spacebar to shoot.", True, (200, 200, 200))
        self.screen.blit(option1_desc, (self.settings.width // 2 - option1_desc.get_width() // 2, 270))

        # Option 2
        option2_text = subfont.render("Option 2", True, (255, 200, 50))
        self.screen.blit(option2_text, (self.settings.width // 2 - option2_text.get_width() // 2, 340))

        option2_desc = subfont.render("Click and Drag to move. Spacebar to shoot.", True, (200, 200, 200))
        self.screen.blit(option2_desc, (self.settings.width // 2 - option2_desc.get_width() // 2, 390))

        # Draw spaceship image
        spaceship_img = self.settings.ship
        self.screen.blit(spaceship_img, (self.settings.width // 2 - spaceship_img.get_width() // 2, 420))

        # Draw Back button
        self.screen.blit(self.settings.back_icon, self.settings.help_rect)

    def handle_events(self, event):
        """Handle tutorial screen events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.settings.help_rect.collidepoint(event.pos):
                self.game.state = self.game.previous_state  # Return to previous screen