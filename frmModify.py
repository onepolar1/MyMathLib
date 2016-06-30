#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createQuestionInfo()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QTextEdit()
        bigEditor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.quesInfoGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createMenu(self):
        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createQuestionInfo(self):
        self.quesInfoGroupBox = QGroupBox("题目属性")
        layout = QHBoxLayout()
        layout.setMargin(10)
        layout.setAlignment(Qt.AlignHCenter)

        layout.addStretch(10)
        label1 = QLabel("类别")
        lineEdit1 = QComboBox()
        layout.addWidget(label1)
        layout.addWidget(lineEdit1)
        
        layout.addStretch(10)        
        label2 = QLabel("题型")
        lineEdit2 = QComboBox()
        layout.addWidget(label2)
        layout.addWidget(lineEdit2)

        layout.addStretch(10)        
        label3 = QLabel("年份")
        lineEdit3 = QComboBox()
        layout.addWidget(label3)
        layout.addWidget(lineEdit3)

        layout.addStretch(10)        
        label4 = QLabel("关键字")
        lineEdit4 = QLineEdit()
        layout.addWidget(label4)
        layout.addWidget(lineEdit4)

        layout.addStretch(10) 
        btn = QPushButton("查询")        
        layout.addWidget(btn)

        layout.addStretch(10)        
        # layout.addStretch(10)        
        # label.setBuddy(lineEdit)

        # layout.setColumnStretch(0, 1)
        # layout.setColumnMinimumWidth(0,20)
        # layout.setColumnMinimumWidth(1,20)
        # layout.setColumnStretch(1, 10)
        self.quesInfoGroupBox.setLayout(layout)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(Dialog.NumButtons):
            button = QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("题目信息填写")
        layout = QGridLayout()

        # for i in range(Dialog.NumGridRows):
        #     label = QLabel("Line %d:" % (i + 1))
        #     lineEdit = QLineEdit()
        #     layout.addWidget(label, i + 1, 0)
        #     layout.addWidget(lineEdit, i + 1, 1)


        self.questionEditor = QTextEdit()
        self.questionEditor.setPlainText("题目信息填写")
        self.answerEditor = QTextEdit()
        self.answerEditor.setPlainText("答案信息填写")

        layout.addWidget(self.questionEditor, 0, 0)
        layout.addWidget(self.answerEditor, 0, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
