from game import Connect4Game
from util import RED_CIRCLE, YELLOW_CIRCLE, print_board

def get_player_move(player_num):
    col = None
    while type(col) != int:
        try:
            col = int(input(f"Player {player_num} - Choose a column (0-6): "))
        except ValueError:
            print("Please enter a valid number between 0 and 6.")

    return col

def main():
    game = Connect4Game()
    
    print("Welcome to Connect 4!")
    print_board(game.board)

    first_turn = input("Do you want the AI to play first? (y/n): ").strip().lower()
    if first_turn == 'y':
        game.ai_move(is_first_turn=True)

    turn_order = 1 if first_turn == 'y' else 0
    while not game.game_over:
        if game.turn % 2 == turn_order:
            col = get_player_move(RED_CIRCLE)
            game.play_move(col, RED_CIRCLE)
        else:
            if input("AI turn? (y/n)").strip().lower() == "y":
                game.ai_move()
            else:
                col = get_player_move(YELLOW_CIRCLE)
                game.play_move(col, YELLOW_CIRCLE)

        


if __name__ == "__main__":
    main()
