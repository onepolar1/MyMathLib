#!/usr/bin/env python

from PyQt4 import QtCore, QtGui

class Dialog(QtGui.QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()
        self.createFormGroupBox()

        bigEditor = QtGui.QTextEdit()
        bigEditor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(bigEditor)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Basic Layouts")

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu = QtGui.QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QtGui.QGroupBox("Horizontal layout")
        layout = QtGui.QHBoxLayout()

        for i in range(Dialog.NumButtons):
            button = QtGui.QPushButton("Button %d" % (i + 1))
            layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)

    def createGridGroupBox(self):
        self.gridGroupBox = QtGui.QGroupBox("题目信息填写")
        layout = QtGui.QGridLayout()

        # for i in range(Dialog.NumGridRows):
        #     label = QtGui.QLabel("Line %d:" % (i + 1))
        #     lineEdit = QtGui.QLineEdit()
        #     layout.addWidget(label, i + 1, 0)
        #     layout.addWidget(lineEdit, i + 1, 1)


        self.questionEditor = QtGui.QTextEdit()
        self.questionEditor.setPlainText("题目信息填写")
        self.answerEditor = QtGui.QTextEdit()
        self.answerEditor.setPlainText("答案信息填写")

        layout.addWidget(self.questionEditor, 0, 0)
        layout.addWidget(self.answerEditor, 0, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        self.gridGroupBox.setLayout(layout)

    def createFormGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("Form layout")
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel("Line 1:"), QtGui.QLineEdit())
        layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
