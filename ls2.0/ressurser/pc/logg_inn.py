from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtGui, QtWidgets
from threading import *
from time import *
from ressurser.pc.templ import Vindu


class entry_med_tekst:
    def __init__(self):
        super().__init__()

    def tekst(self, tekst_="TEST"):
        self.lb = QLabel(f'{tekst_}')
        return self.lb

    def entry(self, tekst_="TEST"):
        self.textbox = QLineEdit()
        self.textbox.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.textbox.resize(280, 40)
        self.textbox.setObjectName("navn")
        self.textbox.setText(tekst_)
        return self.textbox


class loggInn(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.show()

    def logg_inn(self):

        groupbox = QGroupBox("Log Inn")
        groupbox.setCheckable(False)
        self.layout.addWidget(groupbox)

        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)

        l1 = entry_med_tekst().tekst(tekst_="Brukernavn")
        e1 = entry_med_tekst().entry(tekst_="Brukernavn")

        l2 = entry_med_tekst().tekst(tekst_="Passord")
        e2 = entry_med_tekst().entry(tekst_="Passord")

        l3 = entry_med_tekst().tekst(tekst_="Lisens")
        e3 = entry_med_tekst().entry(tekst_="Lisens")

        vbox.addWidget(l1)
        vbox.addWidget(e1)
        vbox.addWidget(l2)
        vbox.addWidget(e2)
        vbox.addWidget(l3)
        vbox.addWidget(e3)

        return vbox