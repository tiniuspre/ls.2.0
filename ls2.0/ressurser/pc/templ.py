from ressurser.delt.SqlKobling import *
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import QtGui, QtWidgets
from threading import *
from time import *


class Vindu(QWidget):
    skrift_strls = 10

    def __init__(self):
        super().__init__()

    @property
    def skrift_type(self):
        return "Times"

    def skrift_size_prop(self):
        size = 10
        return size

    def bygg(self):
        self.logg_in()

    def logg_in(self):
        self.brukernavn = self.entry_boks_med_tekst(tekst="Brukernavn", plass_y=100)
        self.passord = self.entry_boks_med_tekst(tekst="Passord", plass_y=200)
        self.lisens = self.entry_boks_med_tekst(tekst="Lisens", plass_y=300)
        self.knapp(knapp_tekst="Ok", plass_y=400, plass_x=100, size_x=280, target=self.innloggingsjekk_thr_start)
        #self.connect(self.knapp, pyqtSignal("clicked()"), self.innlogging_sjekk)

    def initUI(self):
        self.setGeometry(800, 800, 800, 660)
        self.setWindowTitle(self.vindu_navn)
        self.setWindowIcon(QIcon(self.vindu_bilde))

    def tabs(self, navn="Navn"):
        layout = QGridLayout()
        self.setLayout(layout)
        tabwidget = QTabWidget()
        label1 = self.knapp()
        self.widget = tabwidget.addTab(label1, f"{navn}")
        layout.addWidget(tabwidget)
        self.show()

    def knapp(self, knapp_tekst="Velg Tekst", font=f"{skrift_type}", skrift_size=skrift_strls, plass_x=0, plass_y=0, hover_tekst="Knapp", size_x=100, size_y=50, target=None):
        knapp = QPushButton(f'{knapp_tekst}', self)
        knapp.setFont(QtGui.QFont(font, skrift_size, QtGui.QFont.Bold))
        knapp.setToolTip(f'{hover_tekst}')
        knapp.resize(size_x, size_y)
        knapp.move(plass_x, plass_y)
        if target is not None:
            knapp.clicked.connect(target)
        return knapp

    def vis_tekst(self, tekst="TEKST", font=f"{skrift_type}", plass_x=100, plass_y=100, skrift_size=skrift_strls):
        self.lb = QLabel(f'{tekst}', self)
        self.lb.setFont(QtGui.QFont(font, skrift_size, QtGui.QFont.Bold))
        self.lb.move(plass_x, plass_y)
        return self.lb

    def entry_boks(self, navn, tekst=" ", font=f"{skrift_type}", plass_x=100, plass_y=100, skrift_size=skrift_strls, box_size_x=280, box_size_y=40):
        textbox = QLineEdit(self)
        textbox.move(plass_x, plass_y)
        textbox.setFont(QtGui.QFont(font, skrift_size, QtGui.QFont.Bold))
        textbox.resize(box_size_x, box_size_y)
        textbox.setObjectName(navn)
        textbox.setText(tekst)
        return textbox

    def entry_boks_med_tekst(self, tekst="TEKST", font=f"{skrift_type}", plass_x=100, plass_y=100, skrift_size=skrift_strls, box_size_x=280, box_size_y=40):
        widget = QWidget()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.layout)

        self.vis_tekst(plass_y=plass_y, plass_x=plass_x, tekst=tekst, font=font, skrift_size=skrift_size)
        self.entry_boks(tekst, plass_y=plass_y+20, plass_x=plass_x, box_size_y=box_size_y, box_size_x=box_size_x, font=font, skrift_size=skrift_size)

    def innloggingsjekk_thr_start(self):
        thr1 = Thread(target=self.innlogging_sjekk, args=[])
        thr1.start()

    @pyqtSlot()
    def innlogging_sjekk(self):
        tekst_ = testKobling().test()
        #shost = self.brukernavn.text()
        #print(shost)

        tekst = self.vis_tekst(tekst=tekst_, plass_x=600)
        tekst.show()
