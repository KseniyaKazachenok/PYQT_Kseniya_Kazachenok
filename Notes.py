"""
Задача

Реализовать приложение для работы с заметками

Обязательные функции в приложении:
* Добавление, изменение, удаление заметок
* Сохранение времени добавления заметки и отслеживание времени до дэдлайна.
* Реализация хранения заметок остаётся на ваш выбор (БД, json и т.д.).
"""
import json
import time
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()
        self.tabWidget.installEventFilter(self)
        self.tabCounter = 0

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        self.bushButtonCreate = QtWidgets.QPushButton("Создать заметку")
        self.bushButtonCreate.setAutoFillBackground(True)
        self.bushButtonCreate.setStyleSheet('QPushButton {background-color: #d5bfa8; color: black;}')
        self.bushButtonCreate.setFont('Segoe Script')

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.installEventFilter(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.bushButtonCreate)
        layout.addWidget(self.tabWidget)

        self.setLayout(layout)

    # def eventFilter(self, watched: QtWidgets.QWidget, event: QtCore.QEvent) -> bool:
    #     """
    #     Переименование вкладки
    #
    #     :return: Bool
    #     """
    #     if watched == self.tabWidget.currentWidget() and event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
    #         self.tabWidget.currentWidget().setObjectName("text")
    #     return super(Window, self).eventFilter(watched, event)
    # не работает

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.bushButtonCreate.clicked.connect(self.addTab)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

    def addTab(self):
        widget = NoteWidget()
        widgetName = f"Заметка {self.tabCounter}"
        self.tabWidget.addTab(widget, widgetName)
        index = self.tabWidget.indexOf(widget)
        self.tabWidget.setCurrentIndex(index)
        self.tabCounter += 1

    def close_tab(self, index):
        answer = QtWidgets.QMessageBox.question(
            self, "Удалить заметку", "Вы уверены, что хотите удалить заметку?",
        )

        if answer == QtWidgets.QMessageBox.Yes:
            self.tabWidget.widget(index).deleteLater()
            self.tabWidget.removeTab(index)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна

        :param event: QtGui.QCloseEvent
        :return: None
        """
        if self.tabWidget.count() > 0:
            for el in range(self.tabWidget.count()):
                d = dict()
                d["Названия вкладки"] = self.tabWidget.tabText(el)
                d["Текст"] = self.tabWidget.widget(el).plainTextEdit.toPlainText()
                d["Дата создания"] = self.tabWidget.widget(el).dateTimeEditDateDone.text()
                d["Дата дедлайна"] = self.tabWidget.widget(el).dateTimeEditDeadline.text()
                self.saveNote(d)

    @staticmethod
    def saveNote(data: dict):
        with open(f"{data['Названия вкладки']}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class NoteWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initTimers()
        self.initSignals()


    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        self.labelDateDone = QtWidgets.QLabel("Создано")
        self.labelDateDone.setFont('Segoe Script')
        self.dateTimeEditDateDone = QtWidgets.QDateTimeEdit()
        self.dateTimeEditDateDone.setFont('Segoe Script')
        self.dateTimeEditDateDone.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateTimeEditDateDone.setEnabled(False)
        self.labelDeadline = QtWidgets.QLabel("Дэдлайн")
        self.labelDeadline.setFont('Segoe Script')
        self.dateTimeEditDeadline = QtWidgets.QDateTimeEdit()
        self.dateTimeEditDeadline.setFont('Segoe Script')
        self.dateTimeEditDeadline.setMinimumDate(QtCore.QDate(2023, 5, 27))
        self.dateTimeEditDeadline.setCalendarPopup(True)
        self.labelTimetoDeadline = QtWidgets.QLabel("До дэдлайна осталось:")
        self.labelTimetoDeadline.setFont('Segoe Script')
        self.labelDelta = QtWidgets.QLabel()
        self.labelDelta.setFont('Segoe Script')
        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setPlaceholderText("Введите текст заметки")
        self.plainTextEdit.setMinimumSize(300, 60)
        self.plainTextEdit.setStyleSheet("QWidget {background-color: #d5bfa8}")
        self.plainTextEdit.setFont("Brush Script MT")

        layoutWidgets = QtWidgets.QVBoxLayout()
        layoutWidgets.addWidget(self.labelDateDone)
        layoutWidgets.addWidget(self.dateTimeEditDateDone)
        layoutWidgets.addWidget(self.labelDeadline)
        layoutWidgets.addWidget(self.dateTimeEditDeadline)
        layoutWidgets.addWidget(self.labelTimetoDeadline)
        layoutWidgets.addWidget(self.labelDelta)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.plainTextEdit)
        layout.addLayout(layoutWidgets)
        self.setLayout(layout)

    def initTimers(self) -> None:
        """

        :return:
        """

        self.timer = QtCore.QTimer()
        self.timer.setInterval(2000)
        self.timer.start()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.timer.timeout.connect(self.setDeadline)
        self.dateTimeEditDeadline.dateTimeChanged.connect(self.setDeadline)

    def setDeadline(self):
        time_1 = QtCore.QDateTime.currentDateTime()
        time_2 = self.dateTimeEditDeadline.dateTime()
        dtsec = time_1.msecsTo(time_2)
        days = int(dtsec / 86400000)
        hours = int((dtsec - 86400000 * days) / 3600000)
        minutes = int((dtsec - 86400000 * days - 3600000 * hours) / 60000)
        self.labelDelta.setText(f"{days} дней {hours} часов {minutes} минут")


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()