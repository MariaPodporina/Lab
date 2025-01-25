import time
start_time = time.time()

def read_input(filename: any):
    ''' Функция считывания данных из файла "input.txt"'''
    with open(filename, 'r') as f:
        N, L, K = map(int, f.readline().strip().split())
        pieces = [tuple(map(int, f.readline().strip().split())) for _ in range(K)]
    return N, L, K, pieces

def right_position(board: list[list[int]], x:int, y:int, N:int):
    ''' Функция проверяющая допустима ли позиция для хода '''
    moves = [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for movesforx, movesfory in moves:
        if 0 <= x + movesforx < N and 0 <= y + movesfory < N and board[x + movesforx][y + movesfory] == 1:
            return False
    return True

def check_starting_position(pieces:  list[tuple[int, ...]] , N:int):
    ''' Функция проверяющая правильность изначального расположения фигур '''
    board = [[0] * N for _ in range(N)]
    for x, y in pieces:
        board[x][y] = 1

    for i in range(len(pieces)):
        x, y = pieces[i]
        if not right_position(board, x, y, N):
            return False
    return True

def place_pieces(board:list[list[int]], pieces: list[tuple[int, ...]], L:int, N:int, file:any, lineforx:int, linefory:int):
    ''' Функция для поиска всех возможных решений размещения фигуры '''
    if L == 0:
        file.write(' '.join(f"({x},{y})" for x,y in pieces)+'\n')
        return

    for i in range(lineforx, N):
        for j in range(linefory if i == lineforx else 0, N):
            if board[i][j] == 0 and right_position(board, i, j, N):
                board[i][j] = 1
                pieces.append((i, j))
                place_pieces(board, pieces, L - 1, N,file, i, j)
                pieces.pop()
                board[i][j] = 0
        linefory = 0


def print_board(board:list[list[int]], N:int):
    ''' Функция выводящая в консоль доску '''
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                print("#", end=" ")
            elif right_position(board, i, j, N):
                print("0", end=" ")
            else:
                print("*", end=" ")
        print()

def one_board(N):
    '''Функция считывающая из файла одно решение для вывода в консоль'''
    with open('output.txt', 'r') as file:
        first_line = file.readline().strip()
        if first_line == "no solutions":
            return
        tuple_strings = first_line.replace("(", "").replace(")", "").split()
        one_solution = [tuple(map(int, s.split(','))) for s in tuple_strings]
    new_board = [[0] * N for _ in range(N)]
    for x, y in one_solution:
        new_board[x][y] = 1
    print_board(new_board, N)

def write_output(file:any, pieces):
    ''' Функция записывающая все решения в файл "output.txt" '''
    with open(file, 'a') as f:
            f.write(' '.join(f"({x},{y})" for x,y in pieces)+'\n')

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
    with open('output.txt', 'w') as f:
        f.write("")
    f= open('output.txt', 'a')
    place_pieces(board, initial_positions, L, N, f, 0,0)
    f.close()
    write_output('output.txt', [])
    one_board(N)

if __name__ == "__main__":
    ''' Приводит в действие главную функцию '''
    main()

# ''' Подсчет количества решений'''
with open('output.txt', 'r') as file:
    line_count = sum(1 for line in file)
print(line_count)
''' Измерение времени выполнения'''
end_time = time.time()
elapsed_time = end_time - start_time
print('time: ', elapsed_time)