from termcolor import colored

# QUICK-ACCESS STATES FOR DEBUGGING
STATE_START = "white BR BN BB BQ BK BB BN BR BP BP BP BP BP BP BP BP 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WP WP WP WP WP WP WP WP WR WN WB WQ WK WB WN WR"
STATE_ROOK = "white BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR "
STATE_TWO_KINGS = "white BK 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WK"


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
            if piece.type == "king":
                self.pieces[start_position[0]][start_position[1]] = Piece()
                self.pieces[end_position[0]][end_position[1]] = piece
            self.change_color_to_play()
            return True
        return False
        
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

        
    #Print the board to the standard output
    def display(self):
        for row in self.pieces:
            for piece in row:
                # get info about piece
                piece_to_display = piece
                piece_code = ""
                match piece_to_display.type:
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
                        
                if piece_to_display.color == "white":
                    colored_piece = colored(f"{piece_code:2}", "white", attrs=["bold"])
                elif piece_to_display.color == "black":
                    colored_piece = colored(f"{piece_code:2}", "blue", attrs=["bold"])
                else:
                    colored_piece = f"{piece_code:2}" # fallback
                print(colored_piece, end=" ")
            print()
        if self.to_play == "white":
            print(colored("White to play.", "white", attrs=["bold"]))
        else:
            print(colored("Black to play.", "blue", attrs=["bold"]))
        print()

    #Converts a tuple position to algebraic notation
    #PARAMS: tuple containing the index row and column of a position
    #RETURN: a string with the algebraic notation of the position
    def index_to_algebraic(position):
        r,c = position
        file = chr(ord('a') + c)
        rank = str(8 - r)
        return file + rank
    
    #Converts the algebraic notation of a position to index notation
    #PARAMS: string with valid algebraic notation of a position on the board
    #RETURN: a tuple representing the position in index notation
    def algebraic_to_index(alg):
        file = alg[0]
        rank = alg[1]

        r = ord(file) - ord('a')
        c = 8 - rank
        return (r,c)

class Piece:
    def __init__(self, type="empty", color="None"):
        self.type = type.lower()
        self.color = color.lower()