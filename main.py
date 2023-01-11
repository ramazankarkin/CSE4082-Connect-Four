from copy import deepcopy
import random

# Constants for the board
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


def evaluate_heuristic1(board, player):
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    score = 0

    # Add a bonus for each three-in-a-row sequence that can be completed by the current player
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


# This is a heuristic function for getting the score with respect to the weights of each location on the board
def evaluate_heuristic2(board, player):
    """Returns a score for the given board and player."""
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    # Initialize the score to 0
    score = 0

    # Create a matrix of weights for each position on the board
    weights = [
        [3, 4, 5, 7, 7, 5, 4, 3],
        [4, 6, 8, 10, 10, 8, 6, 4],
        [5, 8, 11, 13, 13, 11, 8, 5],
        [7, 9, 13, 15, 15, 13, 9, 7],
        [5, 8, 11, 13, 13, 11, 8, 5],
        [4, 6, 8, 10, 10, 8, 6, 4],
        [3, 4, 5, 7, 7, 5, 4, 3]
    ]

    # Loop through the board and add the corresponding weight for each cell
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                score += weights[row][col]
            elif board[row][col] == (player + 1) % 2:
                score -= weights[row][col]

    return score


# This heuristic function is same with heuristic 2, it will change.
def evaluate_heuristic3(board, player):
    """Returns a score for the given board and player."""
    if win_condition(board, player):
        return float("inf")
    if win_condition(board, (player + 1) % 2):
        return -float("inf")

    # Initialize the score to 0
    score = 0

    # Create a matrix of weights for each position on the board
    weights = [
        [3, 4, 5, 7, 7, 5, 4, 3],
        [4, 6, 8, 10, 10, 8, 6, 4],
        [5, 8, 11, 13, 13, 11, 8, 5],
        [7, 9, 13, 15, 15, 13, 9, 7],
        [5, 8, 11, 13, 13, 11, 8, 5],
        [4, 6, 8, 10, 10, 8, 6, 4],
        [3, 4, 5, 7, 7, 5, 4, 3]
    ]

    # Loop through the board and add the corresponding weight for each cell
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player:
                score += weights[row][col]
            elif board[row][col] == (player + 1) % 2:
                score -= weights[row][col]

    return score


def minimax(board, player, depth=4, alpha=-float("inf"), beta=float("inf"), eval_func=evaluate_heuristic1):
    """Returns the best column to move and the associated minimax score."""
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
    """Play two AI players against each other."""
    board = game_board()
    current_player = player_1

    print("Choose evaluation function for AI player1:")
    print("1.Heuristic 1")
    print("2.Heuristic 2")
    print("3.Heuristic 3")
    eval_choice_ai1 = int(input())

    print("Choose evaluation function for AI player2:")
    print("1.Heuristic 1")
    print("2.Heuristic 2")
    print("3.Heuristic 3")
    eval_choice_ai2 = int(input())

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
            print("It's a tie!")
            break

        # Switch AI players
        current_player = (current_player + 1) % 2


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
        option3(USER_1)


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
