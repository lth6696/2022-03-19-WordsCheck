# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.RBGoogle = QtWidgets.QRadioButton(self.centralwidget)
        self.RBGoogle.setStyleSheet("font: 87 10pt \"Arial Black\";")
        self.RBGoogle.setObjectName("RBGoogle")
        self.gridLayout.addWidget(self.RBGoogle, 2, 0, 1, 1)
        self.RBDeepL = QtWidgets.QRadioButton(self.centralwidget)
        self.RBDeepL.setStyleSheet("font: 87 10pt \"Arial Black\";")
        self.RBDeepL.setObjectName("RBDeepL")
        self.gridLayout.addWidget(self.RBDeepL, 2, 2, 1, 1)
        self.RBOxford = QtWidgets.QRadioButton(self.centralwidget)
        self.RBOxford.setStyleSheet("font: 87 10pt \"Arial Black\";")
        self.RBOxford.setObjectName("RBOxford")
        self.RBOxford.setChecked(True)
        self.gridLayout.addWidget(self.RBOxford, 2, 1, 1, 1)
        self.RBYouDao = QtWidgets.QRadioButton(self.centralwidget)
        self.RBYouDao.setStyleSheet("font: 87 10pt \"Arial Black\";")
        self.RBYouDao.setObjectName("RBYouDao")
        self.gridLayout.addWidget(self.RBYouDao, 2, 3, 1, 1)
        self.PBCorrect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBCorrect.sizePolicy().hasHeightForWidth())
        self.PBCorrect.setSizePolicy(sizePolicy)
        self.PBCorrect.setStyleSheet("font: 87 16pt \"Arial Black\";\n"
"background-color: rgb(118, 255, 111);")
        self.PBCorrect.setObjectName("PBCorrect")
        self.gridLayout.addWidget(self.PBCorrect, 3, 2, 1, 2)
        self.PBWrong = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBWrong.sizePolicy().hasHeightForWidth())
        self.PBWrong.setSizePolicy(sizePolicy)
        self.PBWrong.setStyleSheet("font: 87 16pt \"Arial Black\";\n"
"background-color: rgb(255, 131, 131);")
        self.PBWrong.setObjectName("PBWrong")
        self.gridLayout.addWidget(self.PBWrong, 3, 0, 1, 2)
        self.PBReplay = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBReplay.sizePolicy().hasHeightForWidth())
        self.PBReplay.setSizePolicy(sizePolicy)
        self.PBReplay.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.PBReplay.setObjectName("PBReplay")
        self.gridLayout.addWidget(self.PBReplay, 4, 0, 1, 4)
        self.PBExit = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBExit.sizePolicy().hasHeightForWidth())
        self.PBExit.setSizePolicy(sizePolicy)
        self.PBExit.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.PBExit.setObjectName("PBExit")
        self.gridLayout.addWidget(self.PBExit, 6, 0, 1, 4)
        self.TBGrade = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TBGrade.sizePolicy().hasHeightForWidth())
        self.TBGrade.setSizePolicy(sizePolicy)
        self.TBGrade.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.TBGrade.setObjectName("TBGrade")
        self.gridLayout.addWidget(self.TBGrade, 1, 0, 1, 4)
        self.TBShow = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TBShow.sizePolicy().hasHeightForWidth())
        self.TBShow.setSizePolicy(sizePolicy)
        self.TBShow.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.TBShow.setObjectName("TBShow")
        self.gridLayout.addWidget(self.TBShow, 0, 0, 1, 4)
        self.PBTranslate = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBTranslate.sizePolicy().hasHeightForWidth())
        self.PBTranslate.setSizePolicy(sizePolicy)
        self.PBTranslate.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.PBTranslate.setObjectName("PBTranslate")
        self.gridLayout.addWidget(self.PBTranslate, 5, 2, 1, 2)
        self.PBSpell = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PBSpell.sizePolicy().hasHeightForWidth())
        self.PBSpell.setSizePolicy(sizePolicy)
        self.PBSpell.setStyleSheet("font: 87 16pt \"Arial Black\";")
        self.PBSpell.setObjectName("PBSpell")
        self.gridLayout.addWidget(self.PBSpell, 5, 0, 1, 2)
        self.gridLayout.setRowStretch(0, 8)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 2)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.RBGoogle.setText(_translate("MainWindow", "Google"))
        self.RBDeepL.setText(_translate("MainWindow", "DeepL"))
        self.RBOxford.setText(_translate("MainWindow", "Oxford"))
        self.RBYouDao.setText(_translate("MainWindow", "YouDao"))
        self.PBCorrect.setText(_translate("MainWindow", "Correct"))
        self.PBWrong.setText(_translate("MainWindow", "Wrong"))
        self.PBReplay.setText(_translate("MainWindow", "Replay"))
        self.PBExit.setText(_translate("MainWindow", "Exit"))
        self.PBTranslate.setText(_translate("MainWindow", "Meaning"))
        self.PBSpell.setText(_translate("MainWindow", "Spell"))
