def rotate(figure: '2d list') -> '2d list':
    out_fig = figure.copy()
    zero = out_fig.pop(0)
    out_fig.append(zero)
    return out_fig


def empty_playground(dimensions=(10, 10)) -> '2d list':
    m, n = dimensions
    matrix = []
    for _ in range(n):
        row = ['-' for _ in range(m)]
        matrix.append(row)
    return matrix


def to_str(matrix: '2d list') -> str:
    return '\n'.join([' '.join(i) for i in matrix]) + '\n'


def get_indexes(in_matrix: '2d list') -> 'list of tuples':
    indexes = []
    for i in range(len(in_matrix)):
        for j in range(len(in_matrix[i])):
            if in_matrix[i][j] == '0':
                indexes.append((i, j))
    return indexes


def move(in_matrix: '2d list', direction='down') -> '2d list':
    n = len(in_matrix)
    m = len(in_matrix[0])
    matrix = empty_playground((m, n))

    old = get_indexes(in_matrix)
    new = []
    for i in old:
        if direction == 'down':
            new.append((i[0] + 1, i[1]))
        elif direction == 'right':
            new.append((i[0], i[1] + 1))
        elif direction == 'left':
            new.append((i[0], i[1] - 1))

    for i in new:
        try:
            matrix[i[0]][i[1]] = '0'
            if i[1] < 0:
                raise IndexError
        except IndexError:
            return in_matrix
    return matrix


def on_floor(in_matrix: '2d list'):
    return bool([i for i in in_matrix[-1] if i == '0'])


def on_border(indexes: 'list of tuples', in_matrix: '2d list'):
    border = [(i[0] - 1, i[1]) for i in indexes]
    for i in range(len(in_matrix)):
        for j in range(len(in_matrix[0])):
            if in_matrix[i][j] == '0' and (i, j) in border:
                return True


def merge(matrix_1: '2d list', matrix_2: '2d list') -> '2d list':
    matrix = [i.copy() for i in matrix_1]
    for i in range(len(matrix_2)):
        for j in range(len(matrix_2[0])):
            if matrix_2[i][j] == '0':
                matrix[i][j] = '0'
    return matrix


def disappear(old_ocupp: 'list of tuples', dimensions=(10, 5)) -> 'list of tuples':
    m, _ = dimensions
    new_occup = []
    if old_ocupp:
        for row_n in range(max(old_ocupp)[0] + 1):
            if len([i for i in old_ocupp if i[0] == row_n]) == m:
                full = row_n
                for i in old_ocupp:
                    if i[0] == full:
                        continue
                    elif i[0] < full:
                        new_occup.append((i[0] + 1, i[1]))
                    else:
                        new_occup.append((i[0], i[1]))
                return new_occup
    return old_ocupp


def finish(indexes: 'list of tuples'):
    for i in indexes:
        if i[0] == 0:
            return True


def from_ind(indexes: 'list of tuples', dim=(10, 10)):
    matrix = empty_playground(dim)
    for coord in indexes:
        matrix[coord[0]][coord[1]] = '0'
    return matrix


def main():
    #  initial position indexes
    O = [[(0, 4), (0, 5), (1, 4), (1, 5)]]
    I = [[(0, 4), (1, 4), (2, 4), (3, 4)], [(0, 3), (0, 4), (0, 5), (0, 6)]]
    S = [[(0, 4), (0, 5), (1, 3), (1, 4)], [(0, 4), (1, 4), (1, 5), (2, 5)]]
    Z = [[(0, 4), (0, 5), (1, 5), (1, 6)], [(0, 5), (1, 4), (1, 5), (2, 4)]]
    L = [[(0, 4), (1, 4), (2, 4), (2, 5)], [(0, 5), (1, 3), (1, 4), (1, 5)], [(0, 4), (0, 5), (1, 5), (2, 5)], [(0, 4), (0, 5), (0, 6), (1, 4)]]
    J = [[(0, 5), (1, 5), (2, 4), (2, 5)], [(0, 3), (0, 4), (0, 5), (1, 5)], [(0, 4), (0, 5), (1, 4), (2, 4)], [(0, 4), (1, 4), (1, 5), (1, 6)]]
    T = [[(0, 4), (1, 4), (1, 5), (2, 4)], [(0, 4), (1, 3), (1, 4), (1, 5)], [(0, 5), (1, 4), (1, 5), (2, 5)], [(0, 4), (0, 5), (0, 6), (1, 5)]]
    figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}

    dimensions = tuple(int(i) for i in input().split())
    empty = empty_playground(dimensions)
    print(to_str(empty))

    occupied = []
    game_over = False
    figure = None

    while True:
        comm = input()
        if comm == 'piece':
            if figure:
                occupied.extend(get_indexes(figure[0]))
            curr_fig = figures[input()]
            figure = [from_ind(i, dimensions) for i in curr_fig]
        if comm == 'rotate' and not on_floor(figure[0]) and not on_border(occupied, figure[0]):
            figure = rotate(figure)
        if comm in 'right_left' and not on_floor(figure[0]) and not on_border(occupied, figure[0]):
            figure = [move(i, direction=comm) for i in figure]
        if comm == 'exit':
            break
        whole = get_indexes(figure[0]) + occupied
        if comm == 'break':
            for _ in range(dimensions[1]):
                whole = disappear(whole, dimensions)
                occupied = [i for i in occupied if i in whole]
            figure[0] = []

        print(to_str(from_ind(whole, dimensions)))
        if game_over:
            print(game_over)
            break

        if not on_border(occupied, figure[0]) and figure[0]:
            figure = [move(i) for i in figure]

        if finish(get_indexes(figure[0])):
            game_over = 'Game Over!'


if __name__ == '__main__':
    main()
