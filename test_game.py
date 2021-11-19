import numpy as np

FIELD_SIZE = 5
WINNING_ROW = 3


def create_board():
    board = np.zeros((FIELD_SIZE, FIELD_SIZE))
    return board


def make_move(board, row, col, sign):
    board[row][col] = sign


def is_valid_cell(board, row, col):
    if board[row][col] != 0:
        print('Эта клетка уже занята! ')
        return False
    return True


def winning_move(board, sign, move):
    """ проверить выйгрышные комбинации """

    original = board[move[0]][move[1]]
    board[move[0]][move[1]] = sign
    x_this, y_this = move

    # границы
    up = min(x_this, WINNING_ROW - 1)
    down = min(FIELD_SIZE - 1 - x_this, WINNING_ROW - 1)
    left = min(y_this, WINNING_ROW - 1)
    right = min(FIELD_SIZE - 1 - y_this, WINNING_ROW - 1)

    # диагональ \
    up_left = min(up, left)
    down_right = min(down, right)
    for i in range(up_left + down_right - WINNING_ROW + 2):
        a = [board[x_this - up_left + i + j][y_this - up_left + i + j] for j in range(WINNING_ROW)]

        if len(set(a)) == 1 and a[0] > 0:
            board[move[0]][move[1]] = original
            return True

    # диагональ /
    up_right = min(up, right)
    down_left = min(down, left)
    for i in range(up_right + down_left - WINNING_ROW + 2):
        a = [board[x_this - up_right + i + j][y_this + up_right - i - j] for j in range(WINNING_ROW)]

        if len(set(a)) == 1 and a[0] > 0:
            board[move[0]][move[1]] = original
            return True

    # ряд
    for i in range(left + right - WINNING_ROW + 2):
        a = [board[x_this][y_this - left + i + j] for j in range(WINNING_ROW)]

        if len(set(a)) == 1 and a[0] > 0:
            board[move[0]][move[1]] = original
            return True

    # колонка
    for i in range(up + down - WINNING_ROW + 2):
        a = [board[x_this - up + i + j][y_this] for j in range(WINNING_ROW)]

        if len(set(a)) == 1 and a[0] > 0:
            board[move[0]][move[1]] = original
            return True

    board[move[0]][move[1]] = original
    return False


game_board = create_board()
game_over = False
turn = 0
print(game_board)
while not game_over:
    # ask for player 1 Input
    if turn % 2 == 0:
        selection = input("Player 1 make move(x,y): ")
        x, y = map(int, selection.split())
        if is_valid_cell(game_board, x, y):
            x = int(x)
            y = int(y)
            make_move(game_board, x, y, 1)

            if winning_move(game_board, 1, (x, y)):
                print('Player 1 winner!')
                game_over = True

            turn += 1
        else:
            print('Неверный ввод!')

    # ask for player 2 Input
    else:
        selection = input("Player 1 make move(x,y): ")
        x, y = selection.split()
        if is_valid_cell(game_board, x, y):
            x = int(x)
            y = int(y)
            make_move(game_board, x, y, 2)

            if winning_move(game_board, 2, (x, y)):
                print('Player 2 winner!')
                game_over = True

            turn += 1

    print(game_board)
