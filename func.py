def decode(piece: '1d list', dimensions=(10, 10)) -> '2d list':
    matrix = empty_playground(dimensions)
    m, n = dimensions
    for i in piece:
        matrix[i // m][i % m] = '0'
    return matrix


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


def merge(matrix_1, matrix_2):
    matrix = [i.copy() for i in matrix_1]
    for i in range(len(matrix_2)):
        for j in range(len(matrix_2[0])):
            if matrix_2[i][j] == '0':
                matrix[i][j] = '0'
    return matrix


def disappear(old_ocupp: 'list of tuples', dimensions=(10, 5)) -> 'list of tuples':
    m, _ = dimensions
    new_occup = []
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
    O = [[4, 14, 15, 5]]
    I = [[4, 14, 24, 34], [3, 4, 5, 6]]
    S = [[5, 4, 14, 13], [4, 14, 15, 25]]
    Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
    L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
    J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
    T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
    figures = {'I': I, 'S': S, 'Z': Z, 'L': L, 'J': J, 'T': T, 'O': O}

    dimensions = tuple(int(i) for i in input().split())
    empty = empty_playground(dimensions)
    print(to_str(empty))

    occupied = []
    flag = False
    decoded = [[]]

    while True:
        comm = input()
        if comm == 'piece':
            occupied.extend(get_indexes(decoded[0]))
            curr_fig = figures[input()]
            decoded = [decode(i, dimensions) for i in curr_fig]
        elif comm == 'rotate' and not on_floor(decoded[0]) and not on_border(occupied, decoded[0]):
            decoded = rotate(decoded)
        elif comm in 'right_left' and not on_floor(decoded[0]) and not on_border(occupied, decoded[0]):
            decoded = [move(i, direction=comm) for i in decoded]
        elif comm == 'exit':
            break

        curr_ind = get_indexes(decoded[0])
        clean = curr_ind + occupied
        break_ = False
        if comm == 'break':
            clean = disappear(curr_ind + occupied, dimensions)
            occupied = [i for i in occupied if i in clean]
            clean = disappear(clean, dimensions)
            occupied = [i for i in occupied if i in clean]
            decoded[0] = []
            break_ = True

        print(to_str(from_ind(clean, dimensions)))
        if flag:
            print(flag)
            break

        if not on_border(occupied, decoded[0]) and not break_:
            decoded = [move(i) for i in decoded]

        if finish(get_indexes(decoded[0])):
            flag = 'Game Over!'


if __name__ == '__main__':
    pass
    main()
