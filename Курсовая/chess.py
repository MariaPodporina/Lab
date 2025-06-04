class Piece:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.moves = (
            (-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)
        )

class Board:
    def __init__(self, size: int, occupied: dict = None):
        if occupied is None:
            self.occupied = dict()
        else:
            self.occupied = occupied
        self.size = size
        self.pieces = []
        self.board = [[0 for i in range(size)] for j in range(size)]

    def attacked_positions(self, piece: Piece):
        attacked_tiles = []
        for i in piece.moves:
            if piece.x + i[0] < 0 or piece.y + i[1] < 0 or piece.x + i[0] > self.size - 1 or piece.y + i[1] > self.size - 1:
                continue
            else:
                attacked_tiles.append((piece.x + i[0], piece.y + i[1]))
        return attacked_tiles

    def is_save(self, piece: Piece):
        if piece.pos in self.occupied or piece.x > self.size or piece.y > self.size:
            return False
        return True

    def place(self, piece: Piece):
        if self.is_save(piece):
            self.pieces.append(piece.pos)
            self.occupied[piece.pos] = -1
            for i in self.attacked_positions(piece):
                if self.occupied.get(i) is None:
                    self.occupied[i] = 1
                else:
                    self.occupied[i] += 1


    def remove(self, piece: Piece):
        if piece.pos in self.pieces:
            self.pieces.remove(piece.pos)
            self.occupied[piece.pos] = 0
            for i in self.attacked_positions(piece):
                self.occupied[i] -= 1

class Chess(Board):
    def __init__(self, size: int, output: str = 'output.txt'):
        super().__init__(size)
        self.cache = set()
        self.cur_sol = []
        self.output = output
        self.const_pieces = self.pieces.copy()

    def algorithm(self, piece: Piece=Piece(0, 0), l = 0) -> None:
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
                    self.place(Piece(i, j), False)
                    self.algorithm(Piece(i ,j), l - 1)
                    self.remove(Piece(i, j))
                    self.cur_sol.pop()
        return None

    def first_sol(self, piece: Piece=Piece(0, 0), l = 0) -> list:
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
                    self.place(Piece(i, j), False)
                    a = self.first_sol(Piece(i ,j), l - 1)
                    return a
        return []

    def write(self, l: int):
        self.f = open(self.output, 'w')
        self.algorithm(l=l)
        self.f.close()

    def compute_first(self, l: int):
        #print(self.const_pieces)
        sol = self.first_sol(l=l)
        self.cache = set()
        self.cur_sol = []
        #self.remove(Piece(sol[-1][0], sol[-1][1]))
        return sol

    def place(self, piece: Piece, save=True):
        if save:
            self.const_pieces.append(piece.pos)
        super().place(piece)

if __name__ == "__main__":
    c = Chess(10)
    c.place(Piece(0, 0))
    print(c.compute_first(1000))
    print(c.const_pieces)
    print(c.cur_sol)
    print(c.occupied)
    c.write(1)
    #c.write(10)