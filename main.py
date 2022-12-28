# Constants for the board
ROWS = 7
COLUMNS = 8

# Constants for the players
USER_1 = 0
USER_2 = 1
AI = 2


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


def board_full(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == -1:
                return False
    return True


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


def option(player_1, player_2):
    board = game_board()

    while True:
        try:
            print_board(board)
            column = int(input("Enter column: "))
            move_piece(board, player_1, column)
            print_board(board)
            if win_condition(board, player_1):
                print("You win!")
                break

        except ValueError as e:
            print(str(e))
            continue
        try:
            column = int(input("Enter column: "))
            move_piece(board, player_2, column)
            print_board(board)
            if win_condition(board, player_2):
                print("You lose!")
                break
        except ValueError as e:
            print(str(e))
            continue

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
        option(USER_1, USER_2)
    elif option == 2:
        # Human vs AI
        option(USER_1, AI)
    else:
        # AI vs AI
        option(AI, AI)


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
