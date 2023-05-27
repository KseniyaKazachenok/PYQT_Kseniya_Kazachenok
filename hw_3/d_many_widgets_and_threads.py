"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets

from hw_3.b_systeminfo_widget import SInfo
from hw_3.c_weatherapi_widget import Weather


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.si = SInfo()
        self.we = Weather()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.addTab(SInfo(), "Info")
        self.tabWidget.addTab(Weather(), "Weather")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tabWidget)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()