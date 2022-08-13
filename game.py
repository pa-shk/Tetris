import random


def rotate(figure: 'list of tuples', occupied):
    intersect = [i for i in figure[1] if i in occupied]
    if not intersect:
        out_fig = figure.copy()
        zero = out_fig.pop(0)
        out_fig.append(zero)
        return out_fig
    return figure


def move(old_ind: 'list of tuples', occupied: 'list of tuples', direction='down', dimensions=(10, 10)) -> 'list of tuples':
    m, n = dimensions
    border = False
    new = []
    for i in old_ind:
        if direction == 'down':
            new.append((i[0] + 1, i[1]))
            if (i[0] + 1, i[1]) in occupied:
                border = True
        if direction in 'right6':
            new.append((i[0], i[1] + 1))
            if i[1] + 1 == m or (i[0] + 1, i[1]) in occupied:
                border = True
        if direction in 'left4':
            new.append((i[0], i[1] - 1))
            if i[1] - 1 < 0 or (i[0], i[1] - 1) in occupied:
                border = True
    if border:
        return old_ind
    return new


def border(occupied: 'list of tuples', piece: 'list of tuples', dimensions=(10, 10)):
    m, n = dimensions
    floor = [(n - 1, i) for i in range(m)]
    above_piece = [(i[0] - 1, i[1]) for i in occupied]
    return bool([i for i in piece if i in floor + above_piece])


def disappear(old_ocupp: 'list of tuples', dimensions=(10, 10)):
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
                return True, new_occup
    return False, old_ocupp


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
    play = True
    while play:
        #dimensions = tuple(int(i) for i in input('Enter the size of playground. Ex: 10 10\n').split())
        dimensions = (10, 10)
        #print(display([], dimensions))
        occupied = []
        figure = None
        stable = True

        print('The game starts now')
        is_new = True

        while True:
            if stable:
                figure_name = random.choice(['I', 'S',  'Z', 'L', 'J', 'T',  'O'])
                #figure_name = input().upper()
                figure = [i for i in get_figure(figure_name, dimensions)]
                stable = False
                if not is_new:
                    print('next')
                is_new = False

            if not stable:
                while True:
                    whole = figure[0] + occupied
                    stable = border(occupied, figure[0], dimensions)
                    print(display(whole, dimensions))
                    print(whole)
                    if stable:
                        occupied.extend(figure[0])
                        print( 'Hit the floor')

                        count = 0
                        for _ in range(dimensions[1]):
                            is_disapp, whole = disappear(whole, dimensions)
                            occupied = [i for i in occupied if i in whole]
                            if not is_disapp:
                                break
                            else:
                                count += 1
                        if count:
                            print(count, 'rows are broken!')
                            print(display(whole, dimensions))
                        break

                    comm = input('Enter rotate, right or left\n').lower()
                    while not comm:
                        print('Enter something!')
                        comm = input('Enter rotate, right or left\n').lower()

                    if comm in 'rotate5':
                        figure = rotate(figure, occupied)
                    if comm in 'rightleft46':
                        figure = [move(i, occupied, direction=comm, dimensions=dimensions) for i in figure]
                    figure = [move(i, occupied, dimensions=dimensions) for i in figure]

            game_over = is_finish(figure[0])
            if game_over:
                print('Game Over!')
                again = input('Wonna play again?')
                if again not in  'yes_ok':
                    play = False
                break

if __name__ == '__main__':
    main()#

# f = [(0, 4), (1, 4), (1, 5), (2, 4), (8, 0), (8, 1), (9, 0), (9, 1), (8, 2), (8, 3), (9, 2), (9, 3), (8, 5), (8, 6), (9, 4), (9, 5), (7, 4), (7, 5), (7, 6), (8, 4), (6, 3), (6, 4), (7, 2), (7, 3), (8, 7), (8, 8), (9, 7), (9, 8), (5, 7), (5, 8), (6, 8), (7, 8), (3, 4), (4, 4), (5, 3), (5, 4)]
#
# print(disappear(f))
# print(display(f))
