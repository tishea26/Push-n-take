import copy
from engine.enums import Tile
from engine.board import Board
from engine.pawn import Pawn

def evaluate(board, color):
    if color == Tile.WHITE:
        enemy = Tile.PURPLE
    else:
        enemy = Tile.WHITE
    score = board.nb_pawn(color) - board.nb_pawn(enemy)

    for pid, pawn in board.pawns.items():
        if pawn.color == color:
            if color == Tile.WHITE:
                score += pawn.i / board.rows
            else:
                score += (board.rows - 1 - pawn.i) / board.rows
                
    if board.win(color):
        score += 1000
    elif board.win(enemy):
        score -= 1000
    return score

def minimax(board, color, depth, alpha=-float('inf'), beta=float('inf'), maximizing=True):

    if depth == 0 or board.win(Tile.WHITE) or board.win(Tile.PURPLE):
        return evaluate(board, color), None

    best_move = None
    moves = []

    if maximizing:
        player = color
    else:
        if color == Tile.WHITE:
            player = Tile.PURPLE
        else:
            player = Tile.WHITE

    for pid, pawn in board.pawns.items():
        if pawn.color != player:
            continue
        for m in board.possible_moves(pawn.id):
            action_type, ni, nj = m
            moves.append((pid, action_type, ni, nj))

    if len(moves) == 0:
        return evaluate(board, color), None

    if maximizing:
        max_eval = -float('inf')
        for move in moves:
            pid, action_type, ni, nj = move
            board_copy = copy.deepcopy(board)
            board_copy.move_pawn(pid, ni, nj)
            eval_score, _ = minimax(board_copy, color, depth-1, alpha, beta, maximizing=False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break 
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            pid, action_type, ni, nj = move
            board_copy = copy.deepcopy(board)
            board_copy.move_pawn(pid, ni, nj)
            eval_score, _ = minimax(board_copy, color, depth-1, alpha, beta, maximizing=True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break 
        return min_eval, best_move
