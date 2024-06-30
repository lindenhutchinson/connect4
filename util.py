BLUE_CIRCLE = "\U0001F535"
RED_CIRCLE = "\U0001F534"
YELLOW_CIRCLE = "\U0001F7E1"

def is_valid_move(board, col):
    return board[0][col] == BLUE_CIRCLE

def drop_piece(board, col, player):
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == BLUE_CIRCLE:
            board[row][col] = player
            return row

def print_board(board):
    for row in board:
        print(" ".join(row))
    print("  ".join(map(str, range(len(board[0])))))
    print()

def is_terminal_node(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == BLUE_CIRCLE:
                return False
    return True
