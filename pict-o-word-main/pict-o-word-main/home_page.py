import pygame
import math
import pygame.mixer
from coin_manager import CoinManager


class HomePage:
    def __init__(self, screen, background_image):
        pygame.mixer.init()  # Initialize the mixer for audio
        self.screen = screen
        self.bg = background_image
        self.width, self.height = screen.get_size()
        self.setup_colors()
        self.setup_fonts()
        self.current_mode = "EASY"
        self.settings_open = False
        self.load_icons()

        # Load the logo
        self.logo = pygame.image.load("Logo4.png")
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = self.width // 2
        self.logo_rect.y = 50

        # Create shadow for the logo
        self.logo_shadow = self.logo.copy()
        self.logo_shadow.fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
        self.logo_shadow_rect = self.logo_shadow.get_rect()
        self.logo_shadow_rect.x = self.logo_rect.x + 9
        self.logo_shadow_rect.y = self.logo_rect.y + 9

        # Music and volume settings
        pygame.mixer.music.load("pianomusic.mp3")  # Replace with your music file
        self.music_on = False  # Music starts off
        self.volume_level = 0.5  # Volume starts at 50%
        pygame.mixer.music.set_volume(self.volume_level)

        # Help text
        self.help_text = None

        # Click feedback
        self.feedback_time = 200  # Feedback lasts for 200ms
        self.last_click_time = 0
        self.feedback_rect = None

        # Track if a selection has been made
        self.selection_made = False  # Initialize to False
        self.selected_mode = None  # Store the selected mode when "Play" is clicked

    def setup_colors(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 127.5 * 0.75, 0)
        self.YELLOW = (255 * 0.65, 255 * 0.65, 0)
        self.RED = (127.5 * 0.75, 0, 0)
        self.PINK = (127.5 * 0.9, 52.5 * 0.9, 90 * 0.9)
        self.LIGHT_BLUE = (86.5 * 0.75, 108 * 0.75, 115 * 0.75)
        self.PALEYELLOW = (225 * 0.75, 225 * 0.75, 100 * 0.75)
        self.YELLOW1 = (255, 255, 0)
        self.PINK1 = (225 * 0.85, 105 * 0.85, 180 * 0.85)

    def setup_fonts(self):
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)
        self.help_font = pygame.font.Font(None, 28)

    def load_icons(self):
        self.icons = {
            "Music": self.create_music_icon(),
            "Volume": self.create_volume_icon(),
            "Need Help?": self.create_help_icon()
        }

    def create_music_icon(self):
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.WHITE, (15, 15), 10, 2)
        pygame.draw.line(surface, self.WHITE, (25, 15), (25, 5), 2)
        return surface

    def create_volume_icon(self):
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(surface, self.WHITE, [(5, 15), (15, 5), (15, 25)])
        pygame.draw.arc(surface, self.WHITE, (15, 5, 10, 20), -math.pi / 3, math.pi / 3, 2)
        return surface

    def create_help_icon(self):
        surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.WHITE, (15, 15), 13, 2)
        font = pygame.font.Font(None, 24)
        text = font.render("?", True, self.WHITE)
        surface.blit(text, (11, 8))
        return surface

    def draw(self):
        print("Drawing home page...")  # Debug statement

        # Fill screen with a color to verify it’s being drawn
        self.screen.fill((50, 150, 200))  # Different color to ensure drawing

        self.screen.blit(self.bg, (0, 0))
        self.draw_logo()
        self.draw_mode_button()
        self.draw_play_button()
        self.draw_exit_button()
        self.draw_settings_icon()
        self.draw_coin_counter()

        if self.settings_open:
            self.draw_settings()


        # Draw help text if active
        if self.help_text:
            self.draw_help_text()

        # Draw click feedback
        if self.feedback_rect and pygame.time.get_ticks() - self.last_click_time < self.feedback_time:
            pygame.draw.rect(self.screen, self.YELLOW1, self.feedback_rect, 3)

    def draw_logo(self):
        self.screen.blit(self.logo_shadow, self.logo_shadow_rect)
        self.screen.blit(self.logo, self.logo_rect)

    def draw_mode_button(self):
        colors = {"EASY": self.GREEN, "MEDIUM": self.YELLOW, "HARD": self.RED}
        y_pos = 330
        self.draw_circle_with_shadow(self.screen, colors[self.current_mode], (self.width // 2, y_pos), 50)
        mode_text = self.button_font.render(self.current_mode, True, self.WHITE)
        mode_rect = mode_text.get_rect(center=(self.width // 2, y_pos))
        self.screen.blit(mode_text, mode_rect)

        if self.current_mode != "EASY":
            pygame.draw.polygon(self.screen, self.WHITE,
                                [(self.width // 2 - 80, y_pos), (self.width // 2 - 60, y_pos - 10),
                                 (self.width // 2 - 60, y_pos + 10)])
        if self.current_mode != "HARD":
            pygame.draw.polygon(self.screen, self.WHITE,
                                [(self.width // 2 + 80, y_pos), (self.width // 2 + 60, y_pos - 10),
                                 (self.width // 2 + 60, y_pos + 10)])

    def draw_play_button(self):
        y_pos = 430
        self.draw_rect_with_shadow(self.screen, self.PALEYELLOW, (self.width // 2 - 90, y_pos, 180, 60),
                                   border_radius=15)
        play_text = self.button_font.render("PLAY", True, self.WHITE)
        play_rect = play_text.get_rect(center=(self.width // 2, y_pos + 30))
        self.screen.blit(play_text, play_rect)

    def draw_exit_button(self):
        y_pos = 530
        self.draw_rect_with_shadow(self.screen, self.PINK1, (self.width // 2 - 90, y_pos, 180, 60), border_radius=15)
        exit_text = self.button_font.render("EXIT", True, self.WHITE)
        exit_rect = exit_text.get_rect(center=(self.width // 2, y_pos + 30))
        self.screen.blit(exit_text, exit_rect)

    def draw_settings_icon(self):
        self.draw_circle_with_shadow(self.screen, self.PINK1, (40, 40), 20)
        for i in range(3):
            y = 33 + i * 7
            pygame.draw.line(self.screen, self.WHITE, (30, y), (50, y), 2)

    def draw_coin_counter(self):
        self.draw_rect_with_shadow(self.screen, self.PINK1, (self.width - 130, 20, 110, 40), border_radius=20)
        pygame.draw.circle(self.screen, self.YELLOW1, (self.width - 110, 40), 15)
        pygame.draw.circle(self.screen, self.BLACK, (self.width - 110, 40), 15, 2)
        coin_text = self.button_font.render(str(CoinManager.get_coins()), True, self.WHITE)
        coin_rect = coin_text.get_rect(center=(self.width - 60, 40))
        self.screen.blit(coin_text, coin_rect)

    def draw_settings(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        settings_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
        settings_surface.fill((173, 216, 230, 200))  # Light blue with some transparency

        settings_title = self.title_font.render("SETTINGS", True, self.WHITE)
        settings_surface.blit(settings_title, (75, 20))

        options = ["Music", "Volume", "Need Help?"]
        for i, option in enumerate(options):
            # Change both text and icon color for the "Music" option based on music state
            text_color = self.YELLOW if option == "Music" and self.music_on else self.WHITE
            icon_color = text_color  # Make icon color same as text color

            # Render the option text (e.g., "Music", "Volume", etc.) with the appropriate color
            text = self.button_font.render(option, True, text_color)
            settings_surface.blit(text, (70, 100 + i * 60))

            # Draw the icon for each setting option
            self.draw_icon(settings_surface, option, (30, 95 + i * 60), icon_color)

            # Draw the volume slider for the "Volume" option
            if option == "Volume":
                pygame.draw.rect(settings_surface, self.WHITE, (70, 140 + i * 60, 160, 4))
                slider_pos = 70 + int(160 * self.volume_level)
                pygame.draw.circle(settings_surface, self.WHITE, (slider_pos, 142 + i * 60), 8)

        self.screen.blit(settings_surface, (self.width // 2 - 150, self.height // 2 - 200))

    def draw_icon(self, surface, option, pos, color):
        if option == "Music":
            pygame.draw.circle(surface, color, (pos[0] + 15, pos[1] + 15), 10, 2)
            pygame.draw.line(surface, color, (pos[0] + 25, pos[1] + 15), (pos[0] + 25, pos[1] + 5), 2)
        elif option == "Volume":
            pygame.draw.polygon(surface, color,
                                [(pos[0] + 5, pos[1] + 15), (pos[0] + 15, pos[1] + 5), (pos[0] + 15, pos[1] + 25)])
            pygame.draw.arc(surface, color, (pos[0] + 15, pos[1] + 5, 10, 20), -math.pi / 3, math.pi / 3, 2)
        elif option == "Need Help?":
            pygame.draw.circle(surface, color, (pos[0] + 15, pos[1] + 15), 13, 2)
            font = pygame.font.Font(None, 24)
            text = font.render("?", True, color)
            surface.blit(text, (pos[0] + 11, pos[1] + 8))

    def draw_help_text(self):
        help_surface_height = 360
        help_surface = pygame.Surface((self.width, help_surface_height), pygame.SRCALPHA)
        help_surface.fill((0, 0, 0, 200))  # Semi-transparent black background

        help_text_lines = [
            "Tap the volume slider to adjust the volume.",
            "Left-click to select and input a letter, Right-click to drop the letter.",
            "There are 3 different difficulties that a user can access, click arrows to navigate",
            "For easy, you have only 1 guess, for medium, 2 and 3 for hard",
            "Maximize screen by clicking F11",
            "To exit a selected game,  close the window,"
            "you'll be automatically taken to the game selection interface",
            "Click the hint button to reveal a letter for 10 coins",
            "You gain 5 coins with every win",
            "Good luck!"
        ]
        y_offset = 15  # Start drawing text from this y-coordinate within help_surface
        line_spacing = 45  # Space between lines of text

        for i, line in enumerate(help_text_lines):
            help_text = self.help_font.render(line, True, self.WHITE)
            help_rect = help_text.get_rect(center=(self.width // 2, y_offset + i * line_spacing))
            help_surface.blit(help_text, help_rect)

        # Blit the help surface onto the screen, positioned at the bottom
        self.screen.blit(help_surface, (0, self.height - help_surface_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()


            if self.settings_open:
                if not self.is_point_inside(mouse_pos, (self.width // 2 - 150, self.height // 2 - 200, 300, 300)):
                    self.settings_open = False
                    self.help_text = None # Clear the help text when closing settings
                else:
                    self.handle_settings_click(mouse_pos)
            else:
                y_pos = 330  # Match the y-position for the mode button

                # Check for right arrow (next mode)
                if self.is_point_inside(mouse_pos, (self.width // 2 + 60, y_pos - 10, 20, 20)):
                    self.cycle_mode(1)
                # Check for left arrow (previous mode)
                elif self.is_point_inside(mouse_pos, (self.width // 2 - 80, y_pos - 10, 20, 20)):
                    self.cycle_mode(-1)
                # Check for settings icon
                elif self.is_point_inside(mouse_pos, (20, 20, 40, 40)):
                    self.settings_open = True
                # Check for play button
                elif self.is_point_inside(mouse_pos, (self.width // 2 - 90, 450, 180, 60)):
                    print("Play button clicked")
                    self.selection_made = True  # Update selection_made when "Play" is clicked
                    self.selected_mode = self.current_mode  # Store the selected mode
                    return "PLAY"
                # Check for exit button
                elif self.is_point_inside(mouse_pos, (self.width // 2 - 90, 530, 180, 60)):
                    pygame.quit()
                    quit()
        return None
    def handle_settings_click(self, mouse_pos):
        x, y = mouse_pos
        setting_rect_x = self.width // 2 - 150
        setting_rect_y = self.height // 2 - 200

        # Check each setting option
        if self.is_point_inside(mouse_pos, (setting_rect_x + 30, setting_rect_y + 95, 240, 60)):
            # Toggle Music
            self.music_on = not self.music_on
            if self.music_on:
                pygame.mixer.music.play(-1)  # Loop forever
            else:
                pygame.mixer.music.stop()
            print(f"Music toggled to {'on' if self.music_on else 'off'}")

            # Add feedback
            self.feedback_rect = (setting_rect_x + 30, setting_rect_y + 95, 240, 60)
            self.last_click_time = pygame.time.get_ticks()

        elif self.is_point_inside(mouse_pos, (setting_rect_x + 30, setting_rect_y + 155, 240, 60)):
            # Adjust Volume using slider
            slider_x = setting_rect_x + 70
            slider_width = 160
            if slider_x <= x <= slider_x + slider_width:
                self.volume_level = (x - slider_x) / slider_width
                pygame.mixer.music.set_volume(self.volume_level)
            print(f"Volume level set to {int(self.volume_level * 100)}%")

            # Add feedback
            self.feedback_rect = (setting_rect_x + 30, setting_rect_y + 155, 240, 60)
            self.last_click_time = pygame.time.get_ticks()


        elif self.is_point_inside(mouse_pos, (setting_rect_x + 30, setting_rect_y + 205, 240, 60)):
            # Show Help
            self.help_text = "Tap the volume slider to adjust volume."
            print("Help shown")

            # Add feedback
            self.feedback_rect = (setting_rect_x + 30, setting_rect_y + 205, 240, 60)
            self.last_click_time = pygame.time.get_ticks()

    def is_point_inside(self, point, rect):
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

    def cycle_mode(self, direction):
        modes = ["EASY", "MEDIUM", "HARD"]
        current_index = modes.index(self.current_mode)
        new_index = (current_index + direction) % 3
        self.current_mode = modes[new_index]

    def draw_circle_with_shadow(self, surface, color, center, radius):
        shadow = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 128), (radius + 2, radius + 2), radius + 2,
                           5)  # Increased shadow size and blur
        surface.blit(shadow, (center[0] - radius - 2, center[1] - radius - 2))
        pygame.draw.circle(surface, color, center, radius)

    def draw_rect_with_shadow(self, surface, color, rect, border_radius=0):
        shadow = pygame.Surface((rect[2] + 4, rect[3] + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 128), (2, 2, rect[2], rect[3]), border_radius=border_radius,
                         width=5)  # Increased shadow size and blur
        surface.blit(shadow, (rect[0] - 2, rect[1] - 2))
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def update(self):
        pass  # Add any update logic here if needed
