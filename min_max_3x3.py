import math
import random
import time

FIELD_SIZE = 3


class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class Human(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None

        while not valid_square:
            square = input(self.letter + '\'s turn. Input move: ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')

        return val


class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        self.minmax_deep = 0

    def get_move(self, game):
        if len(game.available_moves()) == FIELD_SIZE * FIELD_SIZE:
            square = random.choice(game.available_moves())
        else:
            square = self.minmax(game, self.letter)['position']
            print(f'Глубина минмакса: {self.minmax_deep}')
        return square

    def minmax(self, state, player):
        self.minmax_deep += 1
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'
        # firstly check previous move is a winner
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                            state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minmax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class TicTacToe:
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return [' ' for _ in range(FIELD_SIZE*FIELD_SIZE)]

    def print_board(self):
        for row in [self.board[i * FIELD_SIZE: (i + 1) * FIELD_SIZE] for i in range(FIELD_SIZE)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j * FIELD_SIZE, (j + 1) * FIELD_SIZE)] for j in range(FIELD_SIZE)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            # if self.winner(square, letter):
            #     self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # проверка на выйгрыш
        row_ind = math.floor(square / FIELD_SIZE)
        row = self.board[row_ind * FIELD_SIZE:(row_ind + 1) * FIELD_SIZE]

        if all([s == letter for s in row]):
            return True
        col_ind = square % FIELD_SIZE
        column = [self.board[col_ind + i * FIELD_SIZE] for i in range(FIELD_SIZE)]
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == ' ']


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, letter):

            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter
            letter = 'O' if letter == 'X' else 'X'

        time.sleep(0.8)

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    x_play = Human('X')
    o_play = ComputerPlayer('O')

    t = TicTacToe()

    play(t, x_play, o_play, print_game=True)
