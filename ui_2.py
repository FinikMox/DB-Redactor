from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QGridLayout


class Ui_InfoWindow(QDialog):
    def __init__(self):
        super(Ui_InfoWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(550, 500, 375, 200)
        self.setWindowTitle('Команды запроса')

        self.item1 = QLabel('ID(Индефикатор): Для поиска фильмов по id, достаточно использовать\n'
                            '                                знаки сравнения(<, >, =). Пример запроса: id < 10.', self)

        self.item2 = QLabel('Title(Название): Для поиска фильмов по title, нужно использовать\n'
                            '                            сочетание LIKE "(Любая буква)%(Любая буква)".\n'
                            '                             Пример запроса: title LIKE "А%"', self)

        self.item3 = QLabel('Year(Год): Для поиска фильмов по year, достаточно использовать\n'
                            '                    знаки сравнения(<, >, =). Пример запроса: year > 2000.', self)

        self.item4 = QLabel('Genre(Жанр): Для поиска фильмов по genre, достаточно использовать\n'
                            '                        знаки сравнения(<, >, =). Пример запроса: genre = 2.', self)

        self.item5 = QLabel('Duration(Длительность - Мин): Для поиска фильмов по duration, знаки\n'
                            '                                 сравнения(<, >, =). Пример запроса: duration = 60.', self)

        self.item7 = QLabel('Сохранение после изменения данных - выберите и измените нужную ячейку,\n'
                            '     затем введите в строку ID id измененного элемента'
                            ' и нажмине Сохранить.', self)

        self.item6 = QPushButton('OK', self)
        self.item6.clicked.connect(self.close)

        self.box = QGridLayout()
        self.box.addWidget(self.item1)
        self.box.addWidget(self.item2)
        self.box.addWidget(self.item3)
        self.box.addWidget(self.item4)
        self.box.addWidget(self.item5)
        self.box.addWidget(self.item7)
        self.box.addWidget(self.item6)

        self.setLayout(self.box)