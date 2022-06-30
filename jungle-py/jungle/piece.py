from .constants import RED, BLACK, SQUARE_SIZE
import pygame


class Piece:

    def __init__(self, row, col, color, strength):
        self.row = row
        self.col = col
        self.color = color
        self.strength = strength
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        color = self.color
        strength = self.strength
        img = f"./assets/{color+strength}.png"
        image = pygame.transform.smoothscale(
            pygame.image.load(img), (60, 60))
        win.blit(image, (self.x-30, self.y-30))


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color+self.strength)