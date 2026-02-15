import chess
import random

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
        print(moves)
        print(moves_values)
        index = moves_values.index(min(moves_values))
        return moves[index]