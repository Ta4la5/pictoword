import pygame
from coin_manager import CoinManager

from games.Easy1 import Game as Easy1
from games.Easy2 import Game as Easy2
from games.Easy3 import Game as Easy3
from games.Easy4 import Game as Easy4
from games.Easy5 import Game as Easy5
from games.Easy6 import Game as Easy6
from games.Easy7 import Game as Easy7
from games.Easy8 import Game as Easy8
from games.Easy9 import Game as Easy9
from games.Easy10 import Game as Easy10

from games.Medium1 import Game as Medium1
from games.Medium2 import Game as Medium2
from games.Medium3 import Game as Medium3
from games.Medium4 import Game as Medium4
from games.Medium5 import Game as Medium5
from games.Medium6 import Game as Medium6
from games.Medium7 import Game as Medium7
from games.Medium8 import Game as Medium8
from games.Medium9 import Game as Medium9
from games.Medium10 import Game as Medium10

from games.Hard1 import Game as Hard1
from games.Hard2 import Game as Hard2
from games.Hard3 import Game as Hard3
from games.Hard4 import Game as Hard4
from games.Hard5 import Game as Hard5
from games.Hard6 import Game as Hard6
from games.Hard7 import Game as Hard7
from games.Hard8 import Game as Hard8
from games.Hard9 import Game as Hard9
from games.Hard10 import Game as Hard10


