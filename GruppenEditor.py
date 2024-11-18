from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel as QL
from QtUtils.ProgressDialogExt import ProgressDialogExt
from Serialization import Serialization
from QtUtils.WebEngineViewPlus import WebEngineViewPlus
from QtUtils.RichTextButton import RichTextPushButton, RichTextToolButton
from PySide6.QtGui import QPageLayout, QPageSize
import os
import PdfSerializer
from collections import defaultdict
from EinstellungenWrapper import EinstellungenWrapper
from .UI.SelectionDialog import SelectionDialog
# from Core.Fertigkeit import UeberFertigkeit, Fertigkeit
from Core.Talent import Talent

from .UI.MainForm import Ui_Form as MainForm
from .UI.CharakterTab import Ui_Form as CharakterTab
from .Gruppe import Gruppe
import Charakter
import Datenbank
import json
from Wolke import Wolke


class MyProgressDLG(ProgressDialogExt):
    def __init__(self, title="Laden", parent=None):
        super().__init__(parent)
        self.disableCancel()
        self.setWindowTitle(title)
        self.setLabelText("Lade Datenbank")
        self.show()

    def tick(self, value, label=None):
        self.setValue(value)
        if label is not None:
            self.setLabelText(label)

    def stop(self):
        self.hide()
        self.deleteLater()

class IconBtn(RichTextToolButton):
    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.setText(f"<span style='{Wolke.FontAwesomeCSS}'>{icon}</span>&nbsp;&nbsp;{text}")
    

