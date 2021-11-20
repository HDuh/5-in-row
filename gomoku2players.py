import sys

import pygame

# цвета
BLACK = (0, 0, 0)
BLUE = (199, 215, 255)
GREEN = (0, 255, 0)
GREY = (130, 130, 130)
RED = (255, 148, 150)

FIELD_SIZE = 10  # размер поля
WINNING_SEQUENCE = 5  # количество ячеек в ряд для победы


class Game:
    def __init__(self, field_size):
        pygame.init()
        self.game_over = False
        self.field_size = field_size
        self.field = [[0] * self.field_size for _ in range(self.field_size)]  # массив клеток игры
        self.last_pos = None
        self.move_control = 0

        # размер одной ячейки
        self.cell_size = 40

        # размер границы между ячейками
        self.margin = 3

        # размеры поля
        self.width = self.height = self.cell_size * self.field_size + self.margin * (self.field_size + 1)
        self.window_size = (self.width, self.height)

        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Обратные крестики-нолики')

    def computer_move(self):
        pass

    def event_handler(self):
        """ Обработка событий простановки клеток и нажатий на клавиатуру """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # начать игру заново
                    self.game_over = False
                    self.field = [[0] * self.field_size for _ in range(self.field_size)]
                    self.move_control = 0
                    self.screen.fill(BLACK)


            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                # обработка клика на клеточки

                x_mouse, y_mouse = pygame.mouse.get_pos()
                column = x_mouse // (self.margin + self.cell_size)
                row = y_mouse // (self.margin + self.cell_size)
                self.last_pos = (row, column)

                if self.field[row][column] == 0:
                    if self.move_control % 2 == 0:

                        self.field[row][column] = 'x'

                    else:
                        self.field[row][column] = 'o'
                    self.move_control += 1
                    print('last pos:', self.last_pos)

    def check_win(self):
        """ Проверка всех возможных комбинаций """
        if self.row_win():
            return True
        if self.column_win():
            return True
        if self.right_diagonal_win():
            return True
        if self.left_diagonal_win():
            return True

        return False

    def row_win(self):
        """ Проверка выйгрыша по строке относитльно последнего хода """

        last_row = self.last_pos[0]
        last_col = self.last_pos[1]
        last_cell_sign = self.field[last_row][last_col]

        counter = 0
        row_list = []
        for col in range(last_col - 4, last_col + 5):

            if col < 0:
                continue
            if col >= self.field_size:
                break
            if self.field[last_row][col] == last_cell_sign:
                counter += 1
                row_list.append((last_row, col))

            else:
                counter = 0

            if counter == WINNING_SEQUENCE:
                return True

    def column_win(self):
        """ Проверка выйгрыша по стролбцу """

        last_row = self.last_pos[0]
        last_col = self.last_pos[1]
        last_cell_sign = self.field[last_row][last_col]

        counter = 0
        for row in range(last_row - 4, last_row + 5):
            if row < 0:
                continue
            if row >= self.field_size:
                break
            if self.field[row][last_col] == last_cell_sign:
                counter += 1
            else:
                counter = 0

            if counter == WINNING_SEQUENCE:
                return True

    def right_diagonal_win(self):
        """ Проверка выйгрыша по диагонали из нижнего левого к верхнему правому углу"""

        last_row = self.last_pos[0]
        last_col = self.last_pos[1]
        last_cell_sign = self.field[last_row][last_col]

        counter = 0
        for shift in range(-4, 5):
            check_row = last_row - shift
            check_col = last_col + shift

            if check_row >= self.field_size or check_col < 0:
                continue
            if check_row < 0 or check_col >= self.field_size:
                break

            if self.field[check_row][check_col] == last_cell_sign:
                counter += 1
            else:
                counter = 0
            if counter == WINNING_SEQUENCE:
                return True

    def left_diagonal_win(self):
        """ Проверка выйгрыша по диагонали с верхнего левого к нижнему правому углу"""

        last_row = self.last_pos[0]
        last_col = self.last_pos[1]
        last_cell_sign = self.field[last_row][last_col]

        counter = 0
        for shift in range(-4, 5):
            check_row = last_row + shift
            check_col = last_col + shift

            if check_row >= self.field_size or check_col >= self.field_size:
                break
            if check_row < 0 or check_col < 0:
                continue
            if self.field[check_row][check_col] == last_cell_sign:
                counter += 1
            else:
                counter = 0
            if counter == WINNING_SEQUENCE:
                return True

    def draw_field(self):
        """ Отрисовка поля """
        for row in range(self.field_size):
            for col in range(self.field_size):
                if self.field[row][col] == 'x':
                    color = BLUE
                elif self.field[row][col] == 'o':
                    color = RED
                else:
                    color = GREY

                x = col * self.cell_size + (col + 1) * self.margin
                y = row * self.cell_size + (row + 1) * self.margin
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

                if color == BLUE:
                    pygame.draw.line(self.screen, BLACK, (x + 12, y + 12),
                                     (x + self.cell_size - 12, y + self.cell_size - 12), 4)

                    pygame.draw.line(self.screen, BLACK, (x + self.cell_size - 12, y + 12),
                                     (x + 12, y + self.cell_size - 12), 4)
                if color == RED:
                    pygame.draw.circle(self.screen, BLACK, (x + self.cell_size // 2, y + self.cell_size // 2),
                                       self.cell_size // 2 - 8, 3)


    def run(self):
        while True:
            self.event_handler()
            self.draw_field()
            if self.move_control > 0:
                if self.check_win():
                    if (self.move_control - 1) % 2 == 0:  # x
                        winner = 'X'
                    else:
                        winner = 'O'

                    self.screen.fill(BLACK)
                    font = pygame.font.SysFont('serif', 15)
                    winner = f'Победил "{winner}". Чтобы начать сначала нажмите Пробел'
                    text1 = font.render(winner, False, GREY)
                    text_rect = text1.get_rect()
                    text_x = self.screen.get_width() / 2 - text_rect.width / 2
                    text_y = self.screen.get_height() / 2 - text_rect.height / 2
                    self.screen.blit(text1, [text_x, text_y])
                    self.game_over = True

            pygame.display.update()



if __name__ == "__main__":
    game = Game(FIELD_SIZE)
    game.run()
