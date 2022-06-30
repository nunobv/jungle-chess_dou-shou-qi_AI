from copy import deepcopy
from jungle.constants import RED, BLACK
import pygame
import time


def minimax(position, depth, max_player, game, heuristic):
    if depth == 0 or position.winner() != None:
        if heuristic == "evaluate_strength":
            return position.evaluate_strength(), position
        if heuristic == "distance":
            return position.evaluate_distance(), position
        if heuristic == "strength_distance":
            return position.evaluate_strengthAndDistance(), position
        if heuristic == "squares_distance":
            return position.evaluate_boardHeuristic(game), position
        if heuristic == "positionScores":
            return position.evaluate_positionScores(game), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, False, game, heuristic)[0]
            # maxEval = max(maxEval, evaluation)
            # # print("BLACK EVAL: ", evaluation)
            # if maxEval == evaluation:
            #     best_move = move

            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game, heuristic)[0]
            # minEval = min(minEval, evaluation)
            # # print("RED EVAL: ", evaluation)
            # if minEval == evaluation:
            #     best_move = move

            if evaluation < minEval:
                minEval = evaluation
                best_move = move

        return minEval, best_move


def alphabeta(position, depth, alpha, beta, max_player, game, heuristic):
    if depth == 0 or position.winner() != None:
        if heuristic == "evaluate_strength":
            return position.evaluate_strength(), position
        if heuristic == "distance":
            return position.evaluate_distance(), position
        if heuristic == "strength_distance":
            return position.evaluate_strengthAndDistance(), position
        if heuristic == "squares_distance":
            return position.evaluate_boardHeuristic(game), position
        if heuristic == "positionScores":
            return position.evaluate_positionScores(game), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = alphabeta(move, depth-1, alpha,
                                   beta, False, game, heuristic)[0]

            if evaluation > maxEval:
                best_move = move
                maxEval = evaluation

            alpha = max(alpha, maxEval)
            #print("BLACK EVAL: ", move.board, evaluation)

            if beta <= alpha:
                # print("BLACK (MAX) pruning")
                return maxEval, best_move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = alphabeta(move, depth-1, alpha,
                                   beta, True, game, heuristic)[0]

            if evaluation < minEval:
                best_move = move
                minEval = evaluation

            beta = min(beta, evaluation)
            #print("RED EVAL: ", move.board, evaluation)

            if beta <= alpha:
                # print("RED (MIN) pruning")
                return minEval, best_move

        return minEval, best_move


def alphabeta_move_ordering(position, depth, alpha, beta, max_player, game, heuristic):
    if depth == 0 or position.winner() != None:
        if heuristic == "evaluate_strength":
            return position.evaluate_strength(), position
        if heuristic == "distance":
            return position.evaluate_distance(), position
        if heuristic == "strength_distance":
            return position.evaluate_strengthAndDistance(), position
        if heuristic == "squares_distance":
            return position.evaluate_boardHeuristic(game), position
        if heuristic == "positionScores":
            return position.evaluate_positionScores(game), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves_ordering(position, BLACK, game):
            evaluation = alphabeta_move_ordering(move, depth-1, alpha,
                                                 beta, False, game, heuristic)[0]
            if evaluation > maxEval:
                best_move = move
                maxEval = evaluation

            alpha = max(alpha, maxEval)
            #print("BLACK EVAL: ", move.board, evaluation)

            if beta <= alpha:
                # print("BLACK (MAX) pruning")
                return maxEval, best_move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves_ordering(position, RED, game):
            evaluation = alphabeta_move_ordering(move, depth-1, alpha,
                                                 beta, True, game, heuristic)[0]
            if evaluation < minEval:
                best_move = move
                minEval = evaluation

            beta = min(beta, evaluation)
            #print("RED EVAL: ", move.board, evaluation)

            if beta <= alpha:
                # print("RED (MIN) pruning")
                return minEval, best_move

        return minEval, best_move


def iterative_deepening_minimax(position, maxdepth, max_player, game, heuristic, timeout):

    time_start = time.time()
    elapsed_time = 0

    for depth in range(1, maxdepth + 1):
        current_time = time.time()
        elapsed_time = current_time - time_start
        if elapsed_time >= timeout:
            break
        if max_player:
            value, new_board = minimax(
                position, depth, max_player, game, heuristic)
        else:
            value, new_board = minimax(
                position, depth, max_player, game, heuristic)

    return value, new_board


def iterative_deepening_alphabeta(position, maxdepth, alpha, beta, max_player, game, heuristic, timeout):

    time_start = time.time()
    elapsed_time = 0

    for depth in range(1, maxdepth + 1):
        current_time = time.time()
        elapsed_time = current_time - time_start
        if elapsed_time >= timeout:
            break
        if max_player:
            value, new_board = alphabeta(
                position, depth, alpha, beta, max_player, game, heuristic)
        else:
            value, new_board = alphabeta(
                position, depth, alpha, beta, max_player, game, heuristic)

    return value, new_board


def iterative_deepening_alphabeta_move_ordering(position, maxdepth, alpha, beta, max_player, game, heuristic, timeout):

    time_start = time.time()
    elapsed_time = 0

    for depth in range(1, maxdepth + 1):
        current_time = time.time()
        elapsed_time = current_time - time_start
        if elapsed_time >= timeout:
            break
        if max_player:
            value, new_board = alphabeta_move_ordering(
                position, depth, alpha, beta, max_player, game, heuristic)
        else:
            value, new_board = alphabeta_move_ordering(
                position, depth, alpha, beta, max_player, game, heuristic)

    print("DEPTH : ", depth)
    print("TEMPO: ", elapsed_time)
    #print("BEST VAL: ", value)
    return value, new_board


def simulate_move(piece, move, board, game, capture):
    if capture:
        board.remove((move[0], move[1]))
    board.move(piece, move[0], move[1])
    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for piece_posx, possible_moves in valid_moves.items():
            for m, capture in possible_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                if temp_piece != 0:
                    new_board = simulate_move(
                        temp_piece, m, temp_board, game, capture)
                    moves.append(new_board)
    # print("MOVES:\n", moves)
    return moves


def get_all_moves_ordering(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        # ordenar moves de uma peca: capturas primeiro
        for piece_posx, possible_moves in valid_moves.items():
            for m, capture in possible_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                if temp_piece != 0:
                    new_board = simulate_move(
                        temp_piece, m, temp_board, game, capture)
                    moves.append((capture, piece.strength, new_board))
    #print("MOVES:\n", moves)
    moves_sorted = deepcopy(moves)
    moves_sorted = sorted(moves_sorted, key=lambda element: (
        element[0], element[1]), reverse=True)

    return [x[2] for x in moves_sorted]