class GruppenEditor(object):
    """Main UI class contains all the logic for the GruppenEditor Window."""

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
        self.updateUI()
        self.selectionDialog = None
        Wolke.DB = Datenbank.Datenbank()

    def setupUi(self):
        """custom setup to add logic to ui, also called from init."""
        # buttons and actions
        self.ui.btnOpen = IconBtn("\uf07c", "Öffnen")
        self.ui.btnSave = IconBtn("\uf0c7", "Speichern")
        self.ui.btnExport = IconBtn("\uf1c1", "Exportieren")
        self.ui.bottomBar.layout().addWidget(self.ui.btnOpen)
        self.ui.bottomBar.layout().addWidget(self.ui.btnSave)
        self.ui.bottomBar.layout().addWidget(self.ui.btnExport)
        # self.ui.btnSave.setText("<span style='" + Wolke.FontAwesomeCSS + f"'>\uf1c1</span>&nbsp;&nbsp;Speichern")
        self.ui.btnSave.clicked.connect(self.save)
        self.ui.btnOpen.clicked.connect(self.load)
        self.ui.btnExport.clicked.connect(self.export)
        self.ui.btnLoadChar.clicked.connect(self.addCharakter)
        self.ui.btnEditFertigkeiten.clicked.connect(self.openFertigkeitenDialog)
        self.ui.btnEditVorteile.clicked.connect(self.openVorteileDialog)
        self.ui.btnEditZauber.clicked.connect(self.openZauberDialog)
        # self.ui.tabs.changeEvent = self.tabChanged
        self.ui.tabs.tabBar().tabBarClicked.connect(self.tabChanged)
        # edit fields
        self.ui.leName.textChanged.connect(lambda x: setattr(self.gruppe, "name", x))
        self.ui.sbColumns.valueChanged.connect(lambda x: setattr(self.gruppe, "columns", x))
        self.ui.cbFreieFertigkeiten.stateChanged.connect(lambda x: setattr(self.gruppe, "freiefertigkeiten", x==2))
        self.ui.cbBeschreibung.stateChanged.connect(lambda x: setattr(self.gruppe, "beschreibung", x==2))
        self.ui.ddFertigkeiten.currentTextChanged.connect(lambda x: setattr(self.gruppe, "fertigkeitenStrategie", x))
        self.ui.ddVorteile.currentTextChanged.connect(lambda x: setattr(self.gruppe, "vorteileStrategie", x))
        self.ui.ddZauber.currentTextChanged.connect(lambda x: setattr(self.gruppe, "zauberStrategie", x))
        # for fName, wName in self.gruppe.fieldMap.items():
        #     field = getattr(self.ui, wName)
        #     field.textChanged.connect(lambda: setattr(self.gruppe, fName, field.text()))
        # self.ui.leName.textChanged.connect(lambda: self.gruppe.name = self.ui.leName.text())
        
        # make tab titles headings
        # self.ui.tabs.setStyleSheet('QTabBar { font-weight: bold; font-size: ' + str(Wolke.FontHeadingSizeL1) + 'pt; font-family: \"' + Wolke.Settings["FontHeading"] + '\"; }')
    
    def updateUI(self, renderChars=False):
        """Update the UI."""
        # update group form
        self.updateGroupTab()
        # update charakter tabs
        for idx in reversed(range(self.ui.tabs.count()-1)):
            if idx != 0:
                self.ui.tabs.removeTab(idx)
        for idx, char in enumerate(self.charaktere):
            if renderChars:
                self.renderCharTab(char) 
            self.ui.tabs.insertTab(idx+1, char.tab.widget, char.name)
    
    def updateGroupTab(self):
        self.ui.leName.setText(self.gruppe.name)
        self.ui.sbColumns.setValue(self.gruppe.columns)
        self.ui.cbFreieFertigkeiten.setChecked(self.gruppe.freiefertigkeiten)
        self.ui.cbBeschreibung.setChecked(self.gruppe.beschreibung)
        self.ui.cbBild.setChecked(self.gruppe.bild)
        self.ui.cbAttribute.setChecked(self.gruppe.attribute)
        self.ui.cbEigenheiten.setChecked(self.gruppe.eigenheiten)
        self.ui.cbKampfwerte.setChecked(self.gruppe.kampfwerte)
        # self.ui.cbEp.setChecked(self.gruppe.ep)
        self.ui.ddFertigkeiten.setCurrentText(self.gruppe.fertigkeitenStrategie)
        self.ui.ddVorteile.setCurrentText(self.gruppe.vorteile.capitalize())
        self.ui.ddZauber.setCurrentText(self.gruppe.zauber.capitalize())

    
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
        # gruppe = {}
        gruppe = self.gruppe.toDict()
        if not self.ui.leName.text():
            QtWidgets.QMessageBox.warning(self.root, "Fehler", "Bitte Gruppenname eingeben.")
            return
        # gruppe["name"] = self.ui.leName.text()
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
        self.savepath = fname
        # loading bar dialog
        dlg = ProgressDialogExt(minimum = 0, maximum = 100)
        dlg.disableCancel()
        dlg.setWindowTitle("Gruppe laden")    
        dlg.show()
        dlg.setLabelText("Lade Gruppendatei")
        dlg.setValue(0, True)
        with open(fname, "r") as f:
            gruppe = json.load(f)
        dlg.setValue(10, True)
        # self.ui.leName.setText(gruppe["name"])  # part of updateUI
        chars = gruppe.pop("charaktere")
        self.gruppe = Gruppe.fromDict(gruppe)
        # TODO: ask if unsaved changes.. clear or respawn GruppenEditor?
        self.charaktere = []  # make sure allfields are updated and title etc..
        count = len(chars)
        step = 80 // count
        for charIdx, charDict in enumerate(chars):
            dlg.setLabelText(f"Lade Charakter {charIdx+1} von {count}")
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
            dlg.setValue(10 + step * (charIdx + 1), True)
        dlg.setLabelText("Starte Editor")
        self.updateUI(renderChars=True)
        dlg.setValue(100, True)
        dlg.hide()
        dlg.deleteLater()
        
    def export(self):
        """Called on export button click."""
        if self.savepath:
            fname = self.savepath.replace(".json", ".pdf")
        else:
            fname = Wolke.Settings["Pfad-Chars"]
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.root, "Gruppe Exportieren", fname,
            "PDF Dateien (*.pdf);;HTML Dateien (*.html);;Alle Dateien (*)")
        if not fname:
            return
        dlg = MyProgressDLG("Gruppe exportieren")
        dlg.tick(10, "Generiere HTML")
        htmlPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        htmlExport = fname.endswith(".html")
        html = self.gruppe.toHtml(self.charaktere)  # todo fix paths if html export
        if htmlExport:
            dlg.tick(50, "Speichere HTML")
            with open(os.path.join(htmlPath, fname), "w") as f:
                f.write(html)
            dlg.setValue(100, True)
            dlg.hide()
            dlg.deleteLater()
        dlg.tick(50, "Generiere PDF")
        pl = QtGui.QPageLayout()
        pl.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A4))
        pl.setOrientation(QtGui.QPageLayout.Landscape)
        pl.setTopMargin(0)
        pl.setRightMargin(0)
        pl.setBottomMargin(0)
        pl.setLeftMargin(0)
        # TODO: looks like file is not saved when opened somewhere (no error)
        path = PdfSerializer.convertHtmlToPdf(html, htmlPath, pl, out_file=fname)
        dlg.tick(100, "Fertig gespeichert")
        dlg.stop()
    
    def getFertigkeitenDict(self):
        self.loadDB("Keine")  # TODO: fix me
        fertigkeiten = Wolke.DB.fertigkeiten
        data = defaultdict(list)
        for name, f in fertigkeiten.items():
            if f.kampffertigkeit:
                data[f.displayName.replace("profan", "kampf")].append(f.name)
            else:
                data[f.displayName].append(f.name)
        return data
    
    def getVorteileDict(self):
        self.loadDB("Keine") 
        vorteile = Wolke.DB.vorteile
        db = Wolke.DB
        kategorien = list(Wolke.DB.einstellungen["Vorteile: Kategorien"].wert.keys())
        data = defaultdict(list)
        for name, v in vorteile.items():
            k = kategorien[v.kategorie]
            print(k)
            # k = Wolke.DB.vorteilkategorien[v.kategorie]
            print(k)
            data[k].append(v.name)
        return data

    def geZauberDict(self):
        self.loadDB("Keine")
        zauber = Wolke.DB.zauber
        return []
    
    def openFertigkeitenDialog(self):
        """Open the Fertigkeiten dialog."""
        # widget = QtWidgets.QWidget()
        data = self.getFertigkeitenDict()
        self.selectionDialog = SelectionDialog(data)
        self.selectionDialog.save = self.saveFertigkeiten
        self.selectionDialog.setWindowTitle("Fertigkeiten auswählen")
        self.selectionDialog.selectItems(self.gruppe.fertigkeiten)
        self.selectionDialog.show()
    
    def openVorteileDialog(self):
        """Open the Vorteile dialog."""
        # widget = QtWidgets.QWidget()
        data = self.getVorteileDict()
        self.selectionDialog = SelectionDialog(data)
        self.selectionDialog.save = self.saveVorteile
        self.selectionDialog.setWindowTitle("Vorteile auswählen")
        self.selectionDialog.selectItems(self.gruppe.vorteile)
        self.selectionDialog.show()
    
    def openZauberDialog(self):
        """Open the Zauber dialog."""
        # widget = QtWidgets.QWidget()
        data = self.geZauberDict()
        self.selectionDialog = SelectionDialog(data)
        self.selectionDialog.save = self.saveZauber
        self.selectionDialog.setWindowTitle("Zauber auswählen")
        self.selectionDialog.selectItems(self.gruppe.zauber)
        self.selectionDialog.show()

    def saveFertigkeiten(self):
        """Save the selected Fertigkeiten."""
        self.gruppe.fertigkeiten = self.selectionDialog.selectedItems.copy()
        print("Fertigkeiten updated.")
        self.updateUI()
        self.selectionDialog.close()
    
    def saveVorteile(self):
        """Save the selected Vorteile."""
        self.gruppe.vorteile = self.selectionDialog.selectedItems.copy()
        # self.ui.bt
        print("Vorteile updated.")
        self.updateUI()
        self.selectionDialog.close()
    
    def saveZauber(self):    
        """Save the selected Zauber."""
        self.gruppe.zauber = self.selectionDialog.selectedItems.copy()
        print("Zauber updated.")
        self.updateUI()
        self.selectionDialog.close()