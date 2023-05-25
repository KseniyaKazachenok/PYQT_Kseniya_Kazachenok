"""
Реализация программы взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtGui, QtCore

from hw_2.d_eventfilter_settings.d_eventfilter_settings import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings("Event_Filter_Settings")
        # print(self.settings.fileName())

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(['oct', 'hex', 'bin', 'dec'])
        self.loadData()
        self.initSignals()
        self.ui.dial.installEventFilter(self)


    def loadData(self) -> None:
        """
        Загрузка данных в Ui

        :return: None
        """
        modes = {
            "oct": QtWidgets.QLCDNumber.Mode.Oct,
            "hex": QtWidgets.QLCDNumber.Mode.Hex,
            "bin": QtWidgets.QLCDNumber.Mode.Bin,
            "dec": QtWidgets.QLCDNumber.Mode.Dec
        }

        self.ui.comboBox.setCurrentText(self.settings.value("Mode", ""))
        self.ui.lcdNumber.display(self.settings.value("LCDNumber", ""))
        self.ui.lcdNumber.setMode(modes[self.settings.value("Mode", "dec")])

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Установка значений для elf.ui.dial кнопками клавиатуры (+ и -)

        :return: Bool
        """
        if watched == self.ui.dial and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Plus:
                self.ui.dial.setValue(self.ui.dial.value() + 1)
                print(self.ui.dial.value())
            if event.key() == QtCore.Qt.Key.Key_Minus:
                self.ui.dial.setValue(self.ui.dial.value() - 1)
                print(self.ui.dial.value())
        return super(Window, self).eventFilter(watched, event)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.ui.dial.valueChanged.connect(self.changeDial)
        self.ui.horizontalSlider.valueChanged.connect(self.changeHorizontalSlider)
        self.ui.comboBox.currentTextChanged.connect(self.changeComboBox)

    def valueType(self, num):
        """
        Выбор формата данных в зависимости от выбранного в comboBox параметра
        :param num:
        :return:
        """
        if self.ui.comboBox.currentText() == 'oct':
            return oct(num)
        if self.ui.comboBox.currentText() == 'hex':
            return hex(num)
        if self.ui.comboBox.currentText() == 'bin':
            return bin(num)
        if self.ui.comboBox.currentText() == 'dec':
            return num

    def changeDial(self) -> None:
        """
        Обработка сигнала valueChanged для виджета self.ui.dial
        :return: None
        """
        self.ui.lcdNumber.display(self.valueType(self.ui.dial.value()))
        self.ui.horizontalSlider.setValue(self.ui.dial.value())

    def changeHorizontalSlider(self) -> None:
        """
        Обработка сигнала valueChanged для виджета self.ui.horizontalSlider
        :return: None
        """
        self.ui.lcdNumber.display(self.valueType(self.ui.horizontalSlider.value()))
        self.ui.dial.setValue(self.ui.horizontalSlider.value())

    def changeComboBox(self) -> None:
        """
        Обработка сигнала currentTextChanged для виджета self.ui.comboBox
        :return: None
        """
        self.ui.lcdNumber.display(self.valueType(self.ui.dial.value()))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Событие закрытия окна

        :param event: QtGui.QCloseEvent
        :return: None
        """
        self.settings.setValue("Mode", self.ui.comboBox.currentText())
        self.settings.setValue("LCDNumber", self.ui.dial.value())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
