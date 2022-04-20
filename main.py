import math
import random
import sys  # sys нужен для передачи argv в QApplication
import numbers
import numpy as np
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QMessageBox
from PyQt5.QtCore import QCoreApplication
import design  # Это наш конвертированный файл дизайна
import pyqtgraph as pg

class Fluctuations(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        #self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton.clicked.connect(self.draw)
        self.Graph = pg.PlotWidget()
        self.Graph.setBackground('w')
        self.pushButton_3.clicked.connect(self.check)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.pushButton_2.clicked.connect(self.timer.stop)
        self.i = 0
        self.t = []
        self.phi = []

    def draw(self):
        i = 0
        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)
        pen = pg.mkPen(color=(255, 0, 0))
        self.timer.start()
        self.plot_graph = self.Graph.plot(self.t, self.phi, pen=pen)
        plotit = scene.addWidget(self.Graph)

    def check(self):
        a = [self.textEdit.toPlainText(), self.textEdit_2.toPlainText(), self.textEdit_3.toPlainText(), self.textEdit_4.toPlainText(), self.textEdit_5.toPlainText(), self.textEdit_6.toPlainText(), self.textEdit_7.toPlainText()]
        flag = 1
        for i in range(0, 6, 1):
            if a[i] == '' or type(a[i]) == 'str':
                flag = 0

        if flag == 0:
            QMessageBox.critical(self, "Ошибка ", "Вводимые переменные должны быть числами", QMessageBox.Ok)
            self.textEdit.clear()
            self.textEdit_2.clear()
            self.textEdit_3.clear()
            self.textEdit_4.clear()
            self.textEdit_5.clear()
            self.textEdit_6.clear()
            self.textEdit_7.clear()
        else:
            self.phi0 = float(self.textEdit.toPlainText())
            self.speed0 = float(self.textEdit_2.toPlainText())
            self.f = float(self.textEdit_3.toPlainText())
            self.wf = float(self.textEdit_4.toPlainText())
            self.le = float(self.textEdit_5.toPlainText())
            self.m = float(self.textEdit_6.toPlainText())
            self.bet = float(self.textEdit_7.toPlainText())

    def update(self):
        h = 3*self.bet/(2*self.m*self.le)
        k2 = 3*9.8/(2*self.le)
        fo = 3*self.f/(self.m*self.le)
        alfa = math.atan(2*h*self.wf/(k2-self.wf*self.wf))
        ko = math.sqrt(k2 - h * h)
        A = fo/math.sqrt((k2-self.wf*self.wf)*(k2-self.wf*self.wf)+4*self.bet*self.bet*self.wf*self.wf)
        c1 = self.phi0 + A * math.sin(alfa)
        c2 = (self.speed0 + h*c1 -A*self.wf*math.cos(alfa))*(1/ko)
        self.t.append(self.i*100)
        phi1 = math.exp(-h*self.i)*(c2*math.sin(ko*self.i)+c1*math.cos(ko*self.i))+A*math.sin(self.wf*self.i-alfa)
        self.phi.append(phi1)
        self.plot_graph.setData(self.t, self.phi)
        self.i = self.i + 0.1



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Fluctuations()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()