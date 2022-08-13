def rotate(figure: 'list of tuples') -> 'list of tuples':
    out_fig = figure.copy()
    zero = out_fig.pop(0)
    out_fig.append(zero)
    return out_fig


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


def main():
    #   initial position indexes
    O = [[(0, 4), (0, 5), (1, 4), (1, 5)]]
    I = [[(0, 4), (1, 4), (2, 4), (3, 4)], [(0, 3), (0, 4), (0, 5), (0, 6)]]
    S = [[(0, 4), (0, 5), (1, 3), (1, 4)], [(0, 4), (1, 4), (1, 5), (2, 5)]]
    Z = [[(0, 4), (0, 5), (1, 5), (1, 6)], [(0, 5), (1, 4), (1, 5), (2, 4)]]
    L = [[(0, 4), (1, 4), (2, 4), (2, 5)], [(0, 5), (1, 3), (1, 4), (1, 5)], [(0, 4), (0, 5), (1, 5), (2, 5)],
         [(0, 4), (0, 5), (0, 6), (1, 4)]]
    J = [[(0, 5), (1, 5), (2, 4), (2, 5)], [(0, 3), (0, 4), (0, 5), (1, 5)], [(0, 4), (0, 5), (1, 4), (2, 4)],
         [(0, 4), (1, 4), (1, 5), (1, 6)]]
    T = [[(0, 4), (1, 4), (1, 5), (2, 4)], [(0, 4), (1, 3), (1, 4), (1, 5)], [(0, 5), (1, 4), (1, 5), (2, 5)],
         [(0, 4), (0, 5), (0, 6), (1, 5)]]
    figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}

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
            figure = [i for i in figures[input()]]
        if comm == 'rotate' and not border(occupied, figure[0], dimensions):
            figure = rotate(figure)
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








# TODO

O = [[(0, 4), (0, 5), (1, 4), (1, 5)]]
I = [[(0, 4), (1, 4), (2, 4), (3, 4)], [(0, 3), (0, 4), (0, 5), (0, 6)]]
S = [[(0, 4), (0, 5), (1, 3), (1, 4)], [(0, 4), (1, 4), (1, 5), (2, 5)]]
Z = [[(0, 4), (0, 5), (1, 5), (1, 6)], [(0, 5), (1, 4), (1, 5), (2, 4)]]
L = [[(0, 4), (1, 4), (2, 4), (2, 5)], [(0, 5), (1, 3), (1, 4), (1, 5)], [(0, 4), (0, 5), (1, 5), (2, 5)],
     [(0, 4), (0, 5), (0, 6), (1, 4)]]
J = [[(0, 5), (1, 5), (2, 4), (2, 5)], [(0, 3), (0, 4), (0, 5), (1, 5)], [(0, 4), (0, 5), (1, 4), (2, 4)],
     [(0, 4), (1, 4), (1, 5), (1, 6)]]
T = [[(0, 4), (1, 4), (1, 5), (2, 4)], [(0, 4), (1, 3), (1, 4), (1, 5)], [(0, 5), (1, 4), (1, 5), (2, 5)],
     [(0, 4), (0, 5), (0, 6), (1, 5)]]
figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}

# for f in figures.values():
#     #print(f)
#     for i in f:
#         print(display(i))

#print(display([(0, 4), (0, 5), (1, 4), (1, 5)]))
