from PIL import Image, ImageSequence
import pygame

from minimax.algorithm import *

from jungle.stage import Stage
from jungle.button import Button, RadioButton
from jungle.constants import *
from jungle.game import Game

import time


FPS = 60
ICON = pygame.image.load('./assets/icon.png')
BG = pygame.image.load('./assets/bg.jpg')

pygame.display.set_caption('Jungle Chess - Dou Shou Qi')
pygame.display.set_icon(ICON)
pygame.init()


class IntroStage(Stage):

    def create_objects(self):

        # SOUNDS
        # pygame.mixer.Sound.play(pygame.mixer.Sound("assets/pokemon_intro.wav"))

        # IMAGES
        self.menubg = pygame.image.load("./assets/bg.jpg").convert()
        self.top_plaque = pygame.transform.scale(pygame.image.load(
            "assets/plaque.png").convert_alpha(), (440, 150))
        self.wood_sign = pygame.transform.smoothscale(
            pygame.image.load('./assets/sign.png').convert_alpha(), (200, 200))
        self.side_sign = pygame.transform.smoothscale(pygame.image.load(
            './assets/wood-sign-side.png').convert_alpha(), (300, 100))

        # Texts
        self.title = self.font_m.render('JUNGLE CHESS', False, (0, 100, 0))
        self.footer_1 = self.font_s.render(
            'MECD06 - Artificial Intelligence', False, (255, 196, 0))
        self.andre = self.font_s.render('André Afonso', False, (255, 196, 0))
        self.nuno = self.font_s.render(
            'Nuno Vasconcelos', False, (255, 196, 0))
        self.feup = self.font_s.render('FEUP - 2022', False, (255, 196, 0))
        self.press_start = self.font_m.render(
            'PRESS SPACE TO START', False, (255, 0, 0))
        self.rules = self.font_s.render('HOW TO PLAY?', False, (0, 55, 0))

        self.font_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.font_fade, 400)
        self.show_text = True

        # CHILD STAGES
        self.stage_rules = RulesStage(self.screen, self.config)

    def draw(self, surface):

        # IMAGES
        surface.blit(self.menubg, (0, 0))
        surface.blit(self.jungle_gif, (0, 0))
        surface.blit(self.top_plaque, (120, -10))
        surface.blit(self.title, (230, 85))
        surface.blit(self.wood_sign, (470, 410))

        # BUTTONS
        self.rules_btn = Button(0, 400, self.side_sign, 1)
        if self.rules_btn.draw(surface):
            self.stage_rules.mainloop()

        # TEXTS
        surface.blit(self.footer_1, (50, 620))
        surface.blit(self.andre, (500, 440))
        surface.blit(self.nuno, (475, 470))
        surface.blit(self.feup, (500, 620))
        surface.blit(self.rules, (60, 475))

        if self.show_text:
            surface.blit(self.press_start, self.press_start.get_rect(
                center=surface.get_rect().center))

        pygame.display.update()

    def handle_event(self, event):

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                pygame.mixer.quit()
                self.exit()

        if event.type == self.font_fade:
            self.show_text = not self.show_text


class RulesStage(Stage):

    def create_objects(self):

        # IMAGES
        self.menubg = pygame.image.load("./assets/bg.jpg").convert()
        self.jungle_gif = pygame.image.load(
            "./assets/jungle.gif").convert_alpha()
        self.top_plaque = pygame.transform.scale(pygame.image.load(
            "assets/plaque.png").convert_alpha(), (440, 150))
        self.back_arrow = pygame.transform.scale(pygame.image.load(
            "assets/back-arrow.png").convert_alpha(), (140, 60))

        self.header = self.font_m.render(
            'JUNGLE CHESS RULES', False, (255, 255, 255))

        self.p1 = self.font_s.render(
            'Each player has 8 pawns, numbered 1 to 8,', False, (255, 255, 255))
        self.p2 = self.font_s.render(
            'according to their strength', False, (255, 255, 255))

        self.p3 = self.font_s.render(
            'Three types of special squares are indicated:', False, (255, 255, 255))
        self.p4 = self.font_s.render(
            '(Lake, Den, Trap)', False, (255, 255, 255))
        self.p5 = self.font_s.render(
            'All others are normal', False, (255, 255, 255))

        self.p6 = self.font_s.render(
            'Each player possesses a Den.', False, (255, 255, 255))
        self.p7 = self.font_s.render(
            'It is illegal to move your own pawn to your Den.', False, (255, 255, 255))
        self.p8 = self.font_s.render(
            'As soon as an enemy Den is occupied by', False, (255, 255, 255))
        self.p9 = self.font_s.render(
            'an adversary\'s pawn, the game ends.', False, (255, 255, 255))

        self.p10 = self.font_s.render(
            'Each of the two lakes contains 6 squares.', False, (255, 255, 255))
        self.p11 = self.font_s.render(
            'The lion and the tiger may jump over the lake.', False, (255, 255, 255))
        self.p12 = self.font_s.render(
            'But only the rat can swim through them.', False, (255, 255, 255))

        self.p13 = self.font_s.render(
            'Surrounding each Den are three Traps.', False, (255, 255, 255))
        self.p14 = self.font_s.render(
            'Each animal in a trap is considered to have 0 strength.', False, (255, 255, 255))
        self.p15 = self.font_s.render(
            'Therefore it cannot defend itself.', False, (255, 255, 255))

    def draw(self, surface):

        surface.blit(self.menubg, (0, 0))
        surface.blit(self.header, (180, 50))

        surface.blit(self.p1, (50, 150))
        surface.blit(self.p2, (50, 165))

        surface.blit(self.p3, (50, 220))
        surface.blit(self.p4, (50, 235))
        surface.blit(self.p5, (50, 250))

        surface.blit(self.p6, (50, 285))
        surface.blit(self.p7, (50, 300))
        surface.blit(self.p8, (50, 315))
        surface.blit(self.p9, (50, 330))

        surface.blit(self.p10, (50, 385))
        surface.blit(self.p11, (50, 400))
        surface.blit(self.p12, (50, 415))

        surface.blit(self.p13, (50, 460))
        surface.blit(self.p14, (50, 475))
        surface.blit(self.p15, (50, 490))

        # BUTTONS
        self.back_btn = Button(50, 550, self.back_arrow, 1)
        if self.back_btn.draw(surface):
            self.exit()

        pygame.display.update()


class MenuStage(Stage):

    def create_objects(self):

        self.menubg = pygame.image.load("./assets/bg.jpg").convert()
        self.jungle_gif = pygame.image.load(
            "./assets/jungle.gif").convert_alpha()
        self.game_type = pygame.transform.scale(pygame.image.load(
            "assets/plaque.png").convert_alpha(), (340, 100))
        self.p1 = pygame.transform.smoothscale(
            pygame.image.load("./assets/p1.png").convert(), (140, 40))
        self.p2 = pygame.transform.smoothscale(
            pygame.image.load("./assets/p2.png").convert(), (140, 40))
        self.p1ai = pygame.transform.smoothscale(
            pygame.image.load("./assets/p1ai.png").convert(), (140, 40))
        self.p2ai = pygame.transform.smoothscale(
            pygame.image.load("./assets/p2ai.png").convert(), (140, 40))

        self.settings = self.font_m.render('SETTINGS', False, (40, 20, 0))
        self.save = self.font_m.render('START', False, (40, 20, 0))

        self.P1Buttons = [
            RadioButton(100, 170, 120, 40, self.font_s, "HUMAN"),
            RadioButton(100, 230, 120, 40, self.font_s, "AI"),
        ]
        for rb in self.P1Buttons:
            rb.setRadioButtons(self.P1Buttons)
        self.p1group = pygame.sprite.Group(self.P1Buttons)
        self.P1Buttons[0].clicked = True

        self.P2Buttons = [
            RadioButton(500, 170, 120, 40, self.font_s, "HUMAN"),
            RadioButton(500, 230, 120, 40, self.font_s, "AI"),
        ]
        for rb in self.P2Buttons:
            rb.setRadioButtons(self.P2Buttons)
        self.p2group = pygame.sprite.Group(self.P2Buttons)
        self.P2Buttons[1].clicked = True

        self.P1AIButtons = [
            RadioButton(100, 370, 120, 40, self.font_s, "EASY"),
            RadioButton(100, 430, 120, 40, self.font_s, "MEDIUM"),
            RadioButton(100, 490, 120, 40, self.font_s, "HARD"),
        ]
        for rb in self.P1AIButtons:
            rb.setRadioButtons(self.P1AIButtons)
        self.p1aigroup = pygame.sprite.Group(self.P1AIButtons)
        self.P1AIButtons[0].clicked = True

        self.P2AIButtons = [
            RadioButton(500, 370, 120, 40, self.font_s, "EASY"),
            RadioButton(500, 430, 120, 40, self.font_s, "MEDIUM"),
            RadioButton(500, 490, 120, 40, self.font_s, "HARD"),
        ]
        for rb in self.P2AIButtons:
            rb.setRadioButtons(self.P2AIButtons)
        self.p2aigroup = pygame.sprite.Group(self.P2AIButtons)
        self.P2AIButtons[0].clicked = True

        self.config = {
            'P1_TYPE': 0,
            'P2_TYPE': 1,
            'P1AI_LEVEL': 0,
            'P2AI_LEVEL': 0,
        }

    def draw(self, surface):

        surface.blit(self.menubg, (0, 0))
        surface.blit(self.jungle_gif, (0, 0))
        surface.blit(self.game_type, (170, -10))
        surface.blit(self.p1, (90, 100))
        surface.blit(self.p2, (490, 100))
        surface.blit(self.p1ai, (90, 300))
        surface.blit(self.p2ai, (490, 300))

        self.p1group.draw(surface)
        self.p2group.draw(surface)
        self.p1aigroup.draw(surface)
        self.p2aigroup.draw(surface)

        confirm_btn = Button(270, 550, GREEN_BTN, 1)
        if confirm_btn.draw(surface):
            for i, rb in enumerate(self.P1Buttons):
                if rb.clicked:
                    self.config['P1_TYPE'] = i

            for i, rb in enumerate(self.P2Buttons):
                if rb.clicked:
                    self.config['P2_TYPE'] = i

            for i, rb in enumerate(self.P1AIButtons):
                if rb.clicked:
                    self.config['P1AI_LEVEL'] = i

            for i, rb in enumerate(self.P2AIButtons):
                if rb.clicked:
                    self.config['P2AI_LEVEL'] = i

            self.stage_game = GameStage(self.screen, self.config)
            self.stage_game.mainloop()

        surface.blit(self.settings, (270, 50))
        surface.blit(self.save, (300, 560))
        pygame.display.update()

    def handle_event(self, event):

        self.p1group.update(event)
        self.p2group.update(event)
        self.p1aigroup.update(event)
        self.p2aigroup.update(event)


class GameStage(Stage):

    def create_objects(self):

        self.player_turn = self.font_m.render(
            'Player:', False, (255, 255, 255))
        self.game = Game(self.screen)
        self.hint_text = self.font_s.render('HINT', False, (0, 0, 0))
        self.reset_text = self.font_s.render('RESET', False, (0, 0, 0))
        self.quit_text = self.font_s.render('QUIT', False, (0, 0, 0))

        self.end_game = EndStage(self.screen, self.config)

    def draw(self, surface):

        surface.blit(BG, (0, 0))
        surface.blit(BOARD, (0, 0))
        surface.blit(RED_SCORE, (510, 70))
        surface.blit(BLACK_SCORE, (510, 120))

        surface.blit(self.player_turn, (510, 20))

        self.red_score = self.font_m.render(
            f'{8-self.game.board.black_left}', False, (255, 255, 255))
        self.black_score = self.font_m.render(
            f'{8-self.game.board.red_left}', False, (255, 255, 255))
        surface.blit(self.red_score, (650, 75))
        surface.blit(self.black_score, (650, 125))

        self.exit_btn = Button(625, 595, RED_BTN, 1)
        self.reset_btn = Button(
            525, 595, pygame.transform.smoothscale(YELLOW_BTN, (80, 28)), 1)
        self.hint_btn = Button(525, 545, BLUE_BTN, 1)

        surface.blit(BLACKBOARD, (510, 170))

        if self.exit_btn.draw(surface):
            print('Goodbye...')
            self.is_running = False

        if (self.hint_btn.draw(surface) and (self.config['P1_TYPE'] == 0 or self.config['P2_TYPE'] == 0)):
            depth = self.config['P1AI_LEVEL'] + \
                1 if not self.config['P1_TYPE'] == 0 else self.config['P2AI_LEVEL'] + 1
            if (self.config['P1_TYPE'] == 0 and self.config['P2_TYPE'] == 0):
                is_max = True if self.game.turn == BLACK else False
            else:
                is_max = True if self.config['P2_TYPE'] == 1 else False

            curr_board = self.game.get_board()
            value, new_board = minimax(
                curr_board, depth, is_max, self.game, "squares_distance")
            first = [list(map(str, i)) for i in curr_board.board]
            second = [list(map(str, i)) for i in new_board.board]
            idx = []
            for i in range(ROWS):
                for j in range(COLS):
                    if first[i][j] != second[i][j]:
                        idx.append((i, j))

                        if first[i][j] == '0':
                            mov = "right_down"
                        else:
                            mov = "left_up"

            if mov == "left_up":
                self.game.hint_piece = idx[1]
                self.game.hint_move = idx[0]
            else:
                self.game.hint_piece = idx[0]
                self.game.hint_move = idx[1]
            print("HINT:", str(idx[1]) + ">>" + str(idx[0]))

        if self.reset_btn.draw(surface):
            self.game.reset()
            print("GAME RESET!")

        surface.blit(self.hint_text, (540, 555))
        surface.blit(self.quit_text, (640, 605))
        surface.blit(self.reset_text, (535, 605))

    def update(self):

        if (self.game.turn == RED and self.config['P1_TYPE'] == 1):
            # value, new_board = minimax(
            #     self.game.get_board(), self.config['P1AI_LEVEL'] + 1, False, self.game, "positionScores")
            # value, new_board = alphabeta(self.game.get_board(
            # ), self.config['P1AI_LEVEL'] + 2, -9999999, 9999999, False, self.game, "positionScores")
            # value, new_board = alphabeta_move_ordering(self.game.get_board(
            # ), self.config['P1AI_LEVEL'] + 2, -9999999, 9999999, False, self.game, "positionScores")
            # # value, new_board = iterative_deepening_minimax(self.game.get_board(
            # ), self.config['P1AI_LEVEL'] + 20, False, self.game, "positionScores", 0.1)
            # value, new_board = iterative_deepening_alphabeta(self.game.get_board(
            # ), self.config['P1AI_LEVEL'] + 20, -9999999, 9999999, False, self.game, "positionScores", 0.5)
            value, new_board = iterative_deepening_alphabeta_move_ordering(self.game.get_board(
            ), self.config['P1AI_LEVEL'] + 20, -9999999, 9999999, False, self.game, "positionScores", 0.5)

            # print("RED", new_board.board)
            #print("RED FINAL EVAL: ", value)
            self.game.ai_move(new_board)

        if (self.game.turn == BLACK and self.config['P2_TYPE'] == 1):
            start = pygame.time.get_ticks()
            # value, new_board = minimax(
            #     self.game.get_board(), self.config['P2AI_LEVEL'] + 1, True, self.game, "positionScores")
            # value, new_board = alphabeta(self.game.get_board(
            # ), self.config['P2AI_LEVEL'] + 2, -9999999, 9999999, True, self.game, "positionScores")
            # value, new_board = alphabeta_move_ordering(self.game.get_board(
            # ), self.config['P2AI_LEVEL'] + 2, -9999999, 9999999, True, self.game, "positionScores")
            # value, new_board = iterative_deepening_minimax(self.game.get_board(
            # ), self.config['P2AI_LEVEL'] + 20, True, self.game, "positionScores", 0.1)
            # value, new_board = iterative_deepening_alphabeta(self.game.get_board(
            # ), self.config['P2AI_LEVEL'] + 20, -9999999, 9999999, True, self.game, "positionScores", 0.5)
            value, new_board = iterative_deepening_alphabeta_move_ordering(self.game.get_board(
            ), self.config['P2AI_LEVEL'] + 20, -9999999, 9999999, True, self.game, "positionScores", 0.5)

            # print("BLACK", new_board.board)
            end = pygame.time.get_ticks()
            #print("BLACK FINAL EVAL: ", value)
            print('BLACK AI eval time: {}ms'.format(end-start))
            self.game.ai_move(new_board)

        if self.game.winner() != None:
            print("WINNER IS", self.game.winner())
            self.config['winner'] = self.game.winner()
            self.end_game.mainloop()
            self.is_running = False
            # self.is_running = False

        self.game.update()

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            self.is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.reset()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.within_board_pixels(pos):
                row, col = self.get_row_col_from_mouse(pos)
                self.game.select(row, col)

        # pygame.time.delay(500)

        # breakpoint()


class EndStage(Stage):

    def create_objects(self):

        self.menubg = pygame.image.load("./assets/bg.jpg").convert()
        self.jungle_gif = pygame.image.load(
            "./assets/jungle.gif").convert_alpha()
        self.red_wins = pygame.transform.smoothscale(pygame.image.load(
            './assets/red-wins.png').convert_alpha(), (300, 80))
        self.black_wins = pygame.transform.smoothscale(pygame.image.load(
            './assets/black-wins.png').convert_alpha(), (300, 80))
        self.game_over = self.font_m.render('GAME OVER!', False, (155, 0, 0))
        self.reset_text = self.font_m.render('RESTART', False, (40, 20, 0))

        self.img_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.img_fade, 400)
        self.show_winner = True

    def draw(self, surface):

        # IMAGES
        surface.blit(self.menubg, (0, 0))
        surface.blit(self.jungle_gif, (0, 0))

        # BUTTONS
        self.reset_btn = Button(
            270, 550, pygame.transform.smoothscale(YELLOW_BTN, (170, 40)), 1)
        if self.reset_btn.draw(surface):
            self.exit()

        # TEXTS
        surface.blit(self.game_over, (surface.get_rect().center[0] - 100, 200))
        surface.blit(self.reset_text, (surface.get_rect().center[0] - 80, 560))

        if self.config.get('winner') == 10:
            if self.show_winner:
                surface.blit(self.red_wins, self.red_wins.get_rect(
                    center=surface.get_rect().center))
        elif self.config.get('winner') == 20:
            if self.show_winner:
                surface.blit(self.black_wins, self.black_wins.get_rect(
                    center=surface.get_rect().center))

        pygame.display.update()

    def handle_event(self, event):
        if event.type == self.img_fade:
            self.show_winner = not self.show_winner


def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    if pilImage.format == 'GIF' and pilImage.is_animated:
        for frame in ImageSequence.Iterator(pilImage):
            pygameImage = pilImageToSurface(frame.convert('RGBA'))
            frames.append(pygameImage)
    else:
        frames.append(pilImageToSurface(pilImage))
    return frames


class ExitStage(Stage):

    def create_objects(self):
        self.text = self.font_m.render("GOOD BYE", True, (252, 186, 3))
        self.menubg = pygame.image.load("./assets/bg.jpg").convert()
        self.monkey_frames = loadGIF("./assets/monkey.gif")
        self.current_frame = 0

        self.img_fade = pygame.USEREVENT + 1
        pygame.time.set_timer(self.img_fade, 30)
        self.update_gif = True

    def draw(self, surface):

        surface.blit(self.menubg, (0, 0))

        rect = self.monkey_frames[self.current_frame].get_rect(
            center=(350, 500))
        surface.blit(self.monkey_frames[self.current_frame], rect)
        self.current_frame = (self.current_frame + 1) % len(self.monkey_frames)

        surface.blit(self.text, (surface.get_rect().center[0] - 100, 150))
        pygame.display.update()

    def handle_event(self, event):
        pass


class App():

    # --- init ---
    def __init__(self):

        pygame.init()
        screen = pygame.display.set_mode((720, HEIGHT))
        config = {}

        stage = IntroStage(screen, config)
        stage.mainloop()

        stage = MenuStage(screen, config)
        stage.mainloop()

        stage = ExitStage(screen, config)
        stage.mainloop()

        pygame.quit()


if __name__ == '__main__':
    App()
