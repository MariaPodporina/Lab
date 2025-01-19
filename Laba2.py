# import time
# start_time = time.time()

def read_input(filename: any):
    ''' Функция считывания данных из файла "input.txt"'''
    with open(filename, 'r') as f:
        N, L, K = map(int, f.readline().strip().split())
        pieces = [tuple(map(int, f.readline().strip().split())) for _ in range(K)]
    return N, L, K, pieces

def valid_position(board: list[list[int]], x:int, y:int, N:int):
    ''' Функция проверяющая допустима ли позиция для хода '''
    moves = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in moves:
        if 0 <= x + dx < N and 0 <= y + dy < N and board[x + dx][y + dy] == 1:
            return False
    return True

def check_starting_position(pieces:  list[tuple[int, ...]] , N:int):
    ''' Функция проверяющая правильность изначального расположения фигур '''
    board = [[0] * N for _ in range(N)]
    for x, y in pieces:
        board[x][y] = 1

    for i in range(len(pieces)):
        x, y = pieces[i]
        if not valid_position(board, x, y, N):
            return False
    return True

def place_pieces(board:list[list[int]], pieces: list[tuple[int, ...]], L:int, N:int, solutions:list, line:int, col:int):
    ''' Функция для поиска всех возможных решений размещения фигуры '''
    if L == 0:
        solutions.append(pieces.copy())
        return

    for i in range(line, N):
        for j in range(col if i == line else 0, N):
            if board[i][j] == 0 and valid_position(board, i, j, N):
                board[i][j] = 1
                pieces.append((i, j))
                place_pieces(board, pieces, L - 1, N, solutions, i, j)
                pieces.pop()
                board[i][j] = 0
        col = 0

def print_board(board:list[list[int]], N:int):
    ''' Функция выводящая в консоль доску '''
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                print("#", end=" ")
            elif valid_position(board, i, j, N):
                print("0", end=" ")
            else:
                print("*", end=" ")
        print()

def write_output(file:any, solutions:list):
    ''' Функция записывающая все решения в файл "output.txt" '''
    with open(file, 'w') as f:
        if not solutions:
            f.write("no solutions\n")
        else:
            for solution in solutions:
                f.write(' '.join(f"({x},{y})" for x, y in solution) + '\n')

def main():
    ''' Функция работающая со всеми функциями '''
    N, L, K, initial_positions = read_input('input.txt')

    board = [[0] * N for _ in range(N)]

    for x, y in initial_positions:
        board[x][y] = 1
    if not check_starting_position(initial_positions, N):
        write_output('output.txt', [])
        print("no solutions")
        return

    solutions = []
    place_pieces(board, initial_positions, L, N, solutions, 0, 0)
    write_output('output.txt', solutions)

    with open('output.txt', 'r') as file:
        first_line = file.readline().strip()
        tuple_strings = first_line.replace("(", "").replace(")", "").split()
        one_solution = [tuple(map(int, s.split(','))) for s in tuple_strings]
    new_board = [[0] * N for _ in range(N)]

    for x, y in one_solution:
        new_board[x][y] = 1
    print_board(new_board, N)
if __name__ == "__main__":
    ''' Приводит в действие главную функцию '''
    main()

# ''' Подсчет количества решений'''
# with open('output.txt', 'r') as file:
#     line_count = sum(1 for line in file)
# print(line_count)
# ''' Измерение времени выполнения'''
# end_time = time.time()
# elapsed_time = end_time - start_time
# print('Elapsed time: ', elapsed_time)