from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QDialog,
    QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QRunnable
from PySide6.QtGui import QPen
from functools import partial
from chess import Chess, Piece

TILE_SIZE = 50
TILE_COLOR = Qt.white
TILE_WITH_PIECE_COLOR = Qt.green
TILE_WITH_AUTO_PIECE_COLOR = Qt.blue
TILE_ATTACKED_COLOR = Qt.red


class Worker(QRunnable):
    def __init__(self, task):
        super().__init__()
        self.task = task

    def run(self):
        self.task()

class DrawBoard(QDialog):
    def __init__(self, size, l,coords, parent):
        super().__init__(parent)
        self.parent = parent
        self.size = size
        self.coords = coords
        self.l = l
        self.chess = Chess(size)
        for i in coords:
            self.chess.place(Piece(i[0], i[1]))

        # графика
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )

        # кнопки
        self.bt_write = QPushButton("Записать в файл")
        self.bt_close = QPushButton("Выход")

        # сигналы
        self.bt_write.clicked.connect(self.write)
        self.bt_close.clicked.connect(self.close)

        # рисуем графику
        self.chess.compute_first(l)
        pen = QPen(Qt.black)

        for i in range(size):
            for j in range(size):
                rect = QGraphicsRectItem(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                rect.setPen(pen)
                rect.setBrush(TILE_COLOR)
                self.scene.addItem(rect)

        for x, y in self.chess.occupied:
            if self.chess.occupied[(x, y)] > 0:
                rect = QGraphicsRectItem(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                rect.setBrush(TILE_ATTACKED_COLOR)
                self.scene.addItem(rect)
            elif self.chess.occupied[(x, y)] == -1:
                rect = QGraphicsRectItem(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                rect.setBrush(TILE_WITH_AUTO_PIECE_COLOR)
                self.scene.addItem(rect)

        for x, y in coords:
            rect = QGraphicsRectItem(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            rect.setBrush(TILE_WITH_PIECE_COLOR)
            self.scene.addItem(rect)

        # раскладка
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.bt_write)
        layout_btns.addWidget(self.bt_close)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addLayout(layout_btns)
        self.setLayout(self.layout)

    def write(self):
        self.chess = Chess(self.size)
        for i in self.coords:
            self.chess.place(Piece(i[0], i[1]))
        task = partial(self.chess.write, self.l)
        worker = Worker(task)
        self.parent.thread_pool.start(worker)
