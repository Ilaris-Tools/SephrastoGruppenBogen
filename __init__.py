from PySide6 import QtWidgets, QtCore, QtGui
from EventBus import EventBus
from Hilfsmethoden import Hilfsmethoden
from .GruppenEditor import GruppenEditor


class Plugin:
    """Main class and entry point. Loaded by sephrasto."""

    def __init__(self):
        self.mainWindowButton = None

    def createMainWindowButtons(self):
        """Called by sephrastos main menu. Do not rename."""
        self.mainWindowButton = QtWidgets.QPushButton()
        self.mainWindowButton.setObjectName("buttonPlugin")
        self.mainWindowButton.setToolTip("Gruppenbogen erstellen")
        self.mainWindowButton.setProperty("class", "icon")
        self.mainWindowButton.setText("\uf6f0")  #  horse
        self.mainWindowButton.clicked.connect(self.createGruppenEditor) 
        return [self.mainWindowButton]

    def createGruppenEditor(self):
        """Called on main menu button click. Opens group window."""
        self.win = GruppenEditor()
        self.win.root.show()

