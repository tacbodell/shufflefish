from termcolor import colored

class Board:
    # QUICK-ACCESS STATES FOR DEBUGGING
    START_STATE = "W BR BN BB BQ BK BB BN BR BP BP BP BP BP BP BP BP 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 WP WP WP WP WP WP WP WP WR WN WB WQ WK WB WN WR"
    ROOK_STATE = "W BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR BR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR WR "

    def __init__(self,state=""):
        # The color player whose turn it is
        self.to_play = 'W'
        # The pieces on the board
        self.pieces = [['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0'],
                       ['0','0','0','0','0','0','0','0']]
        if state:
            self.set_state(state)
        else:
            self.set_state(Board.START_STATE)

    #Sets board to a certain state
    #PARAMS - s: String, a state to set the board to  .
    def set_state(self, s):
        arr = list(s.split())
        if len(arr) != 65:
            print("Invalid string! Cannot load position.")
        else:
            color_to_play = arr.pop(0)
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


    #Get all legal moves on current board state.
    #RETURN: array of all legal moves in algebraic notation.
    def get_legal_moves(self):
        pass

    #Get all pseudo-legal (legal disregarding checks) moves for the piece at coordinates r,c
    #PARAMS: r - row index of piece to check. c - column index of piece to check.
    #RETURN: array of pseudo-legal moves in move notation
    def get_pseudo_legal_moves_for_piece(self,r,c):
        piece_type = self.pieces[r][c].type
        moves = []
        match piece_type:
            case 'rook':
                pass
            

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
        print()

class Piece:
    def __init__(self, type="empty", color="None"):
        self.type = type.lower()
        self.color = color.lower()