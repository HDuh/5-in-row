import math


def check_win(pos):
    if pos == 5:
        return True
    return False


def minimax(position, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_win(position):
        return position

    if maximizing_player:
        max_eval = -math.inf
        # поиск среди возможных ходовgit
        for child_i in position:
            cur_eval = minimax(child_i, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, cur_eval)
            alpha = max(alpha, cur_eval)
            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = math.inf
        for child_i in position:
            cur_eval = minimax(child_i, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, cur_eval)
            beta = min(beta, cur_eval)
            if beta <= alpha:
                break

        return min_eval
