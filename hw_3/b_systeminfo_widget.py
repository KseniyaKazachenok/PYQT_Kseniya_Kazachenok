"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtGui

from hw_3.a_threads import SystemInfo


class SInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()
        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация Ui

        :return: None
        """

        self.labelTime = QtWidgets.QLabel("Время задержки")
        self.spinBox = QtWidgets.QSpinBox()
        self.labelCPU = QtWidgets.QLabel("Информация о загрузке CPU")
        self.plainTextEditCPU = QtWidgets.QPlainTextEdit()
        self.labelRAM = QtWidgets.QLabel("Информация о загрузке RAM")
        self.plainTextEditRAM = QtWidgets.QPlainTextEdit()

        layoutTime = QtWidgets.QHBoxLayout()
        layoutTime.addWidget(self.labelTime)
        layoutTime.addWidget(self.spinBox)
        layoutCPU = QtWidgets.QHBoxLayout()
        layoutCPU.addWidget(self.labelCPU)
        layoutCPU.addWidget(self.plainTextEditCPU)
        layoutRAM = QtWidgets.QHBoxLayout()
        layoutRAM.addWidget(self.labelRAM)
        layoutRAM.addWidget(self.plainTextEditRAM)
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layoutTime)
        layout.addLayout(layoutCPU)
        layout.addLayout(layoutRAM)

        self.setLayout(layout)

    def initThreads(self) -> None:
        """
        Инициализация потоков

        :return: None
        """

        self.thread = SystemInfo()
        self.thread.start()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.spinBox.textChanged.connect(self.getDelay)
        self.thread.systemInfoReceived.connect(self.getSystemInfo)

    def getDelay(self) -> None:
        self.thread.delay = self.spinBox.value()

    def getSystemInfo(self, systemInfoReceived) -> None:
        """
        Приём данных из потока и отображение в окне приложения

        :param systemInfoReceived: сигнал потока
        :return: None
        """

        self.plainTextEditCPU.setPlainText(str(systemInfoReceived[0]))
        self.plainTextEditRAM.setPlainText(str(systemInfoReceived[1]))


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    sInfo = SInfo()
    sInfo.show()

    app.exec()
