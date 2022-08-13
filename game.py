def rotate(figure: 'list of tuples', occupied):
    intersect = [i for i in figure[1] if i in occupied]
    if not intersect:
        out_fig = figure.copy()
        zero = out_fig.pop(0)
        out_fig.append(zero)
        return out_fig
    return figure


def move(old_ind: 'list of tuples', direction='down', dimensions=(10, 10)) -> 'list of tuples':
    m, n = dimensions
    border = False
    new = []
    for i in old_ind:
        if direction == 'down':
            new.append((i[0] + 1, i[1]))
        if direction == 'right':
            new.append((i[0], i[1] + 1))
            if i[1] + 1 == m:
                border = True
        if direction == 'left':
            new.append((i[0], i[1] - 1))
            if i[1] - 1 < 0:
                border = True
    if border:
        return old_ind
    return new


def border(occupied: 'list of tuples', piece: 'list of tuples', dimensions=(10, 10)):
    m, n = dimensions
    floor = [(n - 1, i) for i in range(m)]
    above_piece = [(i[0] - 1, i[1]) for i in occupied]
    return bool([i for i in piece if i in floor + above_piece])


def disappear(old_ocupp: 'list of tuples', dimensions=(10, 10)) -> 'list of tuples':
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


def is_finish(indexes: 'list of tuples'):
    for i in indexes:
        if i[0] == 0:
            return True


def display(indexes: 'list of tuples', dimensions=(10, 10)) -> str:
    m, n = dimensions
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            if (i, j) in indexes:
                row.append('0')
            else:
                row.append('-')
        matrix.append(row)
    return '\n'.join([' '.join(i) for i in matrix]) + '\n'


def get_figure(figure_name: str, dimensions=(4, 4)) -> 'list of tuples':
    m, _ = dimensions
    O = [[(0, 1), (0, 2), (1, 1), (1, 2)]]
    I = [[(0, 1), (1, 1), (2, 1), (3, 1)], [(0, 0), (0, 1), (0, 2), (0, 3)]]
    S = [[(0, 1), (0, 2), (1, 0), (1, 1)], [(0, 1), (1, 1), (1, 2), (2, 2)]]
    Z = [[(0, 1), (0, 2), (1, 2), (1, 3)], [(0, 2), (1, 1), (1, 2), (2, 1)]]
    L = [[(0, 1), (1, 1), (2, 1), (2, 2)], [(0, 2), (1, 0), (1, 1), (1, 2)], [(0, 1), (0, 2), (1, 2), (2, 2)],
         [(0, 1), (0, 2), (0, 3), (1, 1)]]

    J = [[(0, 2), (1, 2), (2, 1), (2, 2)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 1), (0, 2), (1, 1), (2, 1)],
         [(0, 1), (1, 1), (1, 2), (1, 3)]]

    T = [[(0, 1), (1, 1), (1, 2), (2, 1)], [(0, 1), (1, 0), (1, 1), (1, 2)], [(0, 2), (1, 1), (1, 2), (2, 2)],
         [(0, 1), (0, 2), (0, 3), (1, 2)]]

    figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}
    template = figures[figure_name]
    scaled = []
    shift = (m - 4) // 2
    for piece in template:
        scaled.append([(i[0], i[1] + shift) for i in piece])
    return scaled


def main():
    dimensions = tuple(int(i) for i in input().split())
    print(display([], dimensions))

    occupied = []
    game_over = False
    figure = None
    stable = False

    while True:
        comm = input()
        if comm == 'piece':
            if figure:
                occupied.extend(figure[0])
            figure = [i for i in get_figure(input(), dimensions)]
        if comm == 'rotate' and not stable:
            figure = rotate(figure, occupied)
        if comm in 'right_left' and not stable:
            figure = [move(i, direction=comm, dimensions=dimensions) for i in figure]
        if comm == 'exit':
            break

        whole = figure[0] + occupied

        if comm == 'break':
            for _ in range(dimensions[1]):
                whole = disappear(whole, dimensions)
                occupied = [i for i in occupied if i in whole]
            figure[0] = [i for i in figure[0] if i in whole]

        print(display(whole, dimensions))

        if game_over:
            print(game_over)
            break

        stable = border(occupied, figure[0], dimensions)
        if not stable:
            figure = [move(i, dimensions=dimensions) for i in figure]

        if is_finish(figure[0]):
            game_over = 'Game Over!'


if __name__ == '__main__':
    main()
