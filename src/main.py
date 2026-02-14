import chess

def main():
    print("Welcome to shuffleboard chess!!")
    print("Would you like to play against an ai or use the analysis board?")
    command = ""
    while not command:
        command = input("Enter \'ai\', \'analysis\', or \'quit\': ").strip().lower()
        match command:
            case "ai":
                play_game_with_ai()
            case "analysis":
                do_analysis()
            case "quit":
                pass
            case "test":
                test_function()
            case _:
                command = ""
                print("Invalid command. Please try again.")
            
    print("Thank you for playing shuffleboard chess!")

def play_game_with_ai():
    pass

def do_analysis():
    pass

def test_function():
    board = chess.Board()
    board.set_state(chess.STATE_TWO_KINGS)
    print("PREPARE THYSELF!!")
    while (board.is_game_over()[0] == False):
        board.display()
        command = input("Please type a move: ").split()
        if len(command) != 4:
            print("bro")
        else:
            start_r, start_c, end_r, end_c = int(command[0]), int(command[1]), int(command[2]), int(command[3])
            move = ((start_r,start_c),(end_r,end_c))
            if not board.make_move(move):
                print("Invalid move. Try something else. Dickhead")
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