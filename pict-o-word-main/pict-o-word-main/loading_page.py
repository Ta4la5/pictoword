import pygame
import random

class LoadingPage:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("t1.png")
        self.logo = pygame.image.load("Logo3.png")
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = self.width // 2
        self.logo_rect.y = 50
        self.loading_progress = 0
        self.loading_speed = 4
        self.loading_completed = False
        self.bar_width = 450
        self.bar_height = 50
        self.bar_x = (self.width - self.bar_width) // 2
        self.bar_y = self.height - 200
        self.BLUE = (0, 102, 204)
        self.YELLOW = (255, 255, 100)
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)

        # Load a custom fancy font for the "Word of the Day"
        self.word_font = pygame.font.Font('fancy_font.ttf', 35)  # Use a larger size for emphasis

        # List of words that fit the narrative
        self.words_of_the_day = [
            "Claustrophobic", "Enigma", "Labyrinth", "Mystic", "Ephemeral",
            "Ethereal", "Serendipity", "Pandemonium", "Paradox", "Vortex",
            "Oblivion", "Abyss", "Quagmire", "Eclipse", "Nebula",
            "Chimera", "Phantom", "Reverie", "Mirage", "Specter"
        ]

        # Randomly select a word of the day
        self.word_of_the_day = random.choice(self.words_of_the_day)

        self.shadow = self.logo.copy()
        self.shadow.fill((0, 0, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        if not self.loading_completed:
            self.loading_progress += self.loading_speed
            if self.loading_progress >= self.bar_width:
                self.loading_progress = self.bar_width
                self.loading_completed = True

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.logo, self.logo_rect)

        # Draw loading bar
        pygame.draw.rect(self.screen, self.WHITE, (self.bar_x, self.bar_y, self.bar_width, self.bar_height), 2, border_radius=25)
        pygame.draw.rect(self.screen, self.YELLOW, (self.bar_x, self.bar_y, int(self.loading_progress), self.bar_height), 0, border_radius=25)

        # Loading text
        loading_text = self.font.render("LOADING...", True, self.WHITE)
        text_x = self.bar_x + (self.bar_width - loading_text.get_width()) // 2
        text_y = self.bar_y + (self.bar_height - loading_text.get_height()) // 2
        shadow_text = self.font.render("LOADING...", True, (0, 0, 0))

        self.screen.blit(shadow_text, (text_x + 2, text_y + 2))  # Shadow for loading text
        self.screen.blit(loading_text, (text_x, text_y))

        # Word of the Day text with custom font and subtle shadow effect
        word_text = self.word_font.render(f"Word of the day: {self.word_of_the_day}", True, self.WHITE)
        word_text_shadow = self.word_font.render(f"Word of the day: {self.word_of_the_day}", True, (50, 50, 50))
        word_text_x = (self.width - word_text.get_width()) // 2
        word_text_y = self.bar_y + self.bar_height + 80

        # Shadow effect for the Word of the Day text
        self.screen.blit(word_text_shadow, (word_text_x + 2, word_text_y + 2))  # Subtle shadow
        self.screen.blit(word_text, (word_text_x, word_text_y))  # Main text

        # Shadow for the logo
        shadow_offset = (9, 9)
        self.screen.blit(self.shadow, (self.logo_rect.x + shadow_offset[0], self.logo_rect.y + shadow_offset[1]))

    def handle_event(self, event):
        pass  # No events to handle in the loading page
