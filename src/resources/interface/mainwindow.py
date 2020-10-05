from resources.interface.frontpage import FrontPage
from resources.interface.mainpage import MainPage
from resources.interface.pages import Pages
from os import path
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QStyleFactory, QLabel, QHBoxLayout, QSizePolicy


def is_logged_in():
    return path.exists('.cache-user')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.pages = Pages()
        self.addpages()
        self.initUI()


    def addpages(self):
        self.pages.frontpage.addpages(self.pages)
        self.pages.mainpage.addpages(self.pages)

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('fusion'))
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)


        self.setWindowTitle('Welcome')
        self.resize(400, 300)
        self.layout.addWidget(self.pages.frontpage)
        self.layout.addWidget(self.pages.mainpage)
        if is_logged_in():
            self.pages.frontpage.hide()
            self.pages.mainpage.show()
        else:
            self.pages.mainpage.hide()
            self.pages.frontpage.show()
        self.show()






def main():
    #app = QApplication(sys.argv)
    ex = MainWindow()
    #ex.show()
    #sys.exit(app.exec_())


if __name__ == '__main__':
    main()


