from copy import deepcopy
import random

# Ramazan Karkin 150119512
# This is the homework 2 for the Artificial Intelligence course. This homework is about the Connect-Four game.


# Constants for the board
# Caution: If you want to change the board size, the heuristic function 2 and 3 should be changed.
# Otherwise, it will not work. Because the heuristic function 2 and 3 are designed for 7x8 board.

ROWS = 7
COLUMNS = 8

# Constants for the players
USER_1 = 0
USER_2 = 1


# Create a board with specific ROWS and COLUMNS filled with -1.
def game_board():
    game_board = []
    for row in range(ROWS):
        game_board.append([-1] * COLUMNS)
    return game_board


# Start from the bottom and check specific column for the player then fill the player's value specified column.
# check invalid column.
def move_piece(game_board, player, column):
    if column < 0 or column >= COLUMNS:
        raise ValueError("Invalid column")
    else:
        # range(start, stop, step)
        for row in range(ROWS - 1, -1, -1):
            if game_board[row][column] == -1:
                game_board[row][column] = player
                return


# Returns True if the given column is a valid move, False otherwise.
def is_playable(game_board, column):
    return game_board[0][column] == -1


# It will check board for valid move and if there is a valid move then it will choose a random column.
def choice(board):
    valid_columns = [column for column in range(COLUMNS) if is_playable(board, column)]
    if valid_columns:
        return random.choice(valid_columns)
    return None


# Check the win condition for the player.
def win_condition(game_board, player):
    # check the whole board If there are 4 identical pieces horizontally,
    # according to the value that the player has, send the winning condition True.
    for row in range(ROWS):
        for column in range(COLUMNS):
            if column < COLUMNS - 3:
                if game_board[row][column] == player and game_board[row][column + 1] == player and \
                        game_board[row][column + 2] == player and game_board[row][column + 3] == player:
                    return True

    # check the whole board If there are 4 identical pieces vertically,
    # according to the value that the player has, send the winning condition True.
    for row in range(ROWS):
        for column in range(COLUMNS):
            if row < ROWS - 3:
                if game_board[row][column] == player and game_board[row + 1][column] == player and \
                        game_board[row + 2][column] == player and game_board[row + 3][column] == player:
                    return True

    # check the whole board If there are 4 identical pieces diagonally,
    # according to the value that the player has, send the winning condition True.
    for row in range(ROWS):
        for column in range(COLUMNS):
            if row < ROWS - 3 and column < COLUMNS - 3:
                if game_board[row][column] == player and game_board[row + 1][column + 1] == player and \
                        game_board[row + 2][column + 2] == player and game_board[row + 3][column + 3] == player:
                    return True

    # check the whole board If there are 4 identical pieces anti-diagonally,
    # according to the value that the player has, send the winning condition True.
    for row in range(ROWS):
        for column in range(COLUMNS):
            if row < ROWS - 3 and column > 2:
                if game_board[row][column] == player and game_board[row + 1][column - 1] == player and \
                        game_board[row + 2][column - 2] == player and game_board[row + 3][column - 3] == player:
                    return True
    return False


# This function prints the Connect-Four game play field and also player's move to the console.
def print_board(board):
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


# This heuristic function checks number of occurrences of three-in-a-row sequence that can be completed
# by the current player, if there exist any such sequence, it adds 1 to the score.
def evaluate_heuristic1(board, player):
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    score = 0
    # add 1 to the score if there is a three-in-a-row sequence that can be completed by the current player
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                # Check horizontally
                if col < COLUMNS - 2:
                    if board[row][col + 1] == player and board[row][col + 2] == -1:
                        score += 1
                # Check vertically
                if row < ROWS - 2:
                    if board[row + 1][col] == player and board[row + 2][col] == -1:
                        score += 1
                # Check diagonally
                if col < COLUMNS - 2 and row < ROWS - 2:
                    if board[row + 1][col + 1] == player and board[row + 2][col + 2] == -1:
                        score += 1
                # Check anti-diagonally
                if col > 1 and row < ROWS - 2:
                    if board[row + 1][col - 1] == player and board[row + 2][col - 2] == -1:
                        score += 1

    return score


# This heuristic function uses a weight matrix to assign a score to each cell on the board.
# We have given weight to each position according to the positions we think are more important,
# with higher weights given to cells in the center of the board. This way,
# the AI player will prioritize moves that are made in the center of the board.
def evaluate_heuristic2(board, player):
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    # Initialize the score to 0
    score = 0

    # Created a matrix of weights for each position
    weights = [
        [2, 5, 7, 9, 9, 7, 5, 2],
        [4, 7, 9, 11, 11, 9, 7, 4],
        [6, 10, 14, 18, 18, 14, 10, 6],
        [8, 13, 18, 23, 23, 18, 13, 8],
        [6, 10, 14, 18, 18, 14, 10, 6],
        [4, 7, 9, 11, 11, 9, 7, 4],
        [2, 5, 7, 9, 9, 7, 5, 2]
    ]

    # Add the corresponding weight for each cell
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                score += weights[row][col]

    return score


# This heuristic function uses evaluate_heuristic2 and also checks number of occurrences of two adjacent same player
# values, after heuristic2 assigned a score to each cell on the board according to the weight matrix, then for each
# occurrence of two adjacent same values, it will triple the score

