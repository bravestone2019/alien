import pygame

class GameOverScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 30)

        self.large_font = pygame.font.Font(None, 98)

        # Buttons
        self.home_button = pygame.Rect(0, 0, 200, 50)
        self.restart_button = pygame.Rect(0, 0, 200, 50)

    def draw(self, score, high_score):
        self.screen.blit(self.settings.background, (0, 0))

        game_over_text = self.large_font.render("GAME OVER", True, (0, 255, 0))
        score_text = self.button_font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = self.button_font.render(f"High Score: {high_score}", True, (255, 255, 255))

        self.screen.blit(game_over_text, game_over_text.get_rect(center=(self.settings.width // 2, self.settings.height // 2 - 100)))
        self.screen.blit(score_text, score_text.get_rect(center=(self.settings.width // 2, self.settings.height // 2)))
        self.screen.blit(high_score_text, high_score_text.get_rect(center=(self.settings.width // 2, self.settings.height // 2 + 40)))

        self.home_button.center = (self.settings.width // 2 - 150, self.settings.height // 2 + 120)
        self.restart_button.center = (self.settings.width // 2 + 150, self.settings.height // 2 + 120)

         # Add hover effect by changing button color
        if self.home_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, (0, 255, 0), self.home_button, 3)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.home_button, 2)

        if self.restart_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, (0, 255, 0), self.restart_button, 3)
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), self.restart_button, 2)

        home_text = self.button_font.render("HOME", True, (0, 255, 0))
        restart_text = self.button_font.render("RESTART", True, (0, 255, 0))

        self.screen.blit(home_text, home_text.get_rect(center=self.home_button.center))
        self.screen.blit(restart_text, restart_text.get_rect(center=self.restart_button.center))

    def handle_events(self, event):
         if event.type == pygame.MOUSEBUTTONDOWN:
            if self.home_button.collidepoint(event.pos):
                self.game.state = "menu"  # Switch to menu state
            elif self.restart_button.collidepoint(event.pos):
                self.game.start_new_game()  # Restart the game
