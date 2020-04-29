# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mikx_\IdeaProjects\BabyMathChallenge\src\gui\babymath.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BabyMath(object):
    def setupUi(self, BabyMath):
        BabyMath.setObjectName("BabyMath")
        BabyMath.resize(769, 620)
        font = QtGui.QFont()
        font.setPointSize(6)
        BabyMath.setFont(font)
        BabyMath.setStyleSheet("")
        BabyMath.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        BabyMath.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(BabyMath)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(25, 5, 25, 25)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.horizontalGroupBox.setObjectName("horizontalGroupBox")
        self.players = QtWidgets.QHBoxLayout(self.horizontalGroupBox)
        self.players.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.players.setContentsMargins(1, -1, -1, -1)
        self.players.setSpacing(0)
        self.players.setObjectName("players")
        self.camera_label = QtWidgets.QLabel(self.horizontalGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camera_label.sizePolicy().hasHeightForWidth())
        self.camera_label.setSizePolicy(sizePolicy)
        self.camera_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.camera_label.setFrameShape(QtWidgets.QFrame.Box)
        self.camera_label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera_label.setText("")
        self.camera_label.setTextFormat(QtCore.Qt.AutoText)
        self.camera_label.setScaledContents(False)
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setWordWrap(False)
        self.camera_label.setObjectName("camera_label")
        self.players.addWidget(self.camera_label)
        self.gridLayout_2.addWidget(self.horizontalGroupBox, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.detectbg_btn = QtWidgets.QPushButton(self.centralwidget)
        self.detectbg_btn.setMinimumSize(QtCore.QSize(15, 79))
        self.detectbg_btn.setMaximumSize(QtCore.QSize(125, 130))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.detectbg_btn.setFont(font)
        self.detectbg_btn.setFlat(False)
        self.detectbg_btn.setObjectName("detectbg_btn")
        self.horizontalLayout_2.addWidget(self.detectbg_btn)
        self.dialog = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.dialog.setFont(font)
        self.dialog.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog.setObjectName("dialog")
        self.horizontalLayout_2.addWidget(self.dialog)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        BabyMath.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BabyMath)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 769, 25))
        self.menubar.setObjectName("menubar")
        BabyMath.setMenuBar(self.menubar)

        self.retranslateUi(BabyMath)
        QtCore.QMetaObject.connectSlotsByName(BabyMath)

    def retranslateUi(self, BabyMath):
        _translate = QtCore.QCoreApplication.translate
        BabyMath.setWindowTitle(_translate("BabyMath", "MainWindow"))
        self.detectbg_btn.setText(_translate("BabyMath", "DETECT BG"))
        self.dialog.setText(_translate("BabyMath", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BabyMath = QtWidgets.QMainWindow()
    ui = Ui_BabyMath()
    ui.setupUi(BabyMath)
    BabyMath.show()
    sys.exit(app.exec_())

