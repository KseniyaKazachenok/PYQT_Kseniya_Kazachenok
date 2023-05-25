"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets, QtGui

from hw_3.a_threads import WeatherHandler


class Weather(QtWidgets.QWidget):
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

        self.labelLat = QtWidgets.QLabel("Широта")
        self.doubleSpinBoxLat = QtWidgets.QDoubleSpinBox()
        self.doubleSpinBoxLat.setMaximum(90)

        self.labelLon = QtWidgets.QLabel("Долгота")
        self.doubleSpinBoxLon = QtWidgets.QDoubleSpinBox()
        self.doubleSpinBoxLon.setMaximum(180)

        self.labelTime = QtWidgets.QLabel("Время задержки")
        self.spinBoxTime = QtWidgets.QSpinBox()

        self.labelInf = QtWidgets.QLabel("Информация о погоде")
        self.plainTextEditInf = QtWidgets.QPlainTextEdit()

        self.pushButtonOn = QtWidgets.QPushButton("Запустить")
        self.pushButtonOn.setEnabled(True)
        self.pushButtonOff = QtWidgets.QPushButton("Остановить")
        self.pushButtonOff.setEnabled(False)

        layoutLat = QtWidgets.QHBoxLayout()
        layoutLat.addWidget(self.labelLat)
        layoutLat.addWidget(self.doubleSpinBoxLat)

        layoutLon = QtWidgets.QHBoxLayout()
        layoutLon.addWidget(self.labelLon)
        layoutLon.addWidget(self.doubleSpinBoxLon)

        layoutTime = QtWidgets.QHBoxLayout()
        layoutTime.addWidget(self.labelTime)
        layoutTime.addWidget(self.spinBoxTime)

        layoutInf = QtWidgets.QHBoxLayout()
        layoutInf.addWidget(self.labelInf)
        layoutInf.addWidget(self.plainTextEditInf)

        layoutButton = QtWidgets.QHBoxLayout()
        layoutButton.addWidget(self.pushButtonOn)
        layoutButton.addWidget(self.pushButtonOff)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layoutLat)
        layout.addLayout(layoutLon)
        layout.addLayout(layoutTime)
        layout.addLayout(layoutInf)
        layout.addLayout(layoutButton)

        self.setLayout(layout)

    def initThreads(self) -> None:
        """
        Инициализация потоков

        :return: None
        """

        self.thread = WeatherHandler(0, 0)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        self.doubleSpinBoxLat.textChanged.connect(self.getLatLon)
        self.doubleSpinBoxLon.textChanged.connect(self.getLatLon)
        self.spinBoxTime.textChanged.connect(self.getDelay)
        self.thread.data_responsed.connect(self.getWeatherInfo)
        self.pushButtonOn.clicked.connect(self.runProcess)
        self.pushButtonOff.clicked.connect(self.endProcess)

    def getLatLon(self):
        self.thread.setApiUrl(self.doubleSpinBoxLat.value(), self.doubleSpinBoxLon.value())

    def getDelay(self) -> None:
        self.thread.setDelay(self.spinBoxTime.value())

    def getWeatherInfo(self, data_responsed) -> None:
        """
        Приём данных из потока и отображение в окне приложения

        :param data_responsed: сигнал потока
        :return: None
        """

        if not self.pushButtonOn.isEnabled():
            self.plainTextEditInf.setPlainText(str(data_responsed))

    def runProcess(self) -> None:
        """
        Запуск потока

        :return: None
        """

        self.pushButtonOn.setEnabled(False)
        self.pushButtonOff.setEnabled(True)
        self.thread.setStatus(True)
        self.thread.start()

    def endProcess(self) -> None:
        """
        Остановка потока

        :return: None
        """

        self.pushButtonOff.setEnabled(False)
        self.pushButtonOn.setEnabled(True)
        self.thread.setStatus(None)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    weather = Weather()
    weather.show()

    app.exec()