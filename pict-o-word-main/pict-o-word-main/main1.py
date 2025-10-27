import pygame
from loading_page import LoadingPage
from home_page import HomePage
from game_ui import GameUI  # Import the GameUI class
from coin_manager import CoinManager


class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False  # Track if the game is in full-screen mode or not
        self.screen = pygame.display.set_mode((1280, 720))  # Start in windowed mode

        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("t1.png")

        self.loading_page = LoadingPage(self.screen)
        self.home_page = HomePage(self.screen, self.bg)
        pygame.display.set_caption("Pict-o-word")
        icon = pygame.image.load("Logo3.png")
        pygame.display.set_icon(icon)

        self.game_ui = None
        self.current_page = "loading"

    def run(self):
        running = True
        while running:
            print(f"Current page in loop: {self.current_page}")  # Debugging output

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Toggle full screen when F11 is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                action = self.handle_event(event)

                if action == "BACK_TO_HOME":
                    self.current_page = "home"

            self.update()
            self.draw()
            pygame.display.update()  # Use update() instead of flip() to force redraw
            self.clock.tick(60)

        pygame.quit()

    def toggle_fullscreen(self):
        """Toggle between full-screen and windowed mode."""
        if self.fullscreen:
            self.screen = pygame.display.set_mode((1280, 720))  # Switch to windowed mode
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)  # Switch to full-screen mode
            self.fullscreen = True

        # Update the background and other pages with the new screen size
        self.bg = pygame.transform.scale(self.bg, self.screen.get_size())
        self.loading_page.screen = self.screen
        self.home_page.screen = self.screen
        if self.game_ui:
            self.game_ui.screen = self.screen

    def handle_event(self, event):
        if self.current_page == "loading":
            self.loading_page.handle_event(event)
        elif self.current_page == "home":
            self.home_page.handle_event(event)
        elif self.current_page == "game_ui":
            action = self.game_ui.handle_event(event)
            if action == "BACK_TO_HOME":
                print("Switching to home page")  # Debugging output
                self.current_page = "home"
                print(f"Current page is now: {self.current_page}")  # Confirm the page is set

    def update(self):
        if self.current_page == "loading":
            self.loading_page.update()
            if self.loading_page.loading_completed:
                self.current_page = "home"
        elif self.current_page == "home":
            print("Updating home page...")  # Debugging output
            self.home_page.update()
            if self.home_page.selection_made:
                self.game_ui = GameUI(self.screen, self.home_page.selected_mode)  # Use the selected mode
                self.current_page = "game_ui"
                self.home_page.selection_made = False  # Reset the selection
        elif self.current_page == "game_ui":
            print("Updating game UI page...")  # Debugging output
            self.game_ui.update()
            if self.game_ui.go_back():  # Assuming `go_back` in GameUI returns True if back is pressed
                self.current_page = "home"
                self.home_page.selection_made = False  # Reset the selection when returning to home

    def draw(self):
        # Clear the screen first
        self.screen.fill((0, 0, 0))  # Fill with black or any color to ensure the screen is cleared
        if self.current_page == "loading":
            print("Drawing loading page...")  # Debugging output
            self.loading_page.draw()
        elif self.current_page == "home":
            print("Drawing home page...")  # Debugging output
            self.home_page.draw()
        elif self.current_page == "game_ui":
            print("Drawing game UI page...")  # Debugging output
            self.game_ui.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
