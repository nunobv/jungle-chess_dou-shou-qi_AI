import pygame
from .constants import *
from collections import defaultdict
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.black_left = 8
        self.red_strength = self.black_strength = 36
        self.red_captured_distance = self.black_captured_distance = 0
        self.create_board()

    def draw_squares(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                # last argument for border width
                pygame.draw.rect(win, (0, 55, 0), (col*SQUARE_SIZE,
                                 row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):

        self.board = [[0 for i in range(COLS)] for j in range(ROWS)]

        for pos in RED_LOCATIONS:
            anim = ANIMALS[RED_LOCATIONS.index(pos)]
            self.board[pos[1]][pos[0]] = Piece(pos[1], pos[0], RED, anim)

        for pos in BLACK_LOCATIONS:
            anim = ANIMALS[BLACK_LOCATIONS.index(pos)]
            self.board[pos[1]][pos[0]] = Piece(pos[1], pos[0], BLACK, anim)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, posx):
        piece = self.get_piece_from_board(posx[0], posx[1])
        self.board[piece.row][piece.col] = 0
        if piece.color == RED:
            self.red_left -= 1
            self.red_strength -= piece.strength
            self.red_captured_distance += self.getDistance(piece)
        else:
            self.black_left -= 1
            self.black_strength -= piece.strength
            self.black_captured_distance += self.getDistance(piece)

    def winner(self):

        if self.red_left == 0:
            return BLACK
        elif self.black_left == 0:
            return RED

        if self.board[0][3] != 0 and self.get_piece_from_board(0, 3).color != BLACK:
            return RED

        if self.board[8][3] != 0 and self.get_piece_from_board(8, 3).color != RED:
            return BLACK

        return None

    def is_on_board(self, pos):
        if (pos[0] >= 0 and pos[0] < 9 and pos[1] >= 0 and pos[1] < 7):
            return True
        return False

    def is_water(self, pos):
        if (pos in PONDS):
            return True
        else:
            return False

    def is_own_cave(self, piece, pos):
        if piece.color == BLACK:
            return pos == BLACK_DEN
        else:
            return pos == RED_DEN

    def is_team_piece(self, piece, pos):
        other_piece = self.get_piece_from_board(pos[0], pos[1])
        if other_piece:
            return other_piece.color == piece.color
        return False

    def is_enemy_piece(self, piece, other_piece):
        return other_piece.color != piece.color

    def is_on_trap(self, piece):
        return ((piece.row, piece.col) in BLACK_TRAPS or (piece.row, piece.col) in RED_TRAPS)

    def get_piece_from_board(self, row, col):
        if self.board[row][col] != 0:
            return self.board[row][col]

    def can_capture(self, piece, posx):
        target_piece = self.get_piece_from_board(posx[0], posx[1])
        if target_piece:
            if self.is_enemy_piece(piece, target_piece):
                # Rato pode comer elefante
                if (piece.strength == 1 and target_piece.strength == 8 and (not self.is_water((piece.row, piece.col)))):
                    return True
                # Regras das traps generalizadas
                elif (self.is_on_trap(target_piece)):
                    return True
                else:
                    return piece.strength >= target_piece.strength
        return False

    def get_jumps(self, pos):
        return JUMPS.get(pos)

    def has_enemy_piece(self, piece, pos):
        other_piece = self.get_piece_from_board(pos[0], pos[1])
        if other_piece:
            return self.is_enemy_piece(piece, other_piece)
        return False

    def is_rat_between(self, piece, pos):

        is_rat_between = False
        if piece.col == pos[1]:
            # for each column
            cells = list(map(list, zip(*self.board)))[pos[1]]
            _start = min(pos[0], piece.row)
            _end = max(pos[0], piece.row)
            for c in range(_start+1, _end):
                if cells[c] != 0:
                    if cells[c].strength == 1:
                        is_rat_between = True
        else:
            # for each row
            cells = self.board[pos[0]]
            _start = min(pos[1], piece.col)
            _end = max(pos[1], piece.col)
            for c in range(_start+1, _end):
                if cells[c] != 0:
                    if cells[c].strength == 1:
                        is_rat_between = True

        return is_rat_between

    def get_valid_moves(self, piece):

        # print("---------------------")
        # print("PIECE - ", piece.row, piece.col)

        moves = defaultdict(list)
        for mov in DIRECTIONS:

            newPos = (piece.row + mov[0], piece.col + mov[1])
            posx = (piece.row, piece.col)

            # CHECK IF NEW POSITION IS WITHIN BOARD BOUNDERIES
            if not self.is_on_board(newPos):
                continue

            if self.is_own_cave(piece, newPos):
                continue

            # print(f"POSSIBLE MOVE {posx}-", newPos)

            ##### RAT ######
            '''
            Mouse: Mouse is the most interesting piece in this game.
            Although it is the smallest and weakest one, it can kill an elephant.
            Mouse is also the only animal which can go to a water (blue squares) and block lion's or tiger's jumps.
            However, a mouse in a water cannot capture enemy elephant by jumping out of the water, it must make another move and get out of the water first.
            A mouse jumping from a water can eat only another mouse.
            '''
            if(piece.strength == 1):

                other_piece = self.get_piece_from_board(newPos[0], newPos[1])
                if other_piece:
                    if self.is_enemy_piece(piece, other_piece):

                        # RAT CAN EAT ELEPHANT ONLY IF ON LAND
                        if (other_piece.strength == 8 and (not self.is_water(posx))):
                            moves[posx].append(
                                (newPos, self.can_capture(piece, newPos)))
                        elif (other_piece.strength == 1):
                            moves[posx].append(
                                (newPos, self.can_capture(piece, newPos)))
                        elif ((piece.strength >= other_piece.strength) and (not self.is_water((newPos)))):
                            moves[posx].append(
                                (newPos, self.can_capture(piece, newPos)))
                        elif (self.is_on_trap(other_piece)):
                            moves[posx].append(
                                (newPos, self.can_capture(piece, newPos)))

                # RAT cannot move into same team position or to own cave
                elif (not self.is_team_piece(piece, newPos) and not self.is_own_cave(piece, newPos)):
                    moves[posx].append(
                        (newPos, self.can_capture(piece, newPos)))

            ###### OTHER EXCEPT LION AND TIGER ######
            elif((piece.strength > 1 and piece.strength < 6) or piece.strength == 8):

                # print(posx)
                other_piece = self.get_piece_from_board(newPos[0], newPos[1])
                if other_piece:
                    if self.is_enemy_piece(piece, other_piece):

                        # print(piece, other_piece)
                        if ((piece.strength == 8 and other_piece.strength == 1) and (not self.is_water(newPos))):
                            moves[posx].append(
                                (newPos, self.can_capture(piece, newPos)))
                        else:
                            if((piece.strength >= other_piece.strength) and (not self.is_water(newPos))):
                                moves[posx].append(
                                    (newPos, self.can_capture(piece, newPos)))
                            elif (self.is_on_trap(other_piece)):
                                moves[posx].append(
                                    (newPos, self.can_capture(piece, newPos)))

                # Animals cannot move into same team position, to water or to own cave
                elif (not self.is_team_piece(piece, newPos) and not self.is_own_cave(piece, newPos) and not self.is_water(newPos)):
                    moves[posx].append(
                        (newPos, self.can_capture(piece, newPos)))

            # ###### TIGER OR LION ######
            else:
                '''
                Lion can make (as an addition to its normal moves) jumps over a water.
                It means that if it stands next to a blue square (for example B3)
                and the corresponding target square behind the water (B7 in this case) is empty or occupied by an animal it can eat,
                the lion is allowed to perform a jump move.
                There is one exception - it is not possible to jump if a mouse (player's or opponent's) is blocking the jump path.
                Tiger has the same jumping abilities as lion.
                '''
                if not self.is_water(newPos):
                    other_piece = self.get_piece_from_board(
                        newPos[0], newPos[1])
                    if other_piece:
                        if self.is_enemy_piece(piece, other_piece):
                            if((piece.strength >= other_piece.strength) and (not self.is_water(newPos))):
                                moves[posx].append(
                                    (newPos, self.can_capture(piece, newPos)))
                            elif (self.is_on_trap(other_piece)):
                                moves[posx].append(
                                    (newPos, self.can_capture(piece, newPos)))

                    # These Animals cannot move into same team position, to water or to own cave
                    elif (not self.is_team_piece(piece, newPos) and not self.is_own_cave(piece, newPos)):
                        moves[posx].append(
                            (newPos, self.can_capture(piece, newPos)))

                # These Animals can jump into other bank if there is no RAT in the middle of the jump
                else:
                    jumps = self.get_jumps(posx)
                    for j in jumps:
                        if (not self.is_rat_between(piece, j)):
                            if ((not self.is_team_piece(piece, j)) and (not self.has_enemy_piece(piece, j))):
                                moves[posx].append(
                                    (j, self.can_capture(piece, j)))
                            elif (self.has_enemy_piece(piece, j) and (piece.strength >= self.get_piece_from_board(j[0], j[1]).strength)):
                                moves[posx].append(
                                    (j, self.can_capture(piece, j)))
        return moves

    #### EVALUATION FUNCTIONS ####

    def evaluate(self):
        '''
        Avalia apenas no. peças em falta de cada cor
        Assume que MAX = BLACK / MIN = RED
        '''
        return self.black_left - self.red_left

    def evaluate_strength(self):
        '''
        Avalia valor total de cada cor tendo em conta strength das pecas
        Assume que MAX = BLACK / MIN = RED
        '''
        # print("STRENGTH: ", self.black_strength - self.red_strength)
        return self.black_strength - self.red_strength

    def evaluate_distance(self):
        '''
        Avalia valor total de cada cor tendo em conta distancia das pecas ao Den do adversario
        Assume que MAX = BLACK / MIN = RED
        '''

        dist_red = dist_black = 0

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece_from_board(row, col)
                if piece:
                    if piece.color == RED:
                        dist_red += self.getDistance(piece)
                    else:
                        dist_black -= self.getDistance(piece)

        return dist_black + dist_red + (self.red_captured_distance-self.black_captured_distance)

    # soma das distancias das peças ou melhor distancia indiviual?
    def evaluate_strengthAndDistance(self):
        '''
        Avalia valor total de cada cor tendo em conta strength das pecas e distancia das pecas ao Den do adversario
        72 e o score de cada distancia na configuracao inicial

        Assume que MAX = BLACK / MIN = RED
        '''

        dist_red = dist_black = 0

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece_from_board(row, col)
                if piece:
                    if piece.color == RED:
                        dist_red += self.getDistance(piece)
                    else:
                        dist_black -= self.getDistance(piece)

        #print("BLACK DISTANCE: ", dist_black + 72)
        #print("RED DISTANCE: ", dist_red - 72)
        #print("STRENGTH: ", self.black_strength - self.red_strength)

        return (self.black_strength - self.red_strength) + (dist_black + dist_red + self.red_captured_distance-self.black_captured_distance)

    # precisa de retornar o turno, mas o board nao tem esse atributo

    def evaluate_boardHeuristic(self, game):

        n_pieces_turn = 0
        n_pieces_opp = 0
        board_score = 0
        weight = 10000

        # print(self.turn)

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece_from_board(row, col)
                if piece:
                    if piece.color == game.turn:
                        n_pieces_turn += 1

                        if game.turn == RED:
                            board_score -= MAGIC_NUMBERS[piece.strength][8-row][6-col]
                        else:
                            board_score += MAGIC_NUMBERS[piece.strength][row][col]

                        if game.turn == RED:
                            if (abs(weight) > self.getDistance(piece)):
                                weight = -self.getDistance(piece)
                        else:
                            if (abs(weight) > self.getDistance(piece)):
                                weight = self.getDistance(piece)
                    else:
                        n_pieces_opp += 1

        # print("BS", board_score)
        # print("W", weight)
        # print(n_pieces_opp, n_pieces_turn)
        board_score -= weight
        val = (n_pieces_turn - n_pieces_opp) * 100 + \
            (16 - n_pieces_turn - n_pieces_opp)
        if game.turn == RED:
            board_score -= val
        else:
            board_score += val
        # print("D", board_score)

        return board_score

    def evaluate_positionScores(self, game):
        '''
        Avalia valor total de cada cor tendo em conta as matrizes de avaliacao de cada quadrado no board.
        Esta matriz tem em conta a strength de cada peca e um valor empirico associado a cada posicao para cada peca

        Assume que MAX = BLACK / MIN = RED
        '''

        red_board_score = black_board_score = 0

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece_from_board(row, col)
                if piece:
                    if piece.color == RED:
                        red_board_score += POSITION_VALUES[piece.strength][8-row][6-col]
                    else:
                        black_board_score += POSITION_VALUES[piece.strength][row][col]

        board_score = black_board_score - red_board_score

        return board_score

    def getDistance(self, piece):
        if piece.color == RED:
            return abs(piece.row) + abs(piece.col-3)
        else:
            return abs(8-piece.row) + abs(piece.col-3)
