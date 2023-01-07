from copy import deepcopy
import random

# Constants for the board
ROWS = 7
COLUMNS = 8

# Constants for the players
USER_1 = 0
USER_2 = 1


# create a board with ROWS and COLUMNS
def game_board():
    game_board = []
    for row in range(ROWS):
        game_board.append([-1] * COLUMNS)
    return game_board


# start from the bottom and check specific column for the player
def move_piece(game_board, player, column):
    if column < 0 or column >= COLUMNS:
        raise ValueError("Invalid column")
    else:
        # range(start, stop, step)
        for row in range(ROWS - 1, -1, -1):
            if game_board[row][column] == -1:
                game_board[row][column] = player
                return


def win_condition(game_board, player):
    # check horizontal
    for row in range(ROWS):
        for column in range(COLUMNS - 3):

            if game_board[row][column] == player and game_board[row][column + 1] == player and game_board[row][
                column + 2] == player and game_board[row][column + 3] == player:
                return "horizontal"

    # check vertical
    for row in range(ROWS - 3):
        for column in range(COLUMNS):
            if game_board[row][column] == player and game_board[row + 1][column] == player and game_board[row + 2][
                column] == player and game_board[row + 3][column] == player:
                return "vertical"

    # check diagonal
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if game_board[row][column] == player and game_board[row + 1][column + 1] == player and game_board[row + 2][
                column + 2] == player and game_board[row + 3][column + 3] == player:
                return "diagonal"

    # check anti diagonal
    for row in range(ROWS - 3):
        for column in range(3, COLUMNS):
            if game_board[row][column] == player and game_board[row + 1][column - 1] == player and game_board[row + 2][
                column - 2] == player and game_board[row + 3][column - 3] == player:
                return "anti diagonal"

    return False


def print_board(board):
    """Prints the board to the console."""
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            if board[row][col] == USER_1:
                print("X", end="|")
            elif board[row][col] == USER_2:
                print("O", end="|")
            else:
                print(" ", end="|")
        print()
    print("-" * (COLUMNS * 2 + 1))

def choice(board):
    valid_columns = [column for column in range(COLUMNS) if is_valid_move(board, column)]
    if valid_columns:
        return random.choice(valid_columns)
    return None
def minimax(board, player, depth=4, alpha=-float("inf"), beta=float("inf")):
    """Returns the best column to move and the associated minimax score."""
    if depth == 0 or win_condition(board, player):
        score = evaluate_board(board, player)
        return score, None

    best_column = None
    for column in range(COLUMNS):
        if is_valid_move(board, column):
            temp_board = deepcopy(board)
            move_piece(temp_board, player, column)
            score, _ = minimax(temp_board, (player + 1) % 2, depth - 1, -beta, -alpha)
            score = -score
            if score > alpha:
                alpha = score
                best_column = column
            if alpha >= beta:
                break
    if best_column is None:
        best_column = random.choice([column for column in range(COLUMNS) if is_valid_move(board, column)])
    return alpha, best_column


def evaluate_board(board, player):
    """Returns a score for the given board and player."""
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")
    return 0

def is_valid_move(board, column):
    """Returns True if the given column is a valid move, False otherwise."""
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == -1


def option1(player_1, player_2):
    board = game_board()

    while True:
        try:
            print_board(board)
            column = int(input("Player 1 enter column: "))
            move_piece(board, player_1, column)
            print_board(board)
            if win_condition(board, player_1):
                print("Player 1 wins!")
                break
        except ValueError as e:
            print(str(e))
            continue

        try:
            column = int(input("Player 2 enter column: "))
            move_piece(board, player_2, column)
            print_board(board)
            if win_condition(board, player_2):
                print("Player 2 wins!")
                break
        except ValueError as e:
            print(str(e))
            continue

        # check all row if the there is not -1 in the board then it is a tie
        if all([cell != -1 for row in board for cell in row]):
            print("It's a draw!")
            break

def option2(player_1, player_2):
    board = game_board()

    while True:
        try:
            print_board(board)
            column = int(input("Player 1 enter column: "))
            move_piece(board, player_1, column)
            print_board(board)
            if win_condition(board, player_1):
                print("Player 1 wins!")
                break
        except ValueError as e:
            print(str(e))
            continue


        # The AI's move
        column = minimax(board, player_2, depth=4)[1]
        print("AI move: ", column)
        if column is not None:
            move_piece(board, player_2, column)
        print_board(board)
        if win_condition(board, player_2):
            print("AI wins!")
            break

        # check all row if the there is not -1 in the board then it is a tie
        if all([cell != -1 for row in board for cell in row]):
            print("It's a draw!")
            break
def option3(player_1, player_2):
    board = game_board()

    while True:
        # The AI's move
        column = minimax(board, player_1, depth=4)[1]
        if column is not None:
            move_piece(board, player_1, column)
        print_board(board)
        if win_condition(board, player_1):
            print("AI 1 wins!")
            break

        # The AI's move
        column = minimax(board, player_2, depth=4)[1]
        if column is not None:
            move_piece(board, player_2, column)
        print_board(board)
        if win_condition(board, player_2):
            print("AI 2 wins!")
            break

        # check all row if the there is not -1 in the board then it is a tie
        if all([cell != -1 for row in board for cell in row]):
            print("It's a draw!")
            break
def main():

    print('Welcome to Connect Four!')
    print('1. Human vs Human')
    print('2. Human vs AI')
    print('3. AI vs AI')
    choose = int(input('Enter your choice: '))

    if choose == 1:
        # Human vs Human
        option1(USER_1, USER_2)
    elif choose == 2:
        # Human vs AI
        option2(USER_1, USER_2)
    else:
        # AI vs AI
        option3(USER_2, USER_2)


if __name__ == '__main__':
    main()

"""
kontrol etmek için 
boards = [[1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 1, 0, 1, 0, 1, 0],
          [1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [1, 0, 0, 1, 0, 1, 0, 1]]
print(win_condition(boards, 1))
"""