class GameUI:
    def __init__(self, screen, mode):
        self.screen = screen
        self.mode = mode  # Could be 'easy', 'medium', or 'hard'
        self.width, self.height = self.screen.get_size()
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("t1.png")
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.back_button_pressed = False
        self.back_arrow_rect = pygame.Rect(20, 20, 50, 50)

        self.played_games = [False] * 10

        # Colors
        self.panel_color = (255, 235, 153)  # Light yellow
        self.panel_border_color = (255, 153, 153)  # Pink border
        self.button_color = (255, 255, 255)  # White buttons
        self.button_shadow_color = (200, 200, 200)  # Gray shadow for 3D effect
        #self.button_border_color = (0, 0, 0)  # Black border for buttons
        self.button_text_color = (0, 0, 0)  # Black text on buttons
        self.title_text_color = (255, 255, 255)  # White text for title
        self.shadow_color = (50, 50, 50)  # Shadow color

        # Fonts
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 60)

        # Load a back arrow image or draw it
        self.back_arrow_rect = pygame.Rect(20, 20, 50, 50)  # Position and size for the back arrow

        # UI Elements
        self.panel_rect = pygame.Rect(self.width // 4, self.height // 3, self.width * 2 // 4, self.height // 3 + 40)
        self.title_rect = pygame.Rect(self.width // 4, self.height // 4 + 10, self.width // 3, 50)
        self.buttons = []

        # Create buttons with adjusted spacing for 10 games
        button_width = 60
        button_height = 60
        button_spacing = 25  # Adjusted spacing between buttons in the same row
        row_spacing = 50  # Increased spacing between the two rows of buttons
        start_x = self.panel_rect.x + (self.panel_rect.width - (5 * button_width + 4 * button_spacing)) // 2
        start_y = self.panel_rect.y + (self.panel_rect.height // 3) - (button_height // 2)

        for i in range(10):
            row = i // 5
            col = i % 5
            button_rect = pygame.Rect(
                start_x + col * (button_width + button_spacing),
                start_y + row * (button_height + row_spacing),
                button_width,
                button_height
            )
            self.buttons.append(button_rect)

        self.games = {
            "EASY": [Easy1, Easy2, Easy3, Easy4, Easy5, Easy6, Easy7, Easy8, Easy9, Easy10],
            "MEDIUM": [Medium1, Medium2, Medium3, Medium4, Medium5, Medium6, Medium7, Medium8, Medium9, Medium10],
            "HARD": [Hard1, Hard2, Hard3, Hard4, Hard5, Hard6, Hard7, Hard8, Hard9, Hard10]
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.back_arrow_rect.collidepoint(mouse_pos):
                print("Back button clicked")
                self.back_button_pressed = True  # Set the flag when the back button is pressed
                return True

            for i, button_rect in enumerate(self.buttons):
                if button_rect.collidepoint(mouse_pos):
                    print(f"Game {i + 1} selected in {self.mode.capitalize()} mode.")

                    # Draw the current UI one last time
                    self.draw()  # Ensure the current screen is redrawn
                    pygame.display.flip()  # Update the display before transitioning

                    game_class = self.games[self.mode][i]  # Select the correct game class
                    game_instance = game_class(self.screen)  # Initialize the game

                    game_instance.run()  # Run the selected game

                    # Mark this game as played
                    self.played_games[i] = True  # Update the game tracking status

                    return False
        return False

    def show_loading_screen(self):
        # Fill the screen with a simple loading message
        self.screen.fill((0, 0, 0))
        loading_text = self.font.render("Loading...", True, (255, 255, 255))
        self.screen.blit(loading_text, (self.width // 2 - loading_text.get_width() // 2, self.height // 2))
        pygame.display.flip()

    def use_hint(self):
        if CoinManager.use_coins(10):  # Deduct coins using CoinManager
            # Logic to reveal a letter in the word
            # You'll need to modify your game logic to accommodate this
            print("Hint used!")  # For debugging
        else:
            print("Not enough coins!")  # For debugging

    def update(self):
        # Add any update logic for the Boxes instance
        pass

    def go_back(self):
        if self.back_button_pressed:
            print("Going back to the home page...")
            self.back_button_pressed = False  # Reset the flag
            return True
        return False

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        # Draw the back arrow
        arrow_color = (255, 255, 255)  # White arrow
        arrow_points = [
            (self.back_arrow_rect.left + self.back_arrow_rect.width // 3, self.back_arrow_rect.centery),
            (self.back_arrow_rect.right - self.back_arrow_rect.width // 3, self.back_arrow_rect.top),
            (self.back_arrow_rect.right - self.back_arrow_rect.width // 3, self.back_arrow_rect.bottom)
        ]
        pygame.draw.polygon(self.screen, arrow_color, arrow_points)

        self.draw_coin_counter()

        # Draw panel
        pygame.draw.rect(self.screen, self.panel_border_color, self.panel_rect, border_radius=20)
        pygame.draw.rect(self.screen, self.panel_color, self.panel_rect.inflate(-20, -20), border_radius=20)

        # Draw title with shadow
        title_text = self.title_font.render("SELECT GAME", True, self.title_text_color)
        title_shadow = self.title_font.render("SELECT GAME", True, self.shadow_color)
        self.screen.blit(title_shadow, (self.title_rect.x + 2, self.title_rect.y + 2))
        self.screen.blit(title_text, (self.title_rect.x, self.title_rect.y))

        for i, button_rect in enumerate(self.buttons):
            # If the game has been played, change the button color
            if self.played_games[i]:
                button_color = (0, 200, 0)  # Green for played games
            else:
                button_color = self.button_color  # Default color for unplayed games

            # **3D Effect on Button Background**
            # Draw shadow for 3D effect
            shadow_offset = 5
            shadow_rect = button_rect.move(shadow_offset, shadow_offset)
            pygame.draw.rect(self.screen, self.button_shadow_color, shadow_rect, border_radius=15)
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=15)

            # **3D Effect on Button Text**
            # Draw shadow for text
            button_text_shadow = self.font.render(str(i + 1), True, self.shadow_color)
            text_shadow_rect = button_text_shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery + 2))
            self.screen.blit(button_text_shadow, text_shadow_rect)

            # Draw button text
            button_text = self.font.render(str(i + 1), True, self.button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

        pygame.display.flip()
        self.clock.tick(60)

        pygame.display.flip()
        self.clock.tick(60)

    def draw_coin_counter(self):
        # Display coins from CoinManager
        pygame.draw.rect(self.screen, (255, 192, 203), (self.width - 130, 20, 110, 40), border_radius=20)
        pygame.draw.circle(self.screen, (255, 255, 0), (self.width - 110, 40), 15)
        pygame.draw.circle(self.screen, (0, 0, 0), (self.width - 110, 40), 15, 2)
        coin_text = pygame.font.Font(None, 36).render(str(CoinManager.get_coins()), True, (255, 255, 255))
        coin_rect = coin_text.get_rect(center=(self.width - 60, 40))
        self.screen.blit(coin_text, coin_rect)
