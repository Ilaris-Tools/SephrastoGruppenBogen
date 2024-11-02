from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel as QL
from QtUtils.ProgressDialogExt import ProgressDialogExt
from Serialization import Serialization
from QtUtils.WebEngineViewPlus import WebEngineViewPlus
from PySide6.QtGui import QPageLayout, QPageSize

from EinstellungenWrapper import EinstellungenWrapper

from .UI.MainForm import Ui_Form as MainForm
from .UI.CharakterTab import Ui_Form as CharakterTab
from .Gruppe import Gruppe
import Charakter
import Datenbank
import json
from Wolke import Wolke


class GruppenEditor(object):
    """Main class contains all the logic for the (generated) UI."""

    def __init__(self):
        """Automatically called when the Editor window is created."""
        self.charaktere = []
        self.tabs = []
        self.savepath = None
        self.gruppe = Gruppe()
        self.root = QtWidgets.QWidget()  # empty widget to be filled
        self.ui = MainForm()  # ui from qt designer
        self.ui.setupUi(self.root)  # setup generated from qt designer
        self.setupUi()  # our setup in this wrapper
        Wolke.DB = Datenbank.Datenbank()

    def setupUi(self):
        """custom setup to add logic to ui, also called from init."""
        # buttons and actions
        self.ui.btnSave.clicked.connect(self.save)
        self.ui.btnOpen.clicked.connect(self.load)
        self.ui.btnExport.clicked.connect(self.export)
        self.ui.btnLoadChar.clicked.connect(self.addCharakter)
        # self.ui.tabs.changeEvent = self.tabChanged
        self.ui.tabs.tabBar().tabBarClicked.connect(self.tabChanged)
        # edit fields
        self.ui.leName.textChanged.connect(lambda x: setattr(self.gruppe, "name", x))
        self.ui.sbColumns.valueChanged.connect(lambda x: setattr(self.gruppe, "columns", x))
        # for fName, wName in self.gruppe.fieldMap.items():
        #     field = getattr(self.ui, wName)
        #     field.textChanged.connect(lambda: setattr(self.gruppe, fName, field.text()))
        # self.ui.leName.textChanged.connect(lambda: self.gruppe.name = self.ui.leName.text())
    
    def updateUI(self, renderChars=False):
        """Update the UI."""
        for idx in reversed(range(self.ui.tabs.count()-1)):
            if idx != 0:
                self.ui.tabs.removeTab(idx)
        for idx, char in enumerate(self.charaktere):
            if renderChars:
                self.renderCharTab(char) 
            self.ui.tabs.insertTab(idx+1, char.tab.widget, char.name)
    
    def tabChanged(self, tabNumber):
        """Called when tab is changed."""
        if tabNumber == len(self.charaktere)+1:
            self.addCharakter()
    
    def addCharakter(self):
        """Add a new character to the group."""
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.root, "Charakter laden", Wolke.Settings["Pfad-Chars"], 
            "XML Dateien (*.xml);;Alle Dateien (*)")
        if not filePath:
            return
        char = self.loadChar(filePath)
        char.tab = self.charakterTab()
        self.renderCharTab(char)
        self.charaktere.append(char)
        self.updateUI()

    def charakterTab(self):
        charTab = CharakterTab()
        charTab.widget = QtWidgets.QWidget()
        charTab.setupUi(charTab.widget)
        charTab.btnRemove.clicked.connect(self.removeCurrentChar)
        return charTab

    def renderCharTab(self, char):
        # char.tab.widget.gbAllgemein.setLayout(QtWidgets.QHBoxLayout())
        # char.tab.widget.gbAllgemein.layout().addWidget(QL(f"Name: {char.name}"))
        for group in ["Attributexxx", "Vorteile", "Fertigkeiten", "Zauber"]:
            gb = QtWidgets.QGroupBox()
            gb.setTitle(group)
            char.tab.widget.layout().addWidget(gb)
        # char.tab.gbAllgemein.addWidget(QL(f"Name: {char.name}"))

    def removeCurrentChar(self):
        idx = self.ui.tabs.currentIndex()
        self.charaktere.pop(idx-1)
        self.updateUI()

    def loadChar(self, path):
        # path = "/home/buki/cloud/fremd/dsa/helden/asdf_alrik.xml"
        # copied from CharakterEditor.py, remmoved plugin stuff (no need for read only yet)
        try:
            dlg = ProgressDialogExt(minimum = 0, maximum = 100)
            dlg.disableCancel()
            dlg.setWindowTitle("Charakter laden")    
            dlg.show()
            dlg.setLabelText("Lade Datenbank")
            dlg.setValue(0, True)
            storedHausregeln = Charakter.Char.hausregelnLesen(path)
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
            Wolke.Char.savepath = path
            success, loadResult = Wolke.Char.loadFile(path)
            # if loadResult[0] != Wolke.Char.LoadResultNone:
            #     messageBox = QtWidgets.QMessageBox()
            #     icon = { 1 : QtWidgets.QMessageBox.Information, 2 : QtWidgets.QMessageBox.Warning, 3 : QtWidgets.QMessageBox.Critical }
            #     messageBox.setIcon(icon[loadResult[0]])
            #     messageBox.setWindowTitle(loadResult[1])
            #     messageBox.setText(loadResult[2])
            #     messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            #     messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  
            #     messageBox.exec()

            if not success:
                Wolke.Char.savepath = ""

            dlg.setValue(70, True)   

            Wolke.Char.aktualisieren() # A bit later because it needs access to itself

            dlg.setLabelText("Starte Editor")
            dlg.setValue(80, True)
        finally:
            dlg.hide()
            dlg.deleteLater()
        return Wolke.Char

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

    def save(self, saveAs=False):
        """Called on save button click."""
        if saveAs or not self.savepath:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.root, "Gruppe speichern", Wolke.Settings["Pfad-Chars"], 
                "JSON Dateien (*.json);;Alle Dateien (*)")
            if not fname:
                return
            # self.savepath = newPath  # change here or after serialization or success?
        else:
            fname = self.savepath
        gruppe = {}
        if not self.ui.leName.text():
            QtWidgets.QMessageBox.warning(self.root, "Fehler", "Bitte Gruppenname eingeben.")
            return
        gruppe["name"] = self.ui.leName.text()
        gruppe["charaktere"] = []
        for char in self.charaktere:
            ser = Serialization.getSerializer(".json", 'Charakter')
            char.serialize(ser)
            gruppe["charaktere"].append(ser.root["Charakter"])
            dechar = Charakter.Char()
            deser = Serialization.getDeserializer(".json", 'Charakter')
            deser.initFromSerializer(ser)
            deser.find("Charakter")  # TODO: fix this in serializer? should start at char node not root?
            dechar.deserialize(deser)
            dechar.aktualisieren()  # berechnet abgeleitete Werte wie WS
            print(dechar.name)
            print(dechar.vorteile)
        print(fname)
        with open(fname, "w") as f:
            json.dump(gruppe, f, indent=4, ensure_ascii=False)

    def load(self):
        """Called on load button click."""
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.root, "Gruppe laden", Wolke.Settings["Pfad-Chars"], 
            "JSON Dateien (*.json);;Alle Dateien (*)")
        if not fname:
            return
        with open(fname, "r") as f:
            gruppe = json.load(f)
        self.ui.leName.setText(gruppe["name"])
        # TODO: ask if unsaved changes.. clear or respawn GruppenEditor?
        self.charaktere = []  # make sure allfields are updated and title etc..
        for charDict in gruppe["charaktere"]:
            # preload hausregeln 
            storedHausregeln = gruppe.get("hausregeln", "Keine")
            availableHausregeln = EinstellungenWrapper.getDatenbanken(Wolke.Settings["Pfad-Regeln"])
        
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

            char = Charakter.Char()
            deser = Serialization.getDeserializer(".json", 'Charakter')
            deser._nodeStack = [{"Charakter": charDict}]
            deser._tagStack = []
            deser._currentNode = deser._nodeStack[0]
            # deser.initFromSerializer(ser)
            deser.find("Charakter")
            char.deserialize(deser)
            char.aktualisieren()
            print(char.name)
            char.tab = self.charakterTab()
            self.charaktere.append(char)
        self.updateUI(renderChars=True)
        
    def export(self):
        """Called on export button click."""
        import os
        import PdfSerializer
        htmlPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        pdfFile = os.path.join(htmlPath, "test.pdf")
        html = self.gruppe.toHtml(self.charaktere)
        with open(os.path.join(htmlPath, "test.html"), "w") as f:
            f.write(html)

        pl = QtGui.QPageLayout()
        pl.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A4))
        pl.setOrientation(QtGui.QPageLayout.Landscape)
        pl.setTopMargin(0)
        pl.setRightMargin(0)
        pl.setBottomMargin(0)
        pl.setLeftMargin(0)
        # webEngineView = WebEngineViewPlus()
        pfad = PdfSerializer.convertHtmlToPdf(html, htmlPath, pl, out_file=pdfFile)
        print(pfad)
