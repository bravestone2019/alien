import pygame

class GameStats:
    def __init__(self, game):
        """Initialize statistics."""
        self.game = game
        self.settings = game.settings
        self.reset_stats()
        self.heart_full = pygame.image.load("images/Full.png")
        self.heart_empty = pygame.image.load("images/empty.png")

    def reset_stats(self):
        self.lives = 3
        self.score = self.settings.score

    def show_stats(self, screen):
        screen = pygame.display.get_surface()
        # Draw "Lives" text with larger font and aligned with hearts
        large_font = pygame.font.Font(None, 52)  # Larger font size
        lives_text = large_font.render("Lives:", True, (170, 170, 255))
        screen.blit(lives_text, (10, self.heart_full.get_height() // 2))

        # Draw lives
        text_width = lives_text.get_width()
        for i in range(3):
            x_position = 10 + text_width + 10 + i * (self.heart_full.get_width() + 5)
            if i < self.lives:
                screen.blit(self.heart_full, (x_position, 15))
            else:
                screen.blit(self.heart_empty, (x_position, 15))

        # Draw score
        score_text =  large_font.render(f"Score: {self.score}", True, (170, 170, 255))
        screen.blit(score_text, ((screen.get_width() - score_text.get_width()) // 2 + 20, 32))