def evaluate_heuristic3(board, player):
    """Returns a score for the given board and player."""
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    score = 0

    weights = [
        [2, 5, 7, 9, 9, 7, 5, 2],
        [4, 7, 9, 11, 11, 9, 7, 4],
        [6, 10, 14, 18, 18, 14, 10, 6],
        [8, 13, 18, 23, 23, 18, 13, 8],
        [6, 10, 14, 18, 18, 14, 10, 6],
        [4, 7, 9, 11, 11, 9, 7, 4],
        [2, 5, 7, 9, 9, 7, 5, 2]
    ]
    # Add the corresponding weight for each cell
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                score += weights[row][col]
    # checks number of occurrences of two adjacent same player values
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                # Check horizontally
                if (col < COLUMNS - 1 and board[row][col + 1] == player) or (col > 0 and board[row][col - 1] == player):
                    score += 3
                # Check vertically
                if (row < ROWS - 1 and board[row + 1][col] == player) or (row > 0 and board[row - 1][col] == player):
                    score += 3
                # Check diagonally
                if (row < ROWS - 1 and col < COLUMNS - 1 and board[row + 1][col + 1] == player) or (
                        row > 0 and col > 0 and board[row - 1][col - 1] == player):
                    score += 3
                if (row < ROWS - 1 and col > 0 and board[row + 1][col - 1] == player) or (
                        row > 0 and col < COLUMNS - 1 and board[row - 1][col + 1] == player):
                    score += 3

    return score


# The minimax algorithm approach for which we applied is
# by recursively calling the minimax function for each playable column on the board, and finding
# the alpha and beta values which are used to prune the search tree to avoid unnecessary work.
# The function takes the current state of the board, the player
# that is making the move, alpha, beta, and evaluation function as inputs.
def minimax(board, player, depth=4, alpha=-float("inf"), beta=float("inf"), eval_func=evaluate_heuristic3):
    if depth == 0 or win_condition(board, player):
        # Use the specified evaluation function
        score = eval_func(board, player)
        return score, None

    best_column = None
    for column in range(COLUMNS):
        if is_playable(board, column):
            temp_board = deepcopy(board)
            move_piece(temp_board, player, column)
            score = minimax(temp_board, (player + 1) % 2, depth - 1, -beta, -alpha, eval_func)[0]
            score = -score
            if score > alpha:
                alpha = score
                best_column = column
            if alpha >= beta:
                break
    # If no valid column was found, select a random valid column
    if best_column is None:
        best_column = choice(board)
    return alpha, best_column


def option1(player_1, player_2):
    board = game_board()
    print("Initial board state:")

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

        while True:
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
            break

        # check all row if the there is not -1 in the board then it is a tie
        if all([cell != -1 for row in board for cell in row]):
            print("It's a draw!")
            break


def option2(player_1, player_2):
    board = game_board()
    print("Initial board state:")
    print_board(board)

    while True:
        try:
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


def option3(player_1):
    board = game_board()
    current_player = player_1
    while True:
        print("Choose evaluation function for AI player1:")
        print("1.Heuristic 1")
        print("2.Heuristic 2")
        print("3.Heuristic 3")
        eval_choice_ai1 = int(input())
        if eval_choice_ai1 in [1, 2, 3]:
            break
        print("Invalid option for AI player1. Please enter a valid number.")
    while True:
        print("Choose evaluation function for AI player2:")
        print("1.Heuristic 1")
        print("2.Heuristic 2")
        print("3.Heuristic 3")
        eval_choice_ai2 = int(input())
        if eval_choice_ai2 in [1, 2, 3]:
            break
        print("Invalid option for AI player2. Please enter a valid number.")

    evaluation = [evaluate_heuristic1, evaluate_heuristic2, evaluate_heuristic3]
    print("Initial board state:")
    while True:
        if current_player == player_1:
            evaluation_function = evaluation[eval_choice_ai1 - 1]
            print_board(board)

            # Print the current player's turn
            print(f"AI {current_player + 1}'s turn")

            # Get the AI's move
            column = minimax(board, current_player, eval_func=evaluation_function)[1]
        else:
            evaluation_function = evaluation[eval_choice_ai2 - 1]
            print_board(board)

            # Print the current player's turn
            print(f"AI {current_player + 1}'s turn")

            # Get the AI's move
            column = minimax(board, current_player, eval_func=evaluation_function)[1]

        # Make the move
        try:
            move_piece(board, current_player, column)
        except ValueError as e:
            print(e)
            continue

        # Check if the game is over
        if win_condition(board, current_player):
            print_board(board)
            print(f"AI {current_player + 1} wins!")
            break
        if not any(is_playable(board, column) for column in range(COLUMNS)):
            print_board(board)
            print("It's a draw!")
            break

        # Switch AI players
        current_player = (current_player + 1) % 2


# This is the main function that is used to start the game. If option 3 is selected then
# the game asks to choose the evaluation function for both the AI players.
def main():
    while True:
        print('Welcome to Connect Four!')
        print('1. Human vs Human')
        print('2. Human vs AI')
        print('3. AI vs AI')
        choose = input('Enter your choice: ')
        if choose.isdigit():
            choose = int(choose)
            if choose == 1:
                # Human vs Human
                option1(USER_1, USER_2)
                break
            elif choose == 2:
                # Human vs AI
                option2(USER_1, USER_2)
                break
            elif choose == 3:
                # AI vs AI
                option3(USER_1)
                break
            else:
                print("Invalid option. Please enter a valid number.")
        else:
            print("Invalid option. Please enter a number.")


if __name__ == '__main__':
    main()

"""
We used the following board state to check if some part of the function is giving correct results.
boards = [[1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 1, 0, 1, 0, 1, 0],
          [1, 0, 0, 1, 0, 1, 0, 1],
          [0, 1, 0, 1, 0, 1, 0, 1],
          [1, 0, 0, 1, 0, 1, 0, 1]]
print(win_condition(boards, 1))
"""
