class Piece:
    def __init__(self, x: int, y: int):
        """
        Инициализирует класс фигуры с возможностью ввести координаты
        :param x: Координата X
        :param y: Координата Y
        """
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.moves = (
            (-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)
        )

class Board:
    def __init__(self, size: int, occupied: dict = None):
        """
        Инициализирует класс шахматной доски
        :param size: Размер доски по одной из координат
        :param occupied: Словарь, с ключом координат ячеек (x, y), и со значением:
            -1 - фигура,
            0 - ячейка пуста,
            >0 - ячейка находится под аттакой
        """
        if occupied is None:
            self.occupied = dict()
        else:
            self.occupied = occupied
        self.size = size
        self.pieces = [] # Все шахматные фигуры которые поставили на доску. Сотоит из экземпляров класса Piece

    def attacked_positions(self, piece: Piece):
        """
        Вызывается для расчета координат ячеек под боем
        :param piece: Принимает экземпляр класса Piece
        :return: Возвращает координаты всех ходов этой фигуры
        """
        attacked_tiles = []
        for i in piece.moves:
            if piece.x + i[0] < 0 or piece.y + i[1] < 0 or piece.x + i[0] > self.size - 1 or piece.y + i[1] > self.size - 1:
                continue
            else:
                attacked_tiles.append((piece.x + i[0], piece.y + i[1]))
        return attacked_tiles

    def is_save(self, piece: Piece):
        """
        Проверяет можно ли поставить фигуру
        :param piece: Принимает экземпляр класса Piece
        :return: Возвращает True, если фигуру можно поставить. False - если фигуру нельзя поставить
        """
        if piece.pos in self.occupied or piece.x > self.size or piece.y > self.size:
            return False
        return True

    def place(self, piece: Piece):
        """
        Добавляет piece в список фигур и добавляет координаты фигуры и ее ходы во множество occupied
        :param piece: экземпляр класса Piece
        :return: None
        """
        if self.is_save(piece):
            self.pieces.append(piece.pos)
            self.occupied[piece.pos] = -1
            for i in self.attacked_positions(piece):
                if self.occupied.get(i) is None:
                    self.occupied[i] = 1
                else:
                    self.occupied[i] += 1

    def remove(self, piece: Piece):
        """
        Удаляет фигуру из списка фигур и удаляет фигуру из occupied и минусует каждую атаку данной фигуры на 1
        :param piece: экземпляр класса Piece
        :return: None
        """
        if piece.pos in self.pieces:
            self.pieces.remove(piece.pos)
            self.occupied[piece.pos] = 0
            for i in self.attacked_positions(piece):
                self.occupied[i] -= 1

class Chess(Board):
    def __init__(self, size: int, output: str = 'output.txt'):
        """
        Инициализирует класс решения шахмат
        :param size: размер щахматной доски
        :param output: файл в который выведется решения
        """
        super().__init__(size)
        self.cache = set()
        self.cur_sol = [] # Текущие решения
        self.output = output
        self.const_pieces = self.pieces.copy() # Состоит из экземпляров класса Piece.

    def algorithm(self, piece: Piece=Piece(0, 0), l = 0) -> None:
        """
        Вызывается для нахождения и вывода в файл всех найденых решений
        :param piece: экземпляр класса Piece
        :param l: Число фигур которые необходимо расставить
        :return: None
        """
        if l == 0:
            self.cur_sol.sort()
            cur_sol_t = tuple(self.cur_sol)
            if cur_sol_t in self.cache:
                return None
            self.cache.update(cur_sol_t)
            answ = self.const_pieces + self.cur_sol
            for el in answ:
                self.f.write(str(el) + " ")
            self.f.write('\n')
            return None
        for i in range(piece.x, self.size):
            for j in range(piece.y if i == piece.x else 0, self.size):
                if self.occupied.get((i, j)) is None or self.occupied.get((i, j)) == 0:
                    self.cur_sol.append((i, j))
                    super().place(Piece(i, j))
                    self.algorithm(Piece(i ,j), l - 1)
                    super().remove(Piece(i, j))
                    self.cur_sol.pop()
        return None

    def first_sol(self, piece: Piece=Piece(0, 0), l = 0) -> list:
        """
        Вызывается для нахождения первого решения, ничего не выводит в файл
        :param piece: экземпляр класса Piece
        :param l: Число фигур, которые необходимо расставить
        :return: Первое найденное решение. Список с кортежами, состоящих из координат x и y
        """
        if l == 0:
            self.cur_sol.sort()
            cur_sol_t = tuple(self.cur_sol)
            if cur_sol_t in self.cache:
                return self.const_pieces + self.cur_sol
            self.cache.update(cur_sol_t)
            answ = self.const_pieces + self.cur_sol
            return answ
        for i in range(piece.x, self.size):
            for j in range(piece.y if i == piece.x else 0, self.size):
                if self.occupied.get((i, j)) is None or self.occupied.get((i, j)) == 0:
                    self.cur_sol.append((i, j))
                    super().place(Piece(i, j))
                    a = self.first_sol(Piece(i ,j), l - 1)
                    return a
        return []

    def write(self, l: int):
        """
        Обвёртка для функции алгоритма открывающая и закрывающая файл
        :param l: Число фигур, которые необходимо расставить
        :return:
        """
        self.f = open(self.output, 'w')
        self.algorithm(l=l)
        self.f.close()

    def compute_first(self, l: int) -> list[tuple[int, int]]:
        """
        Обвёртка для функции нахождения первого решения
        :param l: Числофигур, которые необходимо расставить
        :return: Первое найденное решение. Список с кортежами, состоящих из координат x и y
        """
        sol = self.first_sol(l=l)
        self.cache = set()
        self.cur_sol = []
        return sol

    def place(self, piece: Piece) -> None:
        """
        Обвёртка для родительской функции place, сохраняющей координаты (x, y) в списке const_pieces
        :param piece: Фигура. Экземпляр класса Piece
        :return: None
        """
        self.const_pieces.append(piece.pos)
        super().place(piece)

if __name__ == "__main__":
    c = Chess(10)
    c.place(Piece(0, 0))
    #print(c.write(3))
    print(c.const_pieces)
    print(c.cur_sol)
    print(c.occupied)
    c.write(1)
    #c.write(10)