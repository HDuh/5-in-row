import random
import copy
import math as np
import time

MAX_SIMULATION = 20  # константа для просчета ходов AI по количеству ходов наперёд
MAX_SIMULATION_ONE_STEP = 150  # константа для просчета ходов AI по количеству ходов наперёд
TIME_LIMIT = 5  # константа для просчета ходов AI, ограничение по времени
BOARD_SIZE = 10  # размер поля
WINNING_SEQUENCE = 5  # кол-во ряда для победы

board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]


class Node:
    def __init__(self, move, players_in_turn=None, parent=None,
                 num_child=-1, possible_moves_for_child=None, possible_moves_for_expansion=None,
                 board_width=None, board_height=None, num_expand=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.sim_num = 0
        self.win_num = 0
        self.winner = 0

        if parent is None:
            self.max_num_child = num_child
            self.max_num_expansion = num_expand
            self.board_width = board_width
            self.board_height = board_height
            self.possible_moves_for_child = copy.deepcopy(possible_moves_for_child)
            self.possible_moves_for_expansion = copy.deepcopy(possible_moves_for_expansion)

        if parent is not None:
            if parent.max_num_child > 0:
                self.max_num_child = parent.max_num_child - 1

            parent.possible_moves_for_expansion.remove(move)

            # наследование
            self.possible_moves_for_child = copy.deepcopy(parent.possible_moves_for_child)
            self.possible_moves_for_child.remove(move)

            # обновление информации о соседях
            self.possible_moves_for_expansion = copy.deepcopy(parent.possible_moves_for_expansion)
            self.board_width = parent.board_width
            self.board_height = parent.board_height
            x, y = move
            up, down, left, right = x, self.board_height - 1 - x, y, self.board_width - 1 - y
            if up:
                self.possible_moves_for_expansion.add((x - 1, y))
                if left:
                    self.possible_moves_for_expansion.add((x - 1, y - 1))
                if right:
                    self.possible_moves_for_expansion.add((x - 1, y + 1))
            if down:
                self.possible_moves_for_expansion.add((x + 1, y))
                if left:
                    self.possible_moves_for_expansion.add((x + 1, y - 1))
                if right:
                    self.possible_moves_for_expansion.add((x + 1, y + 1))
            if left:
                self.possible_moves_for_expansion.add((x, y - 1))
            if right:
                self.possible_moves_for_expansion.add((x, y + 1))
            self.possible_moves_for_expansion = self.possible_moves_for_expansion & self.possible_moves_for_child
            self.max_num_expansion = len(self.possible_moves_for_expansion)
            self.opponent = parent.player
            self.player = parent.opponent
            parent.children.append(self)
            self.winner = parent.winner
        else:

            self.player = players_in_turn[1]
            self.opponent = players_in_turn[0]


class Board:

    def __init__(self, input_board, n_in_line=5):
        self.width = len(input_board[0])
        self.height = len(input_board)
        self.board = copy.deepcopy(input_board)
        self.n_in_line = n_in_line
        self.available_moves = set([
            (i, j) for i in range(self.height) for j in range(self.width) if input_board[i][j] == 0
        ])
        self.neighbors = self.get_neighbors()
        self.winner = None

    def is_free(self, x, y):
        """ Проверка свободна ли клеточка """
        return 1 if self.board[x][y] == 0 else 0

    def get_neighbors(self):
        neighbors = set()
        if len(self.available_moves) == self.width * self.height:

            # если поле пустое, то выбираем центральную клетку
            x0, y0 = self.width // 2 - 1, self.height // 2 - 1
            neighbors.add((x0, y0))
            return neighbors
        else:
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j]:
                        neighbors.add((i - 1, j - 1))
                        neighbors.add((i - 1, j))
                        neighbors.add((i - 1, j + 1))
                        neighbors.add((i, j - 1))
                        neighbors.add((i, j + 1))
                        neighbors.add((i + 1, j - 1))
                        neighbors.add((i + 1, j))
                        neighbors.add((i + 1, j + 1))

            return neighbors & self.available_moves

    def update(self, player, move, update_neighbor=True):
        """Обновить доску и проверить, победит ли игрок."""
        self.board[move[0]][move[1]] = player
        self.available_moves.remove(move)

        if update_neighbor:
            self.neighbors.remove(move)

            neighbors = set()
            x, y = move
            up, down, left, right = x, self.height - 1 - x, y, self.width - 1 - y
            if up:
                neighbors.add((x - 1, y))
                if left:
                    neighbors.add((x - 1, y - 1))
                if right:
                    neighbors.add((x - 1, y + 1))
            if down:
                neighbors.add((x + 1, y))
                if left:
                    neighbors.add((x + 1, y - 1))
                if right:
                    neighbors.add((x + 1, y + 1))
            if left:
                neighbors.add((x, y - 1))
            if right:
                neighbors.add((x, y + 1))
            neighbors = self.available_moves & neighbors
            self.neighbors = self.neighbors | neighbors

    def check_win(self, player, move):
        """ проверить выйгрышные комбинации """

        original = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = player
        x_this, y_this = move

        # границы
        up = min(x_this, self.n_in_line - 1)
        down = min(self.height - 1 - x_this, self.n_in_line - 1)
        left = min(y_this, self.n_in_line - 1)
        right = min(self.width - 1 - y_this, self.n_in_line - 1)

        # диагональ \
        up_left = min(up, left)
        down_right = min(down, right)
        for i in range(up_left + down_right - self.n_in_line + 2):
            a = [
                self.board[x_this - up_left + i + j][y_this - up_left + i + j] for j in range(self.n_in_line)
            ]

            if len(set(a)) == 1 and a[0] > 0:
                self.board[move[0]][move[1]] = original
                return 1

        # диагональ /
        up_right = min(up, right)
        down_left = min(down, left)
        for i in range(up_right + down_left - self.n_in_line + 2):
            a = [
                self.board[x_this - up_right + i + j][y_this + up_right - i - j] for j in range(self.n_in_line)
            ]

            if len(set(a)) == 1 and a[0] > 0:
                self.board[move[0]][move[1]] = original
                return 1

        # ряд
        for i in range(left + right - self.n_in_line + 2):
            a = [
                self.board[x_this][y_this - left + i + j] for j in range(self.n_in_line)
            ]

            if len(set(a)) == 1 and a[0] > 0:
                self.board[move[0]][move[1]] = original
                return 1

        # колонка
        for i in range(up + down - self.n_in_line + 2):
            a = [
                self.board[x_this - up + i + j][y_this] for j in range(self.n_in_line)
            ]

            if len(set(a)) == 1 and a[0] > 0:
                self.board[move[0]][move[1]] = original
                return 1

        self.board[move[0]][move[1]] = original
        return 0


class MCTS:

    def __init__(self, input_board, players_in_turn, n_in_line=5,
                 confidence=2.0, time_limit=5.0, max_simulation=5, max_simulation_one_play=50):
        self.time_limit = float(time_limit)
        self.max_simulation = max_simulation
        self.max_simulation_one_play = max_simulation_one_play
        self.MCTSboard = Board(input_board, n_in_line)
        self.confidence = confidence
        self.player_turn = players_in_turn
        self.get_player = {
            self.player_turn[0]: self.player_turn[1],
            self.player_turn[1]: self.player_turn[0],
        }
        self.player = self.player_turn[0]
        self.root = Node(None,
                         parent=None,
                         players_in_turn=players_in_turn,
                         num_child=len(self.MCTSboard.available_moves),
                         possible_moves_for_child=self.MCTSboard.available_moves,
                         possible_moves_for_expansion=self.MCTSboard.neighbors,
                         num_expand=len(self.MCTSboard.neighbors),
                         board_width=self.MCTSboard.width,
                         board_height=self.MCTSboard.height)

    def get_action(self):
        if len(self.MCTSboard.available_moves) == 1:
            return list(self.MCTSboard.available_moves)[0]

        num_nodes = 0
        begin_time = time.time()
        while time.time() - begin_time < self.time_limit:

            node_to_expand = self.select_and_expand()

            for _ in range(self.max_simulation):
                board_deep_copy = copy.deepcopy(self.MCTSboard)
                self.simulate_and_bp(board_deep_copy, node_to_expand)

            num_nodes += 1

        percent_wins, move = max(
            (child.win_num / child.sim_num + child.winner, child.move)
            for child in self.root.children
        )
        return move

    def select_and_expand(self):
        "Поиск на основе UCB "
        cur_node = self.root
        while cur_node.children:

            if len(cur_node.children) < cur_node.max_num_expansion:
                break

            ucb, select_node = 0, None
            for child in cur_node.children:

                ucb_child = child.win_num / child.sim_num + np.sqrt(
                    2 * np.log(cur_node.sim_num) / child.sim_num
                )
                if ucb_child >= ucb:
                    ucb, select_node = ucb_child, child
            cur_node = select_node

        expand_move = random.choice(list(cur_node.possible_moves_for_expansion))
        expand_node = Node(expand_move, parent=cur_node)
        return expand_node

    def simulate_and_bp(self, cur_board, expand_node):
        node = expand_node

        while node.parent.move:
            node = node.parent
            cur_board.update(node.player, node.move, update_neighbor=False)

        if len(cur_board.neighbors) == 0:
            return

        cur_board.neighbors = cur_board.get_neighbors()
        player = expand_node.player
        win = cur_board.check_win(player, expand_node.move)
        if win:
            expand_node.winner = player
        cur_board.update(player, expand_node.move)

        for t in range(1, self.max_simulation_one_play + 1):
            is_full = not len(cur_board.neighbors)
            if win or is_full:
                break

            player = self.get_player[player]
            move = random.choice(list(cur_board.neighbors))
            win = cur_board.check_win(player, move)
            cur_board.update(player, move)

        cur_node = expand_node
        while cur_node:
            cur_node.sim_num += 1
            if win and cur_node.player == player:
                cur_node.win_num += 1
            cur_node = cur_node.parent


