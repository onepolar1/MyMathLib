import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        textEdit = QtGui.QTextEdit('',self)
        textEdit.setGeometry(QtCore.QRect(300, 300, 640, 480))
        textEdit.move(0, 0)
        self.setGeometry(300, 300, 640, 480)

        img = QImage('images/trash.png','PNG')

        cursor = QTextCursor(textEdit.document())
        cursor.insertText("Hello World")
        cursor.insertImage(img)

        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
