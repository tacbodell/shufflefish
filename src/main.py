import chess

def main():
    print("Welcome to shuffleboard chess!!")
    print("Would you like to play against an ai or use the analysis board?")
    command = ""
    test_function()
            
    print("Thank you for playing shuffleboard chess!")

def play_game_with_ai():
    pass

def do_analysis():
    pass

def test_function():
    board = chess.Board()
    board.set_state(chess.STATE_START)
    board.display()
    print("PREPARE THYSELF!!")
    while (board.is_game_over()[0] == False):
        command = input("Please type a move: ").strip().split()
        if len(command) != 2:
            print("bro")
        else:
            start_pos_alg, end_pos_alg = command[0], command[1]
            start_pos_ind = board.algebraic_to_index(start_pos_alg)
            end_pos_ind = board.algebraic_to_index(end_pos_alg)
            move = (start_pos_ind, end_pos_ind)

            if not board.make_move(move):
                print("Invalid move. Try something else. Dickhead")
        board.display()
    winner = ""
    match board.is_game_over()[1]:
        case "W":
            print("Congratulations!! White wins!!")
        case "B":
            print("Congratulations!! Black wins!!")
        case "D":
            print("what")



if __name__ == "__main__":
    main()