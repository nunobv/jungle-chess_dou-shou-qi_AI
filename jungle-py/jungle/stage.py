import pygame
from jungle.constants import *

class Stage:

    # --- (global) variables ---

        # empty

    # --- init ---

    def __init__(self, screen, config):

        self.screen = screen
        self.config = config

        self.screen_rect = screen.get_rect()

        self.clock = pygame.time.Clock()
        self.is_running = False

        self.jungle_gif = pygame.image.load("./assets/jungle.gif").convert_alpha()
        self.font_b = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 42)
        self.font_m = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 22)
        self.font_s = pygame.font.Font("./assets/PressStart2P-Regular.ttf", 12)

        self.widgets = []

        self.create_objects()


    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def within_board_pixels(self, pos):
        return (pos[0] < WIDTH and pos[1] < (HEIGHT - 15))

    def quit(self):
        pass

    # --- objects ---

    def create_objects(self):
        pass

    # --- functions ---

    def handle_event(self, event):

        '''
        self.player.handle_event(event)
        '''

        '''
        for widget in self.widgets:
            widget.handle_event(event)
        '''

    def update(self, ):

        '''
        self.player.update()
        '''

        '''
        for widget in self.widgets:
            widget.update()
        '''

    def draw(self, surface):

        #surface.fill(BLACK)

        '''
        self.player.draw(surface)
        '''

        '''
        for widget in self.widgets:
            widget.draw(surface)
        '''

        #pygame.display.update()    

    def exit(self):
        self.is_running = False

    def mainloop(self):

        self.is_running = True
        while self.is_running:
            # --- events ---
            for event in pygame.event.get():

                # --- global events ---
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False

                # --- objects events ---
                self.handle_event(event)

            # --- updates ---
            self.update()

            # --- draws ---
            self.screen.fill(BLACK)
            self.draw(self.screen)
            # pygame.display.update()

            # --- FPS ---
            self.clock.tick(30)

        self.quit()