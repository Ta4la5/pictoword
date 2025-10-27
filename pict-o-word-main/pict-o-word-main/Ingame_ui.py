import pygame

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
        game.boxes = Boxes()  # Reinitialize the boxes
        game.run()  # Restart the game loop


class Boxes:
    def __init__(self):
        self.A1 = (442 + 6, 430 + 4)
        self.A2 = (486 + 6, 430 + 4)
        self.A3 = (530 + 6, 430 + 4)
        self.A4 = (574 + 6, 430 + 4)
        self.A5 = (618 + 6, 430 + 4)
        self.A6 = (662 + 6, 430 + 4)
        self.A7 = (706 + 6, 430 + 4)
        self.A8 = (750 + 6, 430 + 4)
        self.A9 = (794 + 6, 430 + 4)

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

        self.answer_boxX = [442, 486, 530, 574, 618, 662, 706, 750, 794]
        self.answer_boxY = [430, 430, 430, 430, 430, 430, 430, 430, 430]
        self.answer_box = [pygame.image.load("sav.jpg") for _ in range(9)]

        self.box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.boxX, self.boxY)]
        self.black_box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.black_boxX, self.black_boxY)]
        self.answer_box_rects = [pygame.Rect(x, y, 40, 40) for x, y in zip(self.answer_boxX, self.answer_boxY)]

        self.letter_positions = self.box_rects[:]

        self.movement_positions = {
            0: (442, 430),
            1: (486, 430),
            2: (530, 430),
            3: (574, 430),
            4: (618, 430),
            5: (662, 430),
            6: (706, 430),
            7: (750, 430),
            8: (794, 430),
        }

        self.back_value = []
        self.count = 0
        self.tries_left = 3

    def check_win(self):
        print("Checking win")
        correct_positions = [
            (442, 430), (486, 430), (530, 430), (574, 430), (618, 430),
            (662, 430), (706, 430), (750, 430), (794, 430)
        ]

        current_positions = [rect.topleft for rect in self.box_rects[:9]]
        return current_positions == correct_positions

    def display_win_message(self):
        font = pygame.font.Font(None, 74)
        text = font.render('You Win!', True, (0, 255, 0))
        game.screen.blit(text, (540, 360))
        pygame.display.flip()
        pygame.time.wait(2000)
        Reset.reset_game(game)

    def display_lose_message(self):
        font = pygame.font.Font(None, 74)
        text = font.render('You Lose!', True, (255, 0, 0))
        game.screen.blit(text, (540, 360))
        pygame.display.flip()
        pygame.time.wait(2000)
        Reset.reset_game(game)

    def clicks(self, mouse_pos):
        for i, rect in enumerate(self.box_rects):
            if rect.collidepoint(mouse_pos) and self.count < len(self.movement_positions) and mouse_pos[1] > 490:
                pos = self.movement_positions[self.count]
                self.box_rects[i] = pygame.Rect(*pos, 40, 40)
                self.letter_positions[i] = pygame.Rect(*pos, 40, 40)  # Update letter position
                self.count += 1
                self.back_value.append(i)

                # Check if all answer slots are filled
                if self.count == len(self.movement_positions):
                    if self.check_win():
                        print("Winner")
                        self.display_win_message()
                    else:
                        self.tries_left -= 1
                        if self.tries_left <= 0:
                            print("You lose")
                            self.display_lose_message()
                        else:
                            print("Incorrect, please try again.")
                return

    def back_click(self, mouse_pos):
        if self.count > 0:
            last_index = self.back_value.pop()
            self.box_rects[last_index] = pygame.Rect(self.boxX[last_index], self.boxY[last_index], 40, 40)
            self.letter_positions[last_index] = pygame.Rect(self.boxX[last_index], self.boxY[last_index], 40, 40)  # Update letter position
            self.count -= 1


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = pygame.image.load('edc.jpg')
        self.logo = pygame.image.load("logs-removebg-preview.png")
        self.picture_one = pygame.image.load("hard/Adventure/a.jpg")
        self.picture_two = pygame.image.load("hard/Adventure/b.jpg")
        self.picture_three = pygame.image.load("hard/Adventure/c.jpg")
        self.picture_four = pygame.image.load("hard/Adventure/d.jpg")

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.ans_one = self.font.render("A", True, (0, 0, 0))
        self.ans_two = self.font.render("D", True, (0, 0, 0))
        self.ans_three = self.font.render("V", True, (0, 0, 0))
        self.ans_four = self.font.render("E", True, (0, 0, 0))
        self.ans_five = self.font.render("N", True, (0, 0, 0))
        self.ans_six = self.font.render("T", True, (0, 0, 0))
        self.ans_seven = self.font.render("U", True, (0, 0, 0))
        self.ans_eight = self.font.render("R", True, (0, 0, 0))
        self.ans_nine = self.font.render("E", True, (0, 0, 0))

        self.others_one = self.font.render("P", True, (0, 0, 0))
        self.others_two = self.font.render("M", True, (0, 0, 0))
        self.others_three = self.font.render("I", True, (0, 0, 0))
        self.others_four = self.font.render("O", True, (0, 0, 0))
        self.others_five = self.font.render("H", True, (0, 0, 0))
        self.others_six = self.font.render("R", True, (0, 0, 0))
        self.others_seven = self.font.render("S", True, (0, 0, 0))

        self.boxes = Boxes()

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
                    if pygame.mouse.get_pressed()[0]:  # Left click
                        click = True
                    if pygame.mouse.get_pressed()[2]:  # Right click
                        back_click = True

            if click:
                self.boxes.clicks(mouse_pos)
            if back_click:
                self.boxes.back_click(mouse_pos)

            # Display elements
            self.display_elements()

            pygame.display.flip()
            self.clock.tick(60)

    def display_elements(self):
        self.screen.blit(self.logo, (1280 - 150, 720 - 150))
        self.screen.blit(self.picture_one, (488, 98))
        self.screen.blit(self.picture_two, (642, 98))
        self.screen.blit(self.picture_three, (488, 252))
        self.screen.blit(self.picture_four, (642, 252))

        for k, rect in enumerate(self.boxes.answer_box_rects):
            self.screen.blit(self.boxes.answer_box[k], rect)

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