from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QDialog,
    QSizePolicy,
    QLabel,
)
from PySide6.QtCore import Qt, QRunnable, QThreadPool
from PySide6.QtGui import QPen
from functools import partial
from chess import Chess, Piece

# Константы для отображения доски с фигурами
TILE_SIZE = 50
TILE_COLOR = Qt.white
TILE_WITH_PIECE_COLOR = Qt.green
TILE_WITH_AUTO_PIECE_COLOR = Qt.blue
TILE_ATTACKED_COLOR = Qt.red

class Worker(QRunnable):
    def __init__(self, task, parent=None):
        """
        Инициализирует рабочего метод которого будет запущен в другом потоке
        :param task: Функция, которая будет запущена в другом потоке
        :param parent: Родительский класс
        """
        super().__init__()
        self.task = task
        self.parent = parent

    def run(self):
        """
        Вызывается в другом потоке. Записывает результаты решения шахмат в файл и выводит сообщение об их успешной записи
        :return: None
        """
        self.task()
        dlg = QDialog(self.parent)
        dlg.setFixedSize(400, 100)
        text = QLabel("Решения были успешно записаны в файл!")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bt = QPushButton("Ок")
        bt.clicked.connect(dlg.close)
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addWidget(bt)
        dlg.setLayout(layout)
        dlg.exec()

class DrawBoard(QDialog):
    def __init__(self, size, l, coords, parent):
        """
        Инициализирует класс окна вывода шахматной доски
        :param size: Размер шахматной доски
        :param l: Количество фигур, необходимых расставить
        :param coords: Список координат фигур уже поставленных
        :param parent: Родительский класс
        """
        super().__init__(parent)
        print(coords)
        self.parent = parent
        self.size: int = size
        self.coords: list[tuple[int, int]] = coords
        self.l: int = l
        self.chess: Chess = Chess(size)
        self.thread_pool = QThreadPool()
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
        """
        Вызывается для нахождения решений шахмат и ввод их в файл
        :return: None
        """
        self.chess = Chess(self.size)
        for i in self.coords:
            self.chess.place(Piece(i[0], i[1]))
        task = partial(self.chess.write, self.l)
        worker = Worker(task, self)
        self.thread_pool.start(worker)
