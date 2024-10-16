from PySide6 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden

class Plugin:
    def __init__(self):
        self.mainWindowButton = None

    def createMainWindowButtons(self):
        self.mainWindowButton = QtWidgets.QPushButton()
        self.mainWindowButton.setObjectName("buttonPlugin")
        self.mainWindowButton.setToolTip("Gruppenbogen erstellen")
        self.mainWindowButton.setProperty("class", "icon")
        self.mainWindowButton.setText("\uf6f0")  #  horse
        self.mainWindowButton.clicked.connect(self.createGruppenEditor) 
        return [self.mainWindowButton]

    def createGruppenEditor(self):
        print("create Editor")
