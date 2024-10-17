from PySide6 import QtCore, QtWidgets, QtGui
from .UI import MainForm

class GruppenEditor(object):
    """Main class contains all the logic for the (generated) UI."""

    def __init__(self):
        """Automatically called when the Editor window is created."""
        self.root = QtWidgets.QWidget()  # empty widget to be filled
        self.ui = MainForm.Ui_Form()  # ui from qt designer
        self.ui.setupUi(self.root)  # setup generated from qt designer
        self.setupUi()  # our setup in this wrapper

    def setupUi(self):
        """custom setup to add logic to ui, also called from init."""
        # add more setup here 
        self.ui.btn_save.clicked.connect(self.save)
    
    def save(self):
        """Called on save button click."""
        print("Save")