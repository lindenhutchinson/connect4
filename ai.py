import copy
from util import BLUE_CIRCLE, RED_CIRCLE, YELLOW_CIRCLE, is_valid_move, drop_piece, is_terminal_node

class Connect4AI:
    def __init__(self, depth=6):
        self.depth = depth

    def find_best_move(self, board, player, is_first_move=False):
        if is_first_move:
            middle_column = len(board[0]) // 2
            return middle_column
        
        opponent = YELLOW_CIRCLE if player == RED_CIRCLE else RED_CIRCLE
        valid_moves = [col for col in range(len(board[0])) if is_valid_move(board, col)]
        
        # Check for immediate winning move for the AI
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            row = drop_piece(temp_board, move, player)
            if self.is_winning_move(temp_board, player, row, move):
                return move
            temp_board[row][move] = BLUE_CIRCLE  # Undo move

        # Check for immediate blocking move for the opponent
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            row = drop_piece(temp_board, move, opponent)
            if self.is_winning_move(temp_board, opponent, row, move):
                return move
            temp_board[row][move] = BLUE_CIRCLE  # Undo move

        # Check for moves that would allow the opponent to win next turn
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, move, player)
            if self.can_win_next_turn(temp_board, opponent):
                continue  # Skip this move if it allows opponent to win next turn

            # Check for future winning move for the AI (next turn)
            if self.can_win_next_turn(temp_board, player):
                return move

        # Prioritize moves with the least number of neighbors
        valid_moves.sort(key=lambda col: self.count_neighbours(board, col))

        # If none of the above, use the evaluation function to find the best move
        best_score = -float('inf')
        best_move = None
        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            drop_piece(temp_board, move, player)
            score = self.evaluate_board(temp_board, player)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate_board(self, board, player):
        score = 0
        opponent = YELLOW_CIRCLE if player == RED_CIRCLE else RED_CIRCLE
        
        # Evaluate horizontal, vertical, and both diagonal directions
        score += self.score_position(board, player, opponent)
        
        return score

    def score_position(self, board, player, opponent):
        score = 0
        
        # Horizontal evaluation
        for row in range(len(board)):
            for col in range(len(board[0]) - 3):
                window = board[row][col:col + 4]
                score += self.evaluate_window(window, player, opponent)
        
        # Vertical evaluation
        for col in range(len(board[0])):
            for row in range(len(board) - 3):
                window = [board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, player, opponent)
        
        # Diagonal (top-left to bottom-right) evaluation
        for row in range(len(board) - 3):
            for col in range(len(board[0]) - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player, opponent)
        
        # Diagonal (top-right to bottom-left) evaluation
        for row in range(len(board) - 3):
            for col in range(3, len(board[0])):
                window = [board[row + i][col - i] for i in range(4)]
                score += self.evaluate_window(window, player, opponent)
        
        return score

    def evaluate_window(self, window, player, opponent):
        score = 0
        
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(BLUE_CIRCLE) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(BLUE_CIRCLE) == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(BLUE_CIRCLE) == 1:
            score -= 4
        elif window.count(opponent) == 2 and window.count(BLUE_CIRCLE) == 2:
            score -= 2

        return score

    def is_winning_move(self, board, player, row, col):
        # Check for horizontal win
        count = 0
        for c in range(len(board[0])):
            if board[row][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check for vertical win
        count = 0
        for r in range(len(board)):
            if board[r][col] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check for diagonal win (top-left to bottom-right)
        start_col = col - min(row, col)
        start_row = row - min(row, col)
        count = 0
        while start_row < len(board) and start_col < len(board[0]):
            if board[start_row][start_col] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            start_row += 1
            start_col += 1

        # Check for diagonal win (top-right to bottom-left)
        start_col = col + min(row, len(board[0]) - col - 1)
        start_row = row - min(row, len(board[0]) - col - 1)
        count = 0
        while start_row < len(board) and start_col >= 0:
            if board[start_row][start_col] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            start_row += 1
            start_col -= 1

        return False

    def can_win_next_turn(self, board, player):
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                temp_board = copy.deepcopy(board)
                row = drop_piece(temp_board, col, player)
                if self.is_winning_move(temp_board, player, row, col):
                    return True
        return False

    def count_neighbours(self, board, col):
        count = 0
        for r in range(len(board)):
            if board[r][col] != BLUE_CIRCLE:
                count += 1
                break
        return count
