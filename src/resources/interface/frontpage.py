import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QStyleFactory, QLabel, QVBoxLayout, QSizePolicy
from resources.SpotifyManager import SpotifyManager
from os import path


def is_logged_in():
    return path.exists('.cache-user')

class FrontPage(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def addpages(self, pages):
        self.pages = pages

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('fusion'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Welcome to Spotify Manager!')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('font: 20pt Comic Sans MS')

        self.loginbutton = QPushButton('Login')
        self.loginbutton.setDefault(True)
        self.loginbutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.loginbutton.clicked.connect(self.handle_login_button)
        
        self.setWindowTitle('Welcome')
        self.resize(400, 300)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.loginbutton, alignment=Qt.AlignHCenter|Qt.AlignTop)


    def handle_login_button(self):
        sp = SpotifyManager('user')
        if is_logged_in():
            self.pages.frontpage.hide()
            self.pages.mainpage.show()
        

def main():
    app = QApplication(sys.argv)
    ex = FrontPage()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()