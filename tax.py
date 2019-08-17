import sys, cv2, datetime
import numpy as np
from decimal import Decimal
from threading import Thread


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from PyQt5 import QtBluetooth as QtBt


qtcreator_file  = "mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)




class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.calc_tax_button.clicked.connect(self.toggle_camera)
        self.bluetoothButton.clicked.connect(self.bluetoothTest)

    def bluetoothTest(self):
        self.agent = QtBt.QBluetoothDeviceDiscoveryAgent(self)
        self.agent.deviceDiscovered.connect(self.foo)
        self.agent.finished.connect(self.foo)
        self.agent.error.connect(self.foo)
        self.agent.setLowEnergyDiscoveryTimeout(1000)

        timer = QTimer(self.agent)
        timer.start(500)
        timer.timeout.connect(self.display_status)

    def foo(self, *args, **kwargs):
        print('fooo', args, kwargs)

    def display_status(self):
        print(self.agent.isActive(), self.agent.discoveredDevices())


    def toggle_camera(self):
        if(self.calc_tax_button.text()=='Start Camera'):
            self.calc_tax_button.setText('Stop Camera')
            self.start_camera()
        else:
            self.calc_tax_button.setText('Start Camera')
            self.stop_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_frame)
        self.timer.start(34)

    def display_frame(self):
        (grabbed, frame) = self.cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(rgb_frame.tobytes(), rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
        self.camPreviewLabel.setPixmap(QPixmap.fromImage(image))

    def stop_camera(self):
        self.timer.stop()
        self.cap.release()
        self.camPreviewLabel.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()

    #timer = QTimer(window)
    #timer.timeout.connect(window.calculateTax)
    #timer.start(10)
    #window.calculateTax( True)
    sys.exit(app.exec_())
