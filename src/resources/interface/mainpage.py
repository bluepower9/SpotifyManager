import sys, os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QMessageBox, QPushButton, QRadioButton, QSizePolicy, QStyleFactory, QVBoxLayout, QWidget
from resources.createplaylist import create_playlist
from resources.SpotifyManager import SpotifyManager

class MainPage(QWidget):

    def __init__(self):
        super().__init__()

        
        self.checkboxes = {}
        self.initUI()


    def show(self):
        self.sp = SpotifyManager('user')
        self.sp.setup()
        name = self.sp.get_username()
        self.userlabel.setText('Welcome, ' + name)
        super().show()


    def addpages(self, pages):
        self.pages = pages

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('fusion'))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        #toplayout
        self.toplayout = QHBoxLayout()
        self.toplayout.setSpacing(0)
        self.toplayout.setContentsMargins(0,0,0,20)
        self.userlabel = QLabel('Welcome ')
        logoutbutton = QPushButton("logout")
        logoutbutton.setFlat(True)
        logoutbutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logoutbutton.clicked.connect(self.handle_logout_button)
        self.toplayout.addWidget(self.userlabel, alignment=Qt.AlignLeft)
        self.toplayout.addWidget(logoutbutton, alignment=Qt.AlignRight)


        self.label = QLabel('Spotify Playlist Generator')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('font: 18pt Comic Sans MS')

        self.create_playlist_type_group()

        self.setWindowTitle('Spotify Playlist Generator')
        #self.resize(400, 300)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.label.setContentsMargins(0,0,0,20)
        self.layout.addLayout(self.toplayout)
        self.layout.addWidget(self.label, alignment=Qt.AlignTop)
        self.layout.addWidget(self.playlistgroupbox)

        self.popup = QMessageBox()
        self.popup.setWindowTitle('Success')
        self.popup.setStandardButtons(QMessageBox.Close)

        

    def create_playlist_type_group(self):
        self.playlistgroupbox = QGroupBox('Choose Playlist Type')
        self.checkboxes['upbeat'] = QRadioButton("upbeat")
        self.checkboxes['chill'] = QRadioButton("chill")
        self.checkboxes['feels'] = QRadioButton("feels")
        self.checkboxes['acoustic'] = QRadioButton("acoustic")

        generatebutton = QPushButton('generate')
        generatebutton.setDefault(True)
        generatebutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        generatebutton.clicked.connect(self.handle_generate_button)

        layout = QVBoxLayout()
        layout.addWidget(self.checkboxes['upbeat'])
        layout.addWidget(self.checkboxes['chill'])
        layout.addWidget(self.checkboxes['feels'])
        layout.addWidget(self.checkboxes['acoustic'])
        layout.addWidget(generatebutton, stretch=15, alignment=Qt.AlignBottom|Qt.AlignLeft)
        layout.addStretch(1)
        self.playlistgroupbox.setLayout(layout)    

    def get_checked_boxes(self):
        checked = []
        for key in self.checkboxes.keys():
            if self.checkboxes[key].isChecked():
                checked.append(key)
        return checked

    def handle_generate_button(self):
        checked = self.get_checked_boxes()
        if len(checked) == 0:
            return

        for key in checked:
            create_playlist(self.sp, key, key + ' playlist', public = False)
        
        for box in self.checkboxes.values():
            box.setChecked(False)
        self.checkboxes['upbeat'].setChecked(False)

        self.popup.setText('successfully created ' + checked[0] + ' playlist.')
        self.popup.exec()
        

    def handle_logout_button(self):
        os.remove('.cache-user')
        self.pages.mainpage.hide()
        self.pages.frontpage.show()