# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainForm.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(823, 548)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabs = QTabWidget(self.frame)
        self.tabs.setObjectName(u"tabs")
        self.tabGruppe = QWidget()
        self.tabGruppe.setObjectName(u"tabGruppe")
        self.horizontalLayout_4 = QHBoxLayout(self.tabGruppe)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_4 = QFrame(self.tabGruppe)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.frame_4)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.cbWertlos = QCheckBox(self.groupBox)
        self.cbWertlos.setObjectName(u"cbWertlos")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.cbWertlos)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.sbColumns = QSpinBox(self.groupBox)
        self.sbColumns.setObjectName(u"sbColumns")
        self.sbColumns.setMinimum(1)
        self.sbColumns.setMaximum(8)
        self.sbColumns.setValue(4)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sbColumns)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label)

        self.cbHausregeln = QComboBox(self.groupBox)
        self.cbHausregeln.setObjectName(u"cbHausregeln")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.cbHausregeln)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.frame_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_2 = QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.frame_5 = QFrame(self.groupBox_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.checkBox = QCheckBox(self.frame_5)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_5.addWidget(self.checkBox)

        self.cbBild = QCheckBox(self.frame_5)
        self.cbBild.setObjectName(u"cbBild")

        self.horizontalLayout_5.addWidget(self.cbBild)

        self.cbEigenheiten = QCheckBox(self.frame_5)
        self.cbEigenheiten.setObjectName(u"cbEigenheiten")

        self.horizontalLayout_5.addWidget(self.cbEigenheiten)

        self.cbAttribute = QCheckBox(self.frame_5)
        self.cbAttribute.setObjectName(u"cbAttribute")

        self.horizontalLayout_5.addWidget(self.cbAttribute)

        self.cbKampfwerte = QCheckBox(self.frame_5)
        self.cbKampfwerte.setObjectName(u"cbKampfwerte")

        self.horizontalLayout_5.addWidget(self.cbKampfwerte)

        self.cbBeschreibung = QCheckBox(self.frame_5)
        self.cbBeschreibung.setObjectName(u"cbBeschreibung")

        self.horizontalLayout_5.addWidget(self.cbBeschreibung)


        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.frame_5)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.ddVorteile = QComboBox(self.groupBox_2)
        self.ddVorteile.addItem("")
        self.ddVorteile.addItem("")
        self.ddVorteile.addItem("")
        self.ddVorteile.setObjectName(u"ddVorteile")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.ddVorteile)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.ddFertigkeiten = QComboBox(self.groupBox_2)
        self.ddFertigkeiten.addItem("")
        self.ddFertigkeiten.addItem("")
        self.ddFertigkeiten.addItem("")
        self.ddFertigkeiten.setObjectName(u"ddFertigkeiten")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.ddFertigkeiten)

        self.cbFreieFertigkeiten = QCheckBox(self.groupBox_2)
        self.cbFreieFertigkeiten.setObjectName(u"cbFreieFertigkeiten")
        self.cbFreieFertigkeiten.setChecked(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.cbFreieFertigkeiten)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_5)

        self.ddZauber = QComboBox(self.groupBox_2)
        self.ddZauber.addItem("")
        self.ddZauber.addItem("")
        self.ddZauber.addItem("")
        self.ddZauber.setObjectName(u"ddZauber")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.ddZauber)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.tabs.addTab(self.tabGruppe, "")
        self.tabNeu = QWidget()
        self.tabNeu.setObjectName(u"tabNeu")
        self.verticalLayout_2 = QVBoxLayout(self.tabNeu)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_3 = QFrame(self.tabNeu)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btnLoadChar = QPushButton(self.frame_3)
        self.btnLoadChar.setObjectName(u"btnLoadChar")
        self.btnLoadChar.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(9)
        self.btnLoadChar.setFont(font)

        self.horizontalLayout_3.addWidget(self.btnLoadChar)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addWidget(self.frame_3)

        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ContactNew))
        self.tabs.addTab(self.tabNeu, icon, "")

        self.verticalLayout.addWidget(self.tabs)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnReloadAll = QPushButton(self.frame_2)
        self.btnReloadAll.setObjectName(u"btnReloadAll")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.btnReloadAll.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.btnReloadAll)

        self.btnRemoveCurrentChar = QPushButton(self.frame_2)
        self.btnRemoveCurrentChar.setObjectName(u"btnRemoveCurrentChar")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.btnRemoveCurrentChar.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btnRemoveCurrentChar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnOpen = QPushButton(self.frame_2)
        self.btnOpen.setObjectName(u"btnOpen")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen))
        self.btnOpen.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.btnOpen)

        self.btnSave = QPushButton(self.frame_2)
        self.btnSave.setObjectName(u"btnSave")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.btnSave.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.btnSave)

        self.btnExport = QPushButton(self.frame_2)
        self.btnExport.setObjectName(u"btnExport")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentPrint))
        self.btnExport.setIcon(icon5)

        self.horizontalLayout_2.addWidget(self.btnExport)


        self.verticalLayout.addWidget(self.frame_2)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Allgemein", None))
#if QT_CONFIG(tooltip)
        self.cbWertlos.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Bogen ohne Werte exportieren, um sie h\u00e4ndisch eintragen zu k\u00f6nnen.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cbWertlos.setText(QCoreApplication.translate("Form", u"Werte ausblenden", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Charaktere pro Seite", None))
        self.label.setText(QCoreApplication.translate("Form", u"Hausregeln", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Anzeige", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"EP", None))
        self.cbBild.setText(QCoreApplication.translate("Form", u"Bild", None))
        self.cbEigenheiten.setText(QCoreApplication.translate("Form", u"Eigenheiten", None))
        self.cbAttribute.setText(QCoreApplication.translate("Form", u"Attribute", None))
        self.cbKampfwerte.setText(QCoreApplication.translate("Form", u"Kampfwerte", None))
        self.cbBeschreibung.setText(QCoreApplication.translate("Form", u"Beschreibung", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Vorteile", None))
        self.ddVorteile.setItemText(0, QCoreApplication.translate("Form", u"Alle", None))
        self.ddVorteile.setItemText(1, QCoreApplication.translate("Form", u"Keine", None))
        self.ddVorteile.setItemText(2, QCoreApplication.translate("Form", u"Benutzerdefiniert", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Fertigkeiten", None))
        self.ddFertigkeiten.setItemText(0, QCoreApplication.translate("Form", u"Alle", None))
        self.ddFertigkeiten.setItemText(1, QCoreApplication.translate("Form", u"Keine", None))
        self.ddFertigkeiten.setItemText(2, QCoreApplication.translate("Form", u"Benutzerdefiniert", None))

        self.cbFreieFertigkeiten.setText(QCoreApplication.translate("Form", u"Freie Fertigkeiten anzeigen", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Zauber", None))
        self.ddZauber.setItemText(0, QCoreApplication.translate("Form", u"Alle", None))
        self.ddZauber.setItemText(1, QCoreApplication.translate("Form", u"Keine", None))
        self.ddZauber.setItemText(2, QCoreApplication.translate("Form", u"Benutzerdefiniert", None))

        self.tabs.setTabText(self.tabs.indexOf(self.tabGruppe), QCoreApplication.translate("Form", u"Gruppe", None))
        self.btnLoadChar.setText(QCoreApplication.translate("Form", u"Charakter laden", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabNeu), QCoreApplication.translate("Form", u"Charakter hinzuf\u00fcgen", None))
        self.btnReloadAll.setText(QCoreApplication.translate("Form", u"Alle aktualisieren", None))
        self.btnRemoveCurrentChar.setText(QCoreApplication.translate("Form", u"Charakter entfernen", None))
        self.btnOpen.setText(QCoreApplication.translate("Form", u"\u00d6ffnen", None))
        self.btnSave.setText(QCoreApplication.translate("Form", u"Speichern", None))
        self.btnExport.setText(QCoreApplication.translate("Form", u"Export", None))
    # retranslateUi

