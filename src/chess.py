from termcolor import colored

# QUICK-ACCESS STATES FOR DEBUGGING
STATE_START = "white BR BN BB BQ BK BB BN BR BP BP BP BP BP BP BP BP 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WP WP WP WP WP WP WP WP WR WN WB WQ WK WB WN WR"
STATE_ROOK = "white BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR "
STATE_TWO_KINGS = "white BK 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WK"
STATE_TWO_ROOKS = "white BR 0 0 BK 0 0 0 BR 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WR 0 0 0 WK 0 0 WR"


class Board:
    def __init__(self,state=""):
        # The color player whose turn it is
        self.to_play = "white"
        # The pieces on the board
        o = Piece()
        self.pieces = [[o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o],
                       [o,o,o,o,o,o,o,o]]
        if state:
            self.set_state(state)

    #Sets board to a certain state
    #PARAMS - s: String, a state to set the board to  .
    def set_state(self, s):
        arr = list(s.split())
        if len(arr) != 65:
            print("Invalid string! Cannot load position.")
        else:
            color_to_play = arr.pop(0).lower()
            if (color_to_play != "white" and color_to_play != "black"):
                print("Invalid string! First parameter must be \'white\' or \'black\'")
                return -1
            self.to_play = color_to_play

            for rank in range(8):
                for piece in range(8):
                    piece_code = arr.pop(0)
                    piece_color = ""
                    piece_type = ""
                    if piece_code == "0":
                        self.pieces[rank][piece] = Piece("empty")
                    else:
                        match piece_code[0]:
                            case 'W': piece_color = "white"
                            case 'B': piece_color = "black"
                        match piece_code[1]:
                            case 'P': piece_type = "pawn"
                            case 'N': piece_type = "knight"
                            case 'B': piece_type = "bishop"
                            case 'R': piece_type = "rook"
                            case 'Q': piece_type = "queen"
                            case 'K': piece_type = "king"
                        self.pieces[rank][piece] = Piece(piece_type, piece_color)

    #Makes a move on the board, if legal
    #PARAMS: move - a move in move notation ((start_row,start_column),(final_row,final_column)
    #RETURN: bool, representing whether the move was legal or not
    def make_move(self,move):
        start_position, end_position = move
        legal_moves = self.get_legal_moves()
        if move in legal_moves:
            piece = self.pieces[start_position[0]][start_position[1]]
            match piece.type:
                case "king":
                    self.pieces[start_position[0]][start_position[1]] = Piece()
                    self.pieces[end_position[0]][end_position[1]] = piece
                case "rook":
                    # get movement direction
                    diffr = end_position[0] - start_position[0]
                    diffc = end_position[1] - start_position[1]
                    direction = (
                        0 if diffr == 0 else int(diffr / abs(diffr)),
                        0 if diffc == 0 else int(diffc / abs(diffc))
                    )

                    # remove rook from start
                    self.pieces[start_position[0]][start_position[1]] = Piece()

                    # store displaced piece (if any)
                    displaced = self.pieces[end_position[0]][end_position[1]]

                    # place rook
                    self.pieces[end_position[0]][end_position[1]] = piece

                    # if no piece was displaced, nothing more to do
                    if displaced.type == "empty":
                        self.change_color_to_play()
                        return True

                    #handle all bump logic
                    self.handle_bump_chain(displaced, end_position, direction, 2)

            self.change_color_to_play()
            return True
        return False
    
    # Handles all bump-chain logic after an initial collision.
    # PARAMS: piece - first displaced piece
    #         start_position - where the piece currently sits
    #         direction - normalized direction tuple (dr, dc)
    #         momentum - distance for first piece to travel
    def handle_bump_chain(self, piece, start_position, direction, momentum):
        current_piece = piece
        current_row, current_col = start_position
        distance_covered = 0

        while True:
            bumped_this_turn = False

            for _ in range(momentum):
                distance_covered += 1
                next_row = current_row + direction[0]
                next_col = current_col + direction[1]

                # piece falls off board
                if not (0 <= next_row <= 7 and 0 <= next_col <= 7):
                    return

                next_piece = self.pieces[next_row][next_col]

                if next_piece.type != "empty":
                    # collision
                    self.pieces[next_row][next_col] = current_piece
                    current_piece = next_piece
                    bumped_this_turn = True

                current_row = next_row
                current_col = next_col
                momentum = 1

            if not bumped_this_turn:
                # movement completed without collision
                # place final piece
                self.pieces[current_row][current_col] = current_piece
                return

        
    #Get all legal moves on board
    #RETURN: array of tuples containing all legal moves in move notation
    def get_legal_moves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.pieces[r][c].color == self.to_play:
                    moves += self.get_legal_moves_for_piece(r,c)
        return moves

    #Get all legal moves for the piece at coordinates r,c
    #PARAMS: r - row index of piece to check. c - column index of piece to check.
    #RETURN: array of pseudo-legal moves in move notation
    def get_legal_moves_for_piece(self,r,c):
        piece_type = self.pieces[r][c].type
        test_board = Board(self.to_string())
        moves = []
        match piece_type:
            case 'empty':
                return moves
            case 'king':
                directions = [(-1,-1),(-1, 0),(-1, 1),
                              ( 0,-1),        ( 0, 1),
                              ( 1,-1),( 1, 0),( 1, 1)]
                for dr, dc in directions:
                    new_r = dr + r
                    new_c = dc + c
                    if (0 <= new_r <= 7 and 0 <= new_c <= 7):
                        moves.append(((r,c),(new_r,new_c)))
                return moves
            case 'rook':
                directions = [        (-1, 0),
                              ( 0,-1),        ( 0, 1),
                                      ( 1, 0)         ]
                start_position = (r,c)
                for dr, dc in directions:
                    distance_traversed = 0
                    while True:
                        distance_traversed += 1
                        end_position = (r+(dr*distance_traversed),c+(dc*distance_traversed))
                        print(f"Testing the rook at {r} {c}.")
                        print(f"Looking at {end_position}")
                        if (end_position[0] < 0 or
                            end_position[0] > 7 or
                            end_position[1] < 0 or
                            end_position[1] > 7 ):
                            break
                        new_move = (start_position, end_position)
                        moves.append(new_move)
                        if self.pieces[end_position[0]][end_position[1]].type != "empty":
                            break
                return moves
                            
                        



    #Returns a compact string representing the current board state to be loaded into other games.
    def to_string(self):
        string = "" 
        string += self.to_play + ' '
        for r in range(8):
            for c in range(8):
                piece_type = self.pieces[r][c].type
                if piece_type == "knight":
                    piece_type = "nnight" #this looks stupid as fuck lol
                piece_color = self.pieces[r][c].color

                if piece_type == "empty":
                    string = string + "0 "
                else:
                    string = string + piece_color[0].upper() + piece_type[0].upper() + ' '
        return string
    
    #Determines whether the game is over.
    #RETURNS: Tuple. Index 0 is T/F representing whether game is over, Index 1 is a char representing the winning side. Index 1 may be W, B, or D.
    def is_game_over(self):
        white_king_exists = False
        black_king_exists = False
        for r in range(8):
            for c in range(8):
                piece = self.pieces[r][c]
                if piece.type == "king":
                    if piece.color == "white":
                        white_king_exists = True
                    elif piece.color == "black":
                        black_king_exists = True
        if (white_king_exists and black_king_exists):
            return (False,None)
        elif (white_king_exists):
            return (True,'W')
        elif (black_king_exists):
            return (True,'B')
        return (True,'D')
    
    def change_color_to_play(self):
        if self.to_play == "white":
            self.to_play = "black"
        else:
            self.to_play = "white"

        
    def display(self):
        for r in range(8):
            # Print rank label (8 at top → 1 at bottom)
            rank_label = 8 - r
            print(f"{rank_label} ", end="")
    
            for c in range(8):
                piece = self.pieces[r][c]
    
                match piece.type:
                    case "pawn":
                        piece_code = "P"
                    case "knight":
                        piece_code = "N"
                    case "bishop":
                        piece_code = "B"
                    case "rook":
                        piece_code = "R"
                    case "queen":
                        piece_code = "Q"
                    case "king":
                        piece_code = "K"
                    case "empty":
                        piece_code = "-"
    
                if piece.color == "white":
                    colored_piece = colored(f"{piece_code:2}", "white", attrs=["bold"])
                elif piece.color == "black":
                    colored_piece = colored(f"{piece_code:2}", "blue", attrs=["bold"])
                else:
                    colored_piece = f"{piece_code:2}"
    
                print(colored_piece, end=" ")
            print()
    
        # Print file labels
        print("  ", end="")
        for c in range(8):
            file_label = chr(ord('A') + c)
            print(f"{file_label}  ", end="")
        print()
    
        # Print side to move
        if self.to_play == "white":
            print(colored("White to play.", "white", attrs=["bold"]))
        else:
            print(colored("Black to play.", "blue", attrs=["bold"]))
        print()

    # Converts a tuple index position to algebraic notation
    # PARAMS: position - tuple (row, column) with 0-based indices
    # RETURN: string in algebraic notation, e.g., "e4"
    def index_to_algebraic(self, position):
        r, c = position
        file = chr(ord('a') + c)   # column 0 → 'a', column 1 → 'b', etc.
        rank = str(8 - r)          # row 0 → rank 8, row 7 → rank 1
        return file + rank
    
    #Converts the algebraic notation of a position to index notation
    #PARAMS: string with valid algebraic notation of a position on the board
    #RETURN: a tuple representing the position in index notation
    def algebraic_to_index(self, alg):
        file = alg[0]
        rank = int(alg[1])

        r = 8 - rank
        c = ord(file) - ord('a')
        return (r,c)

class Piece:
    def __init__(self, type="empty", color="None"):
        self.type = type.lower()
        self.color = color.lower()