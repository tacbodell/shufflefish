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
    board.display()
    print(board.to_string())
    print(board.is_game_over())
    board.set_state(board.ROOK_STATE)
    board.display()
    print(board.to_string())
    print(board.is_game_over())

if __name__ == "__main__":
    main()