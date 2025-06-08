from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QLabel,
)
from chess import Board, Piece

class InputCoord(QDialog):
    def __init__(self, const: int, size: int, parent):
        """
        Инициализатор окна ввода координат
        :param const: Количество фигур, которые необходимо расставить
        :param size: Размер шахматной доски
        :param parent: Родительский ласс, который вызвал данный класс
        """
        super().__init__(parent)
        self.setWindowTitle("Ввод Координат")
        self.setModal(True)

        self.coords: list[tuple[int,int]] = []
        self.size: int = size
        self.inputs: list[str] = []
        layout = QVBoxLayout()

        for i in range(const):
            row = QHBoxLayout()

            label = QLabel(f"Фигура {i + 1}")

            inpt = QLineEdit()
            inpt.setPlaceholderText("x y")
            inpt.textEdited.connect(self.validator)

            self.inputs.append(inpt)

            row.addWidget(label)
            row.addWidget(inpt)

            layout.addLayout(row)

        # кнопки
        self.bt_accept = QPushButton("Ok")
        self.bt_accept.setEnabled(False)

        bt_cancel = QPushButton("Отмена")

        # сигналы
        self.bt_accept.clicked.connect(self.accept)
        bt_cancel.clicked.connect(self.reject)

        # раскладка
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.bt_accept)
        layout_btns.addWidget(bt_cancel)

        layout.addLayout(layout_btns)
        self.setLayout(layout)

    def validator(self):
        """
        Валидатор вводимых координат пользователем. Активирует кнопку подтверждения
        :return: None
        """
        is_valid = True
        board = Board(self.size)

        for line in self.inputs:
            text = line.text().strip()
            try:
                x, y = map(int, text.split())
                if board.is_save(Piece(x, y)):
                   board.place(Piece(x, y))
                else:
                    is_valid = False
            except:
                is_valid = False
        self.coords = board.pieces
        self.bt_accept.setEnabled(is_valid)
