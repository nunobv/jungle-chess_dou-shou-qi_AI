import pygame
from .constants import *
from jungle.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        if self.selected:
            self.draw_valid_moves(self.valid_moves)
            self.draw_selected(self.selected)
        if self.hint_piece and self.hint_move:
            self.draw_hint()            
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.hint_piece = None
        self.hint_move = None        
        self.board = Board()
        self.turn = FIRST_MOVE
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        valids = self.valid_moves[(self.selected.row, self.selected.col)]
        for m in valids:
            if m[0] == (row, col):
                if self.selected and piece == 0:
                    self.board.move(self.selected, row, col)
                    # return True
                if m[1]:
                    self.board.remove((row, col))
                    self.board.move(self.selected, row, col)
                self.change_turn()
                return True
        else:
            return False


    def draw_valid_moves(self, moves):
        for k,v in moves.items():
            for m in v:
                row, col = m[0]
                self.win.blit(ALLOWED_MOVES, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10))

    def draw_selected(self, selected):
        if selected:
            row, col = selected.row, selected.col
            self.win.blit(SELECTED, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_hint(self):
        self.win.blit(HINT_PIECE, (self.hint_piece[1] * SQUARE_SIZE, self.hint_piece[0] * SQUARE_SIZE))
        self.win.blit(HINT_POS, (self.hint_move[1] * SQUARE_SIZE + 10, self.hint_move[0] * SQUARE_SIZE + 10))

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = BLACK
        else:
            self.turn = RED
        self.selected = None
        self.hint_piece = None
        self.hint_move = None        

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()