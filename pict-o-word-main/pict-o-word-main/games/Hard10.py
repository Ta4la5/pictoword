import pygame
import os
import random
import math
from coin_manager import CoinManager

class Reset:
    @staticmethod
    def reset_boxes(boxes):
        boxes.count = 0
        boxes.back_value = []
        boxes.tries_left = 3

        # Reset the box positions
        boxes.box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(boxes.boxX, boxes.boxY)]
        boxes.letter_positions = boxes.box_rects[:]

    @staticmethod
    def reset_game(game):
        game.boxes = Boxes(game)  # Reinitialize the boxes
        game.run()  # Restart the game loop


class Boxes:
    def __init__(self, game):
        self.A1 = (442 + 6, 430 + 4)
        self.A2 = (486 + 6, 430 + 4)
        self.A3 = (530 + 6, 430 + 4)
        self.A4 = (574 + 6, 430 + 4)
        self.A5 = (618 + 6, 430 + 4)
        self.A6 = (662 + 6, 430 + 4)
        self.A7 = (706 + 6, 430 + 4)
        self.A8 = (750 + 6, 430 + 4)

        self.T1 = (466 + 6, 520 + 4)
        self.T2 = (510 + 6, 520 + 4)
        self.T3 = (554 + 6, 520 + 4)
        self.T4 = (598 + 6, 520 + 4)
        self.T5 = (642 + 6, 520 + 4)
        self.T6 = (686 + 6, 520 + 4)
        self.T7 = (730 + 6, 520 + 4)
        self.T8 = (774 + 6, 520 + 4)

        self.B1 = (466 + 6, 564 + 4)
        self.B2 = (510 + 6, 564 + 4)
        self.B3 = (554 + 6, 564 + 4)
        self.B4 = (598 + 6, 564 + 4)
        self.B5 = (642 + 6, 564 + 4)
        self.B6 = (686 + 6, 564 + 4)
        self.B7 = (730 + 6, 564 + 4)
        self.B8 = (774 + 6, 564 + 4)

        self.boxX = [466, 510, 554, 598, 642, 686, 730, 774, 466, 510, 554, 598, 642, 686, 730, 774]
        self.boxY = [520, 520, 520, 520, 520, 520, 520, 520, 564, 564, 564, 564, 564, 564, 564, 564]
        self.box = [pygame.image.load("qaz.jpg") for _ in range(16)]

        self.black_boxX = [466, 510, 554, 598, 642, 686, 730, 774, 466, 510, 554, 598, 642, 686, 730, 774]
        self.black_boxY = [520, 520, 520, 520, 520, 520, 520, 520, 564, 564, 564, 564, 564, 564, 564, 564]
        self.black_box = [pygame.image.load("sav.jpg") for _ in range(16)]

        self.answer_boxX = [442+22, 486+22, 530+22, 574+22, 618+22, 662+22, 706+22, 750+22]
        self.answer_boxY = [430, 430, 430, 430, 430, 430, 430, 430]
        self.answer_box = [pygame.image.load("sav.jpg") for _ in range(9)]

        self.box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.boxX, self.boxY)]
        self.black_box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.black_boxX, self.black_boxY)]
        self.answer_box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.answer_boxX, self.answer_boxY)]

        self.letter_positions = self.box_rects[:]

        self.movement_positions = {
            0: (442+22, 430),
            1: (486+22, 430),
            2: (530+22, 430),
            3: (574+22, 430),
            4: (618+22, 430),
            5: (662+22, 430),
            6: (706+22, 430),
            7: (750+22, 430),
        }

        self.correct_positions = {
            0: 15,  # index of the first correct letter
            1: 9,  # index of the second correct letter
            2: 11,  # index of the third correct letter
            3: 6,  # index of the fourth correct letter
            4: 8,  # index of the fifth correct letter
            5: 3,
            6: 5,
            7: 0
        }

        self.game = game
        self.coins = 0
        self.hint_button = pygame.Rect(100, 550, 215, 50)  # Example position and size
        self.hint_button_color = (125, 50, 50)  # Example background color (DodgerBlue)
        self.hint_text_color = (255, 255, 255)  # White text color
        self.hint_font = pygame.font.Font(None, 40)
        self.coin_image = pygame.image.load('coin.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))

        self.back_value = []
        self.count = 0
        self.tries_left = 3
        self.border_radius = 15
        self.game_over = False
        self.win = False

    def use_hint(self):
        if CoinManager.use_coins(10):  # Deduct 10 coins for a hint
            self.reveal_letter()  # Reveal a letter
            self.play_hint_effects()  # Play visual/sound effects
            return True
        else:
            self.play_not_enough_coins_effects()  # Play visual/sound effects for insufficient coins
            return False

    def play_not_enough_coins_effects(self):
        # Play a "negative" sound effect indicating failure to use hint
        not_enough_coins_sound = pygame.mixer.Sound('not_enough_coins.wav')  # Placeholder sound file
        not_enough_coins_sound.play()

        # Display a fading "Not enough coins!" message
        self.display_not_enough_coins_text()

    def display_not_enough_coins_text(self):
        no_coins_text_color = (255, 0, 0)  # Red color to indicate an error
        font = pygame.font.Font(None, 60)
        no_coins_text = font.render("Not enough coins!", True, no_coins_text_color)

        # Display the text at the center of the screen
        for alpha in range(0, 255, 25):  # Fading effect
            no_coins_text.set_alpha(alpha)  # Set transparency level
            self.game.screen.fill((0, 0, 0, 128))  # Optional: Dim the background slightly
            self.game.screen.blit(no_coins_text,
                                  (self.game.screen.get_width() // 2 - no_coins_text.get_width() // 2, 300))
            pygame.display.flip()
            pygame.time.wait(200)

    def play_hint_effects(self):
        # Play a subtle sound effect
        hint_sound = pygame.mixer.Sound('hint_used_sound.wav')  # Placeholder sound file
        hint_sound.play()

        # Flash "Hint Activated!" text on the screen
        self.display_hint_text()

    def display_hint_text(self):
        hint_text_color = (255, 255, 0)  # Bright yellow for the hint text
        font = pygame.font.Font(None, 60)
        hint_text = font.render("Hint Activated!", True, hint_text_color)

        # Display the text at the center of the screen
        for alpha in range(0, 255, 25):  # Fading effect
            hint_text.set_alpha(alpha)  # Set transparency level
            self.game.screen.blit(hint_text, (self.game.screen.get_width() // 2 - hint_text.get_width() // 2, 300))
            pygame.display.flip()
            pygame.time.wait(200)

    def display_message(self, message, position, color):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, color)
        self.game.screen.blit(text, position)
        pygame.display.flip()
        pygame.time.wait(500)  # Wait for a second to show the message

    def reveal_letter(self):
        for i in range(len(self.movement_positions)):
            if i >= self.count:
                correct_box_index = self.correct_positions[i]
                pos = self.movement_positions[i]
                self.box_rects[correct_box_index] = pygame.Rect(*pos, 40, 40)
                self.letter_positions[correct_box_index] = pygame.Rect(*pos, 40, 40)
                self.count += 1
                self.back_value.append(correct_box_index)
                break

    def check_win(self):
        print("Checking win")
        correct_position1 = [(442 + 22, 430), (486 + 22, 430), (530 + 22, 430), (574 + 22, 430), (618 + 22, 430), (662 + 22, 430), (706 + 22, 430), (750 + 22, 430)]
        current_positions = [self.box_rects[i].topleft for i in self.correct_positions.values()]
        return current_positions == correct_position1

    def draw_hint_button(self, screen):
        pygame.draw.rect(screen, self.hint_button_color, self.hint_button, border_radius=self.border_radius)
        hint_text = self.hint_font.render("Use Hint 10 ", True, self.hint_text_color)
        screen.blit(hint_text, (self.hint_button.x + 10, self.hint_button.y + 10))

        coin_x = self.hint_button.x + hint_text.get_width() + 8  # Adjust the X position to place the coin next to the text
        coin_y = self.hint_button.y + 9  # Adjust the Y position to align with the text
        screen.blit(self.coin_image, (coin_x, coin_y))

    def display_last_chance_effect(self):
        self.game.screen.fill((0, 0, 0))  # Black out the background
        font = pygame.font.Font(None, 74)
        text = font.render('Last Chance!', True, (255, 125, 0))  # Yellow text to indicate urgency
        self.game.screen.blit(text, (540, 360))  # Display in the center

        # Optional: Add a screen shake effect to emphasize the last chance
        for _ in range(20):  # Shake for a brief moment
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            self.game.screen.blit(text, (540 + offset_x, 360 + offset_y))
            pygame.display.flip()
            pygame.time.wait(20)  # Wait between shakes

        pygame.display.flip()
        pygame.time.wait(1500)  # Wait for 1.5 seconds before continuing

    def display_last_chance_effect2(self):
        self.game.screen.fill((0, 0, 0))  # Black out the background
        font = pygame.font.Font(None, 74)
        text = font.render('Two More Chances!', True, (255, 255, 0))  # Yellow text to indicate urgency
        self.game.screen.blit(text, (540, 360))  # Display in the center

        # Optional: Add a screen shake effect to emphasize the last chance
        for _ in range(20):  # Shake for a brief moment
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            self.game.screen.blit(text, (540 + offset_x, 360 + offset_y))
            pygame.display.flip()
            pygame.time.wait(20)  # Wait between shakes

        pygame.display.flip()
        pygame.time.wait(1500)  # Wait for 1.5 seconds before continuing

    def clicks(self, mouse_pos):
        for i, rect in enumerate(self.box_rects):
            if rect.collidepoint(mouse_pos) and self.count < len(self.movement_positions) and mouse_pos[1] > 490:
                pos = self.movement_positions[self.count]
                self.box_rects[i] = pygame.Rect(*pos, 40, 40)
                self.letter_positions[i] = pygame.Rect(*pos, 40, 40)  # Update letter position
                self.count += 1
                self.back_value.append(i)

                self.game.click_sound.play()

                # Check if all answer slots are filled
                if self.count == len(self.movement_positions):
                    if self.check_win():
                        self.game_over = True
                        self.win = True
                    else:
                        self.tries_left -= 1
                        if self.tries_left <= 0:
                            self.game_over = True
                            self.win = False
                        else:
                            if self.tries_left == 1:
                                self.display_last_chance_effect()
                            else:
                                pygame.time.wait(200)
                                self.display_last_chance_effect2()

                return

    def back_click(self, mouse_pos):
        if self.count > 0:
            last_index = self.back_value.pop()
            self.box_rects[last_index] = pygame.Rect(self.boxX[last_index], self.boxY[last_index], 40, 40)
            self.letter_positions[last_index] = pygame.Rect(self.boxX[last_index], self.boxY[last_index], 40,
                                                            40)  # Update letter position
            self.count -= 1
            self.game.click_sound.play()


class Game:
    def __init__(self, screen):
        pygame.init()
        pygame.mixer.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.boxes = Boxes(self)
        base_path = os.path.dirname(__file__)
        image_path1 = os.path.join(base_path, "hard", "Solitude", "a.png")
        image_path2 = os.path.join(base_path, "hard", "Solitude", "b.png")
        image_path3 = os.path.join(base_path, "hard", "Solitude", "c.png")
        image_path4 = os.path.join(base_path, "hard", "Solitude", "d.png")
        self.hint_font = pygame.font.Font('freesansbold.ttf', 24)
        self.coin_font = pygame.font.Font('freesansbold.ttf', 24)

        self.background = pygame.image.load('edc.jpg')
        self.logo = pygame.image.load("logs-removebg-preview.png")
        self.picture_one = pygame.image.load(image_path1)
        self.picture_two = pygame.image.load(image_path2)
        self.picture_three = pygame.image.load(image_path3)
        self.picture_four = pygame.image.load(image_path4)

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.game_number = 10
        self.game_over_delay = 1000

        self.ans_one = self.font.render("E", True, (0, 0, 0))
        self.ans_two = self.font.render("N", True, (0, 0, 0))
        self.ans_three = self.font.render("P", True, (0, 0, 0))
        self.ans_four = self.font.render("U", True, (0, 0, 0))
        self.ans_five = self.font.render("H", True, (0, 0, 0))
        self.ans_six = self.font.render("D", True, (0, 0, 0))
        self.ans_seven = self.font.render("I", True, (0, 0, 0))
        self.ans_eight = self.font.render("W", True, (0, 0, 0))
        self.ans_nine = self.font.render("T", True, (0, 0, 0))

        self.others_one = self.font.render("O", True, (0, 0, 0))
        self.others_two = self.font.render("H", True, (0, 0, 0))
        self.others_three = self.font.render("L", True, (0, 0, 0))
        self.others_four = self.font.render("R", True, (0, 0, 0))
        self.others_five = self.font.render("P", True, (0, 0, 0))
        self.others_six = self.font.render("A", True, (0, 0, 0))
        self.others_seven = self.font.render("S", True, (0, 0, 0))

        self.boxes = Boxes(self)
        self.coin_image = pygame.image.load('coin.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (30, 30))
        self.PINK1 = (225 * 0.85, 105 * 0.85, 180 * 0.85)

        self.click_sound = pygame.mixer.Sound('click_sound.wav')  # Load the click sound
        self.win_sound = pygame.mixer.Sound('win_sound.wav')  # Load the win sound
        self.lose_sound = pygame.mixer.Sound('lose_sound.wav')  # Load the lose sound
        self.click_sound.set_volume(0.5)  # Set click sound volume to 50%
        self.win_sound.set_volume(0.6)  # Set win sound volume to 60%
        self.lose_sound.set_volume(0.5)  # Set lose sound volume to 50%

    def draw_coin_counter(self):
        self.draw_rect_with_shadow(self.screen, self.PINK1, (self.screen.get_width() - 130, 20, 110, 40),
                                   border_radius=20)
        self.screen.blit(self.coin_image, (self.screen.get_width() - 120, 25))  # Draw the coin image
        coin_text = self.coin_font.render(str(CoinManager.get_coins()), True, (255, 255, 255))  # Render coin count
        self.screen.blit(coin_text, (self.screen.get_width() - 65, 28))  # Draw the coin count next to the coin image

    def draw_rect_with_shadow(self, surface, color, rect, border_radius=0):
        shadow = pygame.Surface((rect[2] + 4, rect[3] + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 128), (2, 2, rect[2], rect[3]), border_radius=border_radius,
                         width=5)  # Increased shadow size and blur
        surface.blit(shadow, (rect[0] - 2, rect[1] - 2))
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def run(self):
        while self.running:
            self.screen.fill("purple")
            self.screen.blit(self.background, (0, 0))

            click = False
            back_click = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.boxes.hint_button.collidepoint(mouse_pos):
                            if self.boxes.use_hint():
                                print("Hint used!")
                            else:
                                print("Not enough coins for hint!")
                        else:
                            click = True

                    elif event.button == 3:  # Right click
                        back_click = True

            if click:
                self.boxes.clicks(mouse_pos)
            if back_click:
                self.boxes.back_click(mouse_pos)

            # Display elements
            self.display_elements()

            self.draw_coin_counter()

            self.draw_game_number()

            if self.boxes.game_over:
                pygame.display.flip()  # Ensure the last frame with all letters is displayed
                pygame.time.wait(self.game_over_delay)  # Wait before showing the game over message
                if self.boxes.win:
                    self.display_win_message()
                else:
                    self.display_lose_message()

            pygame.display.flip()
            self.clock.tick(60)

    def display_win_message(self):
        self.win_sound.play()
        start_time = pygame.time.get_ticks()
        duration = 2000  # 2 seconds

        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))  # Black background

            # Create a pulsating effect
            scale = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)

            font = pygame.font.Font(None, int(74 * scale))
            text = font.render('CORRECT!', True, (0, 255, 0))
            text_rect = text.get_rect(center=(640, 360))

            # Add a glowing effect
            glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 255, 0, 100), glow_surf.get_rect(), border_radius=10)
            glow_surf = pygame.transform.scale(glow_surf, (
                int(glow_surf.get_width() * scale), int(glow_surf.get_height() * scale)))
            glow_rect = glow_surf.get_rect(center=(640, 360))

            self.screen.blit(glow_surf, glow_rect)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        CoinManager.add_coins(5)
        self.running = False

    def display_lose_message(self):
        self.lose_sound.play()
        start_time = pygame.time.get_ticks()
        duration = 1500  # 1.5 seconds

        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))  # Black background

            # Create a shaking effect
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)

            font = pygame.font.Font(None, 74)
            text = font.render('WRONG!', True, (255, 0, 0))
            text_rect = text.get_rect(center=(640 + offset_x, 360 + offset_y))

            # Add a flashing effect
            if pygame.time.get_ticks() % 200 < 100:
                self.screen.blit(text, text_rect)

            pygame.display.flip()

        self.running = False

    def draw_game_number(self):
        """ Draw a green circle containing the game number at the top of the screen. """
        circle_color = (0, 255, 0)  # Green color
        text_color = (255, 255, 255)  # White color
        circle_center = (self.screen.get_width() // 2, 60)  # Centered horizontally, and at the top
        circle_radius = 25  # Adjust the size of the circle as needed

        # Draw the green circle
        pygame.draw.circle(self.screen, circle_color, circle_center, circle_radius)

        # Render the game number text
        game_number_text = self.font.render(str(self.game_number), True, text_color)
        text_rect = game_number_text.get_rect(center=circle_center)

        # Draw the text on top of the circle
        self.screen.blit(game_number_text, text_rect)

    def display_elements(self):
        self.screen.blit(self.logo, (1280 - 150, 720 - 150))
        self.screen.blit(self.picture_one, (488, 98))
        self.screen.blit(self.picture_two, (642, 98))
        self.screen.blit(self.picture_three, (488, 252))
        self.screen.blit(self.picture_four, (642, 252))

        pygame.draw.rect(self.screen, (0, 255, 0), self.boxes.hint_button)
        hint_text = self.hint_font.render("Hint (10)", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=self.boxes.hint_button.center)
        self.screen.blit(hint_text, hint_rect)

        for k, rect in enumerate(self.boxes.answer_box_rects):
            self.screen.blit(self.boxes.answer_box[k], rect)

        self.boxes.draw_hint_button(self.screen)

        for j, rect in enumerate(self.boxes.black_box_rects):
            self.screen.blit(self.boxes.black_box[j], rect)

        for i, rect in enumerate(self.boxes.box_rects):
            self.screen.blit(self.boxes.box[i], rect)
            # Display the letters on top of boxes
            if i < 9:
                letter_surface, letter_rect = self.get_answer_letter(i)
                self.screen.blit(letter_surface, letter_rect)
            else:
                letter_surface, letter_rect = self.get_other_letter(i - 9)
                self.screen.blit(letter_surface, letter_rect)

    def get_answer_letter(self, index):
        answer_texts = [
            self.ans_one, self.ans_two, self.ans_three,
            self.ans_four, self.ans_five, self.ans_six,
            self.ans_seven, self.ans_eight, self.ans_nine
        ]
        letter_rect = answer_texts[index].get_rect(center=self.boxes.letter_positions[index].center)
        return answer_texts[index], letter_rect

    def get_other_letter(self, index):
        other_texts = [
            self.others_one, self.others_two, self.others_three,
            self.others_four, self.others_five, self.others_six,
            self.others_seven
        ]
        letter_rect = other_texts[index].get_rect(center=self.boxes.letter_positions[index + 9].center)
        return other_texts[index], letter_rect


if __name__ == "__main__":
    game = Game()
    game.run()