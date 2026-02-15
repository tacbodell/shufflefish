import chess
import random

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        if parent:
            self.parent = parent
            self.move_sequence = parent.move_sequence + move
        else:
            self.move_sequence = []

class Search_Tree:
    def __init__(self, state):
        self.root = Node(state)
        self.frontier = []



#returns a random legals move from a given board state.
def find_random_move(state):
    board = chess.Board()
    board.set_state(state)
    moves = board.get_legal_moves()
    n = random.randint(0, len(moves)-1)
    return moves[n]

#returns the current material advantage of a state. positive is winning for white, negative is winning for black.
def get_material_value(state):
    board = chess.Board(state)
    color_modifier = 1
    value = 0
    for r in range(8):
        for c in range(8):
            piece = board.pieces[r][c]
            color_modifier = 1 if piece.color == "white" else -1
            match piece.type:
                case 'pawn':
                    value += 1 * color_modifier
                case 'knight':
                    value += 3 * color_modifier
                case 'bishop':
                    value += 3 * color_modifier
                case 'rook':
                    value += 5 * color_modifier                                                            
                case 'queen':
                    value += 9 * color_modifier
                case 'king':
                    value += 100 * color_modifier
    return value

#returns the move that ends with the best material for the given state. only 1 move deep
def find_best_by_material(state):
    board = chess.Board()
    board.set_state(state)
    to_play = board.to_play
    moves = board.get_legal_moves()
    moves_values = []
    for m in moves:
        board.set_state(state)
        board.make_move(m)
        value = get_material_value(board.to_string())
        moves_values.append(value)
    if to_play == "white":
        index = moves_values.index(max(moves_values))
        return moves[index]
    if to_play == "black":
        index = moves_values.index(min(moves_values))
        return moves[index]
    
def adversarial_search(state, depth):
    board = chess.Board()
    board.set_state(state)

    best_move = None
    alpha = float("-inf")
    beta = float("inf")

    maximizing = (board.to_play == "white")

    best_value = float("-inf") if maximizing else float("inf")

    moves = board.get_legal_moves()

    for move in moves:
        board.set_state(state)
        board.make_move(move)

        value = alphabeta(
            board.to_string(),
            depth - 1,
            alpha,
            beta,
            not maximizing
        )

        if maximizing:
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)

    return best_move

def alphabeta(state, depth, alpha, beta, maximizing_player):
    board = chess.Board()
    board.set_state(state)

    game_over, winner = board.is_game_over()

    # terminal node
    if depth == 0 or game_over:
        return get_material_value(state)

    moves = board.get_legal_moves()

    if maximizing_player:
        value = float("-inf")
        for move in moves:
            board.set_state(state)
            board.make_move(move)

            value = max(
                value,
                alphabeta(
                    board.to_string(),
                    depth - 1,
                    alpha,
                    beta,
                    False
                )
            )

            alpha = max(alpha, value)
            if beta <= alpha:
                break  # PRUNE

        return value

    else:
        value = float("inf")
        for move in moves:
            board.set_state(state)
            board.make_move(move)

            value = min(
                value,
                alphabeta(
                    board.to_string(),
                    depth - 1,
                    alpha,
                    beta,
                    True
                )
            )

            beta = min(beta, value)
            if beta <= alpha:
                break  # PRUNE

        return value
