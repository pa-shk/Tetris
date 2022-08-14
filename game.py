import random
import time


def rotate(figure: '2d list of tuples', occupied, dimensions=(10, 10)):
    _, n = dimensions
    intersect = [i for i in figure[1] if i in occupied]
    border = [i for i in figure[1] if i[0] >= n]
    if not intersect and not border:
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


def at_border(occupied: 'list of tuples', piece: 'list of tuples', dimensions=(10, 10)):
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
        moves = 0
        is_new = True
        game_over = False
        print('The game starts now...')
        time.sleep(0.5)

        while not  game_over:
            if stable:
                figure_name = random.choice(['I', 'S',  'Z', 'L', 'J', 'T',  'O'])
                figure_name = input('Enter figure').upper()
                figure = [i for i in get_figure(figure_name, dimensions)]
                stable = False
                if not is_new:
                    print('Next...')
                time.sleep(1)
                is_new = False
            else:
                while True:
                    whole = figure[0] + occupied
                    stable = at_border(occupied, figure[0], dimensions)
                    print(display(whole, dimensions))
                    with open('debag', 'w') as file:
                        print(whole, file=file)
                    if stable:
                        occupied.extend(figure[0])
                        #print('Hit the border')
                        count = 0
                        for _ in range(dimensions[1]):
                            is_disapp, whole = disappear(whole, dimensions)
                            occupied = [i for i in occupied if i in whole]
                            if not is_disapp:
                                break
                            else:
                                count += 1
                        if count:
                            message = 'rows are broken!' if count > 1 else 'row is broken!'
                            print(count, message)
                            print(display(whole, dimensions))
                            time.sleep(1.5)
                        break

                    comm = input('Enter rotate, right or left\n').lower()
                    while not comm:
                        print('Enter something!')
                        comm = input('Enter rotate, right or left\n').lower()

                    if comm in 'rotate5' and figure_name !=  'O':
                        figure = rotate(figure, occupied, dimensions)
                    if comm in 'rightleft46':
                        figure = [move(i, occupied, direction=comm, dimensions=dimensions) for i in figure]
                    if not at_border(occupied,figure[0], dimensions):
                        figure = [move(i, occupied, dimensions=dimensions) for i in figure]
                        moves += 1

                game_over = is_finish(figure[0])
                if game_over:
                    print('Game Over!')
                    print(f"You've made {moves} moves")
                    time.sleep(0.5)
                    again = input('Wonna play again?\n')
                    if again not in  'yes_ok':
                        play = False


if __name__ == '__main__':
    main()
