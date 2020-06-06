import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from ui_3 import Ui_MainWindow
from ui_2 import Ui_InfoWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.delete_elem)
        self.pushButton_4.clicked.connect(self.add_elem)
        self.pushButton_5.clicked.connect(self.commands)
        self.modified = {}
        self.truer = 1
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        if self.textEdit.toPlainText() == '':
            self.no_correct_query(0)
        elif 'id' not in str(self.textEdit.toPlainText()) and \
                'title' not in str(self.textEdit.toPlainText()) and\
                'genre' not in str(self.textEdit.toPlainText()) and \
                'duration' not in str(self.textEdit.toPlainText()) and\
                'year' not in str(self.textEdit.toPlainText()):
            self.no_correct_query(0)
        else:
            result = cur.execute("SELECT * FROM Films WHERE " + self.textEdit.toPlainText()).fetchall()
            if not result:
                self.no_correct_query(1)
            else:
                self.tableWidget.setRowCount(len(result))
                self.tableWidget.setColumnCount(len(result[0]))
                self.titles = [description[0] for description in cur.description]
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
                self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.spinBox.text() == '0':
            self.warn()
        else:
            if len(self.modified) > 1:
                self.one_more()
            elif self.modified:
                cur = self.con.cursor()
                que = "UPDATE films SET\n"
                for key in self.modified.keys():
                    que += "{}='{}'\n".format(key, self.modified.get(key))
                que += "WHERE id = ?"
                cur.execute(que, (self.spinBox.text(),))
                self.con.commit()
                self.truer = True
                self.spinBox.setValue(0)
                valid = QMessageBox.question(self, '',
                                             "Успешно сохранено!",
                                             QMessageBox.Ok)
                if valid == QMessageBox.Ok:
                    self.modified = {}

    def delete_elem(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if not rows and not ids:
            valid = QMessageBox.question(self, '',
                                         "Элементы не выбраны!",
                                         QMessageBox.Ok)
            if valid == QMessageBox.Ok:
                pass
        else:
            valid = QMessageBox.question(self, '',
                                         "Действительно удалить элементы с id " +
                                         ",".join(ids), QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur = self.con.cursor()
                cur.execute("DELETE from films WHERE ID in (" +
                            ", ".join('?' * len(ids)) + ")", ids)
                self.con.commit()

    def no_correct_query(self, n):
        if n == 0:
            valid = QMessageBox.question(self, '',
                                         "Некорректный запрос",
                                         QMessageBox.Ok)
            if valid == QMessageBox.Ok:
                pass
        else:
            valid = QMessageBox.question(self, '',
                                         "Элемент не найден",
                                         QMessageBox.Ok)
            if valid == QMessageBox.Ok:
                pass

    def add_elem(self):
        if self.spinBox.text() == '0':
            self.warn()
        else:
            cur = self.con.cursor()
            result = cur.execute("Select * from films WHERE id=?",
                                 (self.spinBox.text(),)).fetchall()
            if not result:
                que = "INSERT INTO films(id, title, year, genre, duration)\n"
                que += "VALUES(?, '', '', '', '')"
                cur.execute(que, (self.spinBox.text(),))
                self.con.commit()
                self.spinBox.setValue(0)
                valid = QMessageBox.question(self, '',
                                             "Успешно добавлен!",
                                             QMessageBox.Ok)
                if valid == QMessageBox.Ok:
                    pass
            else:
                valid = QMessageBox.question(self, '',
                                             "Элемент уже существует!",
                                             QMessageBox.Ok)
                if valid == QMessageBox.Ok:
                    pass
                self.spinBox.setValue(0)

    def commands(self):
        self.infoWindow = Ui_InfoWindow()
        self.infoWindow.show()

    def warn(self):
        valid = QMessageBox.question(self, '',
                                     "ID не выбран",
                                     QMessageBox.Ok)
        if valid == QMessageBox.Ok:
            pass

    def one_more(self):
        valid = QMessageBox.question(self, '',
                                     "Нельзя менять больше\n"
                                     "одного элемента одновременно!",
                                     QMessageBox.Ok)
        if valid == QMessageBox.Ok:
            self.spinBox.setValue(0)
            self.modified = {}


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
