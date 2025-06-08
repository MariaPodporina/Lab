from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
)
from PySide6.QtCore import QSize, QThreadPool
from draw_board import DrawBoard
from input_coord import InputCoord
from chess import Chess

MAIN_WINDOW_SIZE = QSize(400, 150)

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Инициализатор класса основного окна
        :return: None
        """
        super().__init__()

        self.setWindowTitle("Шахматы")
        self.setFixedSize(MAIN_WINDOW_SIZE)
        self.coord : list = []

        # Поля ввода
        self.inputSize = QLineEdit()
        self.inputSize.setPlaceholderText("Размер доски (N)")

        self.inputL = QLineEdit()
        self.inputL.setPlaceholderText("Число фигур(L)")

        self.inputConst = QLineEdit()
        self.inputConst.setPlaceholderText("Число фигур уже поставленных(K)")

        # Кропки
        self.bt_coord = QPushButton("Создать Доску")
        self.bt_coord.setDisabled(True)

        self.bt_draw_board = QPushButton("Нарисовать Доску")
        self.bt_draw_board.setDisabled(True)

        self.bt_exit = QPushButton("Выход")

        # Сигналы
        self.inputSize.textChanged.connect(self.validator)
        self.inputL.textChanged.connect(self.validator)
        self.inputConst.textChanged.connect(self.validator)

        self.bt_coord.clicked.connect(self.bt_coord_clicked)
        self.bt_draw_board.clicked.connect(self.draw_board)
        self.bt_exit.clicked.connect(self.close)

        # Раскладка Ввода
        layout_inputs = QVBoxLayout()

        layout_inputs.addWidget(self.inputSize)
        layout_inputs.addWidget(self.inputL)
        layout_inputs.addWidget(self.inputConst)

        # Раскладка Кнопок
        layout_btns = QHBoxLayout()

        layout_btns.addWidget(self.bt_coord)
        layout_btns.addWidget(self.bt_draw_board)
        layout_btns.addWidget(self.bt_exit)

        layout = QVBoxLayout()
        layout.addLayout(layout_inputs)
        layout.addLayout(layout_btns)

        wdg = QWidget()
        wdg.setLayout(layout)
        self.setCentralWidget(wdg)

    def validator(self):
        """
        Активирует или отключает кнопки после того как пользователь что то ввел
        :return: None
        """
        is_size_correct = self.inputSize.text().isdigit()
        is_L_correct = self.inputL.text().isdigit()
        is_const_correct = self.inputConst.text().isdigit()

        if is_size_correct and is_L_correct and is_const_correct:
            if int(self.inputL.text()) > 0 and int(self.inputSize.text()):
                size = int(self.inputSize.text())
                const = int(self.inputConst.text())
                self.bt_coord.setEnabled(const > 0)
                self.bt_draw_board.setEnabled(const == 0 or len(self.coord) == const)
        else:
            self.bt_coord.setEnabled(False)
            self.bt_draw_board.setEnabled(False)

    def bt_coord_clicked(self):
        """
        Вызывает модальное окно для ввода координат фигур
        :return: None
        """
        const = int(self.inputConst.text())
        size = int(self.inputSize.text())

        dlg = InputCoord(const, size, self)

        if dlg.exec() == QDialog.Accepted:
            self.coord = dlg.coords
        self.validator()

    def draw_board(self):
        """
        Вызывает модальное окно с шахматной доской и возможностью записать решения в файл. Если решений не найдено,
        то создает окно с надписью, что решений нет
        :return: None
        """
        l = int(self.inputL.text())
        size = int(self.inputSize.text())
        chess = Chess(size)
        sol = chess.compute_first(l)

        if not sol:
            dlg = QDialog()
            label = QLabel("Нет Решений!")
            bt = QPushButton("Ок")
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(bt)
            dlg.setLayout(layout)
            dlg.exec()
        else:
            dlg = DrawBoard(size, l, self.coord, self)
            dlg.exec()

if __name__ == '__main__':
    app = QApplication()
    wdg = MainWindow()
    wdg.show()
    app.exec()