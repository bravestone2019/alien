import pygame
import random
from game_stats import GameStats
from over import GameOverScreen
from ship import Ship
from bullets import Bullet
from alien import Alien
from alien_bullet import AlienBullet

class Game:
    def __init__(self, game):
        """Initialize the game screen and game objects."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        self.game_stats = GameStats(self)

        self.ship_hit_time = None
        self.hit_pause_duration = 1500  # milliseconds
        self.ship_visible = True
        self.aliens_paused = False
        self.last_alien_shot_time = pygame.time.get_ticks()
        self.alien_shoot_interval = self.settings.alien_shoot_interval
        self.fleet_respawn_time = None
        self.respawn_delay = 1000  # 1 second in milliseconds

        self.game_over_screen = GameOverScreen(self)

        self._create_fleet()

    def draw_game(self):
        self.screen.blit(self.settings.background, (0, 0))

        # Draw icons
        sound_icon = self.settings.sound_icon_on if self.settings.sound_on else self.settings.sound_icon_off
        self.screen.blit(sound_icon, self.settings.sound_rect)
        self.screen.blit(self.settings.help_icon, self.settings.help_rect)

        # Draw lives and score
        self.game_stats.show_stats(self.screen)

        now = pygame.time.get_ticks()

        if self.game.state == "game_over":
            self.game_over_screen.draw(
            score=self.game_stats.score,
            high_score=self.game_stats.high_score
            )
            pygame.display.flip()
            return

        if self.ship.rect.bottom >= self.settings.height:
            self.game.state = "game_over"
            return

        if self.ship_hit_time:
            if now - self.ship_hit_time >= self.hit_pause_duration:
                self.ship_visible = True
                self.aliens_paused = False
                self.ship_hit_time = None
            else:
                if self.ship_visible:
                    self.ship.update()
                    self.ship.blitme()
                for bullet in self.alien_bullets:
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
                pygame.display.flip()
                return

        if self.ship_visible:
            collision = pygame.sprite.spritecollideany(self.ship, self.alien_bullets)
            if collision:
                self.game_stats.lives -= 1
                if self.game_stats.lives <= 0:
                    self.game.state = "game_over"
                    return
                self.ship_visible = False
                self.aliens_paused = True
                self.ship_hit_time = now
                collision.kill()
                self.bullets.empty()
                self.alien_bullets.empty()
                return
            
        # Handle delayed fleet respawn
        if self.fleet_respawn_time:
            if now - self.fleet_respawn_time >= self.respawn_delay:
                self._create_fleet()
                self.fleet_respawn_time = None
            else:
                pygame.display.flip()
                return  # Pause game during fleet respawn delay
    
        if self.ship_visible:
            self.ship.move_with_mouse()
            self.ship.update()
            self.ship.blitme()

        if not self.aliens_paused:
            self._alien_fire_check()
            self.alien_bullets.update()

        for bullet in self.alien_bullets:
            bullet.draw_bullet()

        if self.ship_visible:
            self.update_bullets()
            for bullet in self.bullets:
                bullet.draw_bullet()

        if not self.aliens_paused:
            self.update_aliens()

        self.aliens.draw(self.screen)
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hasattr(event, 'pos') and self.settings.help_rect.collidepoint(event.pos):
                self.game.previous_state = "game"
                self.game.state = "tutorial"
            elif hasattr(event, 'pos') and self.ship.rect.collidepoint(event.pos):
                self.ship.dragging = True
                self.ship.offset_x = self.ship.rect.x - event.pos[0]

        elif event.type == pygame.MOUSEBUTTONUP:
            self.ship.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.ship.dragging and hasattr(event, 'pos'):
                self.ship.rect.x = event.pos[0] + self.ship.offset_x

        elif event.type == pygame.KEYDOWN:
            self._check_keydown_events(event)

        elif event.type == pygame.KEYUP:
            self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.ship.moving_right = True
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.ship.moving_right = False
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        self.bullets.update()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for hit_list in collisions.values():
                self.game_stats.score += 10 * len(hit_list)

    def update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Check if any alien has reached the bottom
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.height:
                self.game.state = "game_over" # move to over screen
                return

         # Check for collision between ship and any alien
        if self.ship_visible:
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self.game.state = "game_over" # move to over screen
                return

        # If all aliens are destroyed and no timer set, start the respawn timer
        if not self.aliens and self.fleet_respawn_time is None:
            self.bullets.empty()          # Clear all ship bullets
            self.alien_bullets.empty()    # Clear all alien bullets
            self.fleet_respawn_time = pygame.time.get_ticks()

    def _check_fleet_edges(self):
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create a fleet of aliens and center it on the screen."""

        # Clear existing aliens before creating new ones
        self.aliens.empty()

        # Create a single alien to get its size
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        row_colors = ["red", "red", "green", "green", "blue", "blue"]

        # Calculate how many aliens fit in a row
        available_space_x = self.settings.width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Create the full fleet of aliens
        for row_number, color in enumerate(row_colors):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, color)

    def _create_alien(self, alien_num, row, color):
        alien = Alien(self, alien_type=color)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1.3 * alien_width * alien_num
        alien.rect.x = alien.x
        alien.rect.y = 100 + 0.8 * alien_height * row
        self.aliens.add(alien)

    def _alien_fire_check(self):
        now = pygame.time.get_ticks()
        if now - self.last_alien_shot_time > self.alien_shoot_interval:
            if self.aliens:
                alien = random.choice(self.aliens.sprites())
                bullet = AlienBullet(self, alien, self.ship)
                self.alien_bullets.add(bullet)
                self.last_alien_shot_time = now
