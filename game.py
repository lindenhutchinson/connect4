from ai import Connect4AI
from util import BLUE_CIRCLE, RED_CIRCLE, YELLOW_CIRCLE, is_valid_move, drop_piece, print_board, is_terminal_node
import copy

class Connect4Game:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[BLUE_CIRCLE for _ in range(self.cols)] for _ in range(self.rows)]
        self.ai = Connect4AI(6)
        self.game_over = False
        self.turn = 0

    def is_game_over(self, col, row):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal /
        for direction in directions:
            count = 1
            for d in [1, -1]:  # check both positive and negative direction
                for i in range(1, 4):
                    r = row + direction[0] * i * d
                    c = col + direction[1] * i * d
                    if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == self.board[row][col]:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
        return False

    def play_move(self, col, player):
        if is_valid_move(self.board, col):
            row = drop_piece(self.board, col, player)
            print_board(self.board)

            if self.is_game_over(col, row):
                print(f"Player {1 if player == RED_CIRCLE else 2} wins!")
                self.game_over = True
            self.turn += 1
        else:
            print("Invalid move! Try again.")

    def ai_move(self, is_first_turn=False, ai_colour=YELLOW_CIRCLE):
        print("AI's turn...")
        best_col = self.ai.find_best_move(copy.deepcopy(self.board), ai_colour, is_first_turn)
        self.play_move(best_col, YELLOW_CIRCLE)
        
        print_board(self.board)
        print(f"{ai_colour} - {best_col}")
        if is_terminal_node(self.board):
            print("Game Over!")
            self.game_over = True