class Field:
    def __init__(self):
        self.height = BOARD_SIZE
        self.width = BOARD_SIZE

    def ai_move(self, x, y):
        ai_move(x, y)
        print(f'Компьютер сделал ход: ({x}, {y})')

    def player_move(self, x, y):
        player_move(x, y)
        print(f'Сделан ход: ({x}, {y})')


def AI_turn():
    MCTS_AI = MCTS(board,
                   players_in_turn=[1, 2],  # компьютер - 1
                   n_in_line=WINNING_SEQUENCE,
                   confidence=1.96,
                   time_limit=TIME_LIMIT,
                   max_simulation=MAX_SIMULATION,
                   max_simulation_one_play=MAX_SIMULATION_ONE_STEP)

    while True:
        move = MCTS_AI.get_action()
        x, y = move

        if is_free(x, y):
            break
    field.ai_move(x, y)


def is_free(x, y):
    """ проверка доступности """
    return 0 <= x < field.width and 0 <= y < field.height and board[x][y] == 0


def ai_move(x, y):
    if is_free(x, y):
        board[x][y] = 1
    else:
        print(f" Клетка ({x},{y}) занята. ")


def player_move(x, y):
    if is_free(x, y):
        board[x][y] = 2
    else:
        print(f" Клетка ({x},{y}) занята. ")


def brain_show():
    """ Отрисовка поля в консоле """
    st = '  '
    for i in range(len(board[0])):
        if i > 9:
            st += str(i) + ' '
        else:
            st += ' ' + str(i) + ' '
    print(st)
    c = 0
    for row in board:
        if c > 9:
            print(c, end=' ')
        else:
            print('', c, end=' ')
        c += 1
        st = ''
        for ii in row:
            if ii == 1:
                st += 'O  '
            elif ii == 2:
                st += 'X  '
            else:
                st += '-  '
        print(st)


def play():
    while 1:
        print('Для выхода их игры введите "q" .')
        x = input("Ваш ход, введите координаты через пробел: 'x y':")
        print()
        if x == 'q':
            print('Вы вышли из игры.')
            return None
        x = x.split()
        try:
            player_move(int(x[0]), int(x[1]))

        except Exception:
            print(f'Неправильно что-то написали, попробуйте ещё раз.')
            continue
        break
    return 0


def main():
    brain_show()

    while play() is not None:
        AI_turn()
        brain_show()


if __name__ == "__main__":
    field = Field()
    main()
