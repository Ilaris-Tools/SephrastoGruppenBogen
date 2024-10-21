from PySide6 import QtCore, QtWidgets, QtGui
from QtUtils.ProgressDialogExt import ProgressDialogExt

from EinstellungenWrapper import EinstellungenWrapper

from .UI import MainForm
import Charakter
import Datenbank
from Wolke import Wolke


class GruppenEditor(object):
    """Main class contains all the logic for the (generated) UI."""

    def __init__(self):
        """Automatically called when the Editor window is created."""
        self.root = QtWidgets.QWidget()  # empty widget to be filled
        self.ui = MainForm.Ui_Form()  # ui from qt designer
        self.ui.setupUi(self.root)  # setup generated from qt designer
        self.setupUi()  # our setup in this wrapper
        Wolke.DB = Datenbank.Datenbank()

    def setupUi(self):
        """custom setup to add logic to ui, also called from init."""
        # add more setup here 
        self.ui.btn_save.clicked.connect(self.save)
        self.ui.pushButton.clicked.connect(self.loadChar)
    

    def save(self):
        """Called on save button click."""
        print("Save")
    

    def loadChar(self):
        path = "/home/buki/cloud/fremd/dsa/helden/asdf_alrik.xml"
        # copied from CharakterEditor.py, remmoved plugin stuff (no need for read only yet)
        try:
            dlg = ProgressDialogExt(minimum = 0, maximum = 100)
            dlg.disableCancel()
            dlg.setWindowTitle("Charakter laden")    
            dlg.show()
            dlg.setLabelText("Lade Datenbank")
            dlg.setValue(0, True)
            self.savepath = path
            storedHausregeln = Charakter.Char.hausregelnLesen(self.savepath)
            availableHausregeln = EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"])
        
            dlg.setValue(10, True)
            if storedHausregeln in availableHausregeln:
                hausregeln = storedHausregeln
            else:
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Hausregeln nicht gefunden!")
                messagebox.setText(f"Der Charakter wurde mit den Hausregeln {storedHausregeln} erstellt. Die Datei konnte nicht gefunden werden.\n\n"\
                    "Bitte wähle aus, mit welchen Hausregeln der Charakter stattdessen geladen werden soll.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical )
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
                combo = QtWidgets.QComboBox()
                combo.addItems(availableHausregeln)
                messagebox.layout().addWidget(combo, 1, 2)
                messagebox.exec()
                hausregeln = combo.currentText()

            self.loadDB(hausregeln)

            dlg.setLabelText("Lade Charakter")
            dlg.setValue(40, True)
            Wolke.Char = Charakter.Char()
            success, loadResult = Wolke.Char.loadFile(self.savepath)
            if loadResult[0] != Wolke.Char.LoadResultNone:
                messageBox = QtWidgets.QMessageBox()
                icon = { 1 : QtWidgets.QMessageBox.Information, 2 : QtWidgets.QMessageBox.Warning, 3 : QtWidgets.QMessageBox.Critical }
                messageBox.setIcon(icon[loadResult[0]])
                messageBox.setWindowTitle(loadResult[1])
                messageBox.setText(loadResult[2])
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
                messageBox.exec()

            if not success:
                self.savepath = ""

            dlg.setValue(70, True)   

            Wolke.Char.aktualisieren() # A bit later because it needs access to itself

            dlg.setLabelText("Starte Editor")
            dlg.setValue(80, True)
        finally:
            dlg.hide()
            dlg.deleteLater()

    def loadDB(self, hausregeln):
        # copied from CharakterEditor.py
        if Wolke.DB.datei is None or Wolke.DB.hausregelDatei != hausregeln:
            if not Wolke.DB.loadFile(hausregeln = hausregeln, isCharakterEditor = True):
                messagebox = QtWidgets.QMessageBox()
                messagebox.setWindowTitle("Fehler!")
                messagebox.setText(hausregeln + " ist keine valide Datenbank-Datei! Der Charaktereditor wird ohne Hausregeln gestartet.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)  
                messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                messagebox.exec()

