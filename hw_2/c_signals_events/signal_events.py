"""
Реализация программы проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""
import time

from PySide6 import QtWidgets, QtCore

from hw_2.c_signals_events.c_signals_events import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.ui.pushButtonLT.clicked.connect(self.moveWindowLT)
        self.ui.pushButtonRT.clicked.connect(self.moveWindowRT)
        self.ui.pushButtonCenter.clicked.connect(self.moveWindowCenter)
        self.ui.pushButtonLB.clicked.connect(self.moveWindowLB)
        self.ui.pushButtonRB.clicked.connect(self.moveWindowRB)
        self.ui.pushButtonMoveCoords.clicked.connect(self.moveWindow)
        self.ui.pushButtonGetData.clicked.connect(self.getWindowData)

    def moveWindowLT(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLT

        :return: None
        """
        window.move(self.pos().x() - 1, self.pos().y() - 1)

    def moveWindowRT(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRT

        :return: None
        """
        window.move(self.pos().x() + 1, self.pos().y() - 1)

    def moveWindowCenter(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonCenter

        :return: None
        """
        window.move(int(self.rect().center().x()), int(self.rect().center().y()))

    def moveWindowLB(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLB

        :return: None
        """
        window.move(self.pos().x() - 1, self.pos().y() + 1)

    def moveWindowRB(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRB

        :return: None
        """
        window.move(self.pos().x() + 1, self.pos().y() + 1)

    def moveWindow(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonMoveCoords

        :return: None
        """
        window.move(int(self.ui.spinBoxX.value()), int(self.ui.spinBoxY.value()))

    def getWindowData(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonMoveCoords

        :return: None
        """
        self.ui.plainTextEdit.setPlainText(
            str(QtWidgets.QApplication.screens()) + "\n" +
            str(QtWidgets.QApplication.primaryScreen()) + "\n" +
            str(self.screen().geometry()) + "\n" +
            str(self.screen()) + "\n" +
            str(self.size()) + "\n" +
            str(self.minimumSize()) + "\n" +
            str(self.pos()) + "\n" +
            str(self.rect().center()) + "\n" +
            str(self.isHidden()) + "\n" +
            str(self.isActiveWindow()) + "\n" +
            str(self.isFullScreen()) + "\n" +
            str(self.isVisible()) + "\n" +
            str(time.ctime())
        )

    def event(self, event: QtCore.QEvent) -> bool:
        """
        Событие отслеживания состояния окна

        :return: None
        """

        if event.type() == QtCore.QEvent.Type.Move:
            print(event.oldPos(), ">>>", event.pos(), ">>>", time.ctime())

        if event.type() == QtCore.QEvent.Type.Resize:
            print(event.size(), ">>>", time.ctime())

        return super(Window, self).event(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
