import random
import time
import json


def rotate(figure: '2d list of tuples', occupied: 'list of tuples', dimensions=(10, 10)):
    _, n = dimensions
    intersect = [i for i in figure[1] if i in occupied]
    border = [i for i in figure[1] if i[0] >= n]
    if not intersect and not border:
        out_fig = figure.copy()
        zero = out_fig.pop(0)
        out_fig.append(zero)
        return out_fig
    return figure


def move(old_ind: 'list of tuples', occupied: 'list of tuples', direction='down',
         dimensions=(10, 10)) -> 'list of tuples':
    m, n = dimensions
    border = False
    new = []
    for i in old_ind:
        if direction == 'down':
            new.append((i[0] + 1, i[1]))
            if i[0] + 1 == n or (i[0] + 1, i[1]) in occupied:
                border = True
        if direction in 'right6':
            new.append((i[0], i[1] + 1))
            if i[1] + 1 == m or (i[0], i[1] + 1) in occupied:
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


def is_finish(occupied: 'list of tuples', indexes: 'list of tuples', dimensions=(10, 10)):
    border = at_border(occupied, indexes, dimensions)
    for i in indexes:
        if i[0] == 0 and border:
            return True


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


def display(indexes: 'list of tuples', dimensions=(10, 10)) -> None:
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
    print(*[' '.join(i) for i in matrix], sep='\n', end='\n\n')


def get_cash() -> '(bool, dict)':
    try:
        with open('cash') as file:
            cash = json.load(file)
        return True, cash
    except FileNotFoundError:
        with open('cash', 'w') as file:
            cash = {'dimensions': (10, 10), 'progress': []}
            json.dump(cash, file)
    return False, cash


def check_dimensions(user_input: str)-> 'bool or tuple':
    try:
        m, n = [int(i) for i in user_input.split()]
        if all([m > 4, n > 4, m < 21, n < 21]):
            return (m, n)
    except ValueError:
        return False
    return False



def main():
    saved, cash = get_cash()

    if saved:
        print('Your saved settings loaded')
    else:
        print('Default settings loaded.')

    dimensions = cash['dimensions']
    progress = cash['progress']

    print(f'''You play with {dimensions[0]} X {dimensions[1]} board
Max score {max([*progress, 0])} moves so far''')
    change = input('Wanna change settings?\n')

    if change.lower() in 'yesok':
        user_dimensions = check_dimensions(input('Enter dimensions. Ex: 10 10\n'))
        if user_dimensions:
            cash['dimensions'] = user_dimensions
        else:
            print('''Wrong dimensions. 
Should be 2 number. No more than 20 and no less that 5 each''')
        if input('Wanna reset progress\n').lower() in 'yesok':
            cash['progress'] = []
        dimensions = cash['dimensions']
        progress = cash['progress']

    play = True
    while play:
        with open('cash', 'w') as file:
            json.dump(cash, file)
        occupied = []
        stable = True
        moves = 0
        is_new = True
        game_over = False
        print('The game starts now...')
        time.sleep(0.5)

        while not game_over:
            if stable and not is_new:
                occupied.extend(figure[0])
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
                    display(whole, dimensions)
                    time.sleep(1.5)
                print('Next...')
                time.sleep(1)

            if stable:
                figure_name = random.choice(['I', 'S', 'Z', 'L', 'J', 'T', 'O'])
                # figure_name = input('Enter figure').upper()
                figure = [i for i in get_figure(figure_name, dimensions)]
                is_new = False

            whole = figure[0] + occupied
            stable = at_border(occupied, figure[0], dimensions)
            with open('debag', 'w') as file:
                print(whole, file=file)
            display(whole, dimensions)

            game_over = is_finish(occupied, figure[0], dimensions)
            if game_over:
                print('Game Over!')
                print(f"You've made {moves} moves")
                if progress and moves > max(progress):
                    print("It's your best score!")
                elif progress and moves > progress[-1]:
                    print("It's an improvment!")
                time.sleep(0.5)
                progress.append(moves)
                again = input('Wanna play again?\n')
                if again not in 'yesok':
                    play = False

            if not stable:
                comm = input('Enter rotate(5), right(4), left(6) or down(2)\n').lower()
                while not comm:
                    comm = input('Enter something!').lower()

                if comm in 'rotate5' and figure_name != 'O':
                    figure = rotate(figure, occupied, dimensions)
                if comm in 'rightleft46':
                    figure = [move(i, occupied, direction=comm, dimensions=dimensions) for i in figure]

                figure = [move(i, occupied, dimensions=dimensions) for i in figure]
                moves += 1


if __name__ == '__main__':
    main()
