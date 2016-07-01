#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from myQwebview import myqwebview
import markdown
try: import mdx_mathjax
except: pass

mdProcessor = markdown.Markdown(extensions=['mathjax'])

class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()

        self.createQuestionDisp()
        self.createQuestionInfo()
        self.createQuestionEditor()
        self.createHorizontalGroupBox()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.quesInfoGroupBox)
        mainLayout.addWidget(self.quesDispGroupBox)
        mainLayout.addWidget(self.quesEditorGroupBox)
        mainLayout.addWidget(self.horizontalGroupBox)

        self.setLayout(mainLayout)

        self.setWindowTitle("题目信息维护")

    def refreshDisp(self):
        questionstr = self.questionEditor.toPlainText()
        answerstr = self.answerEditor.toPlainText()
        print(mdProcessor.convert(questionstr))
        print(markdown.markdown(questionstr))
        self.questionDisp.setHtmlString(mdProcessor.convert(questionstr))
        self.answerDisp.setHtmlString(mdProcessor.convert(answerstr))
        # quesStr = self.

    def createQuestionDisp(self):
        self.quesDispGroupBox = QGroupBox("题目显示效果")
        layout = QGridLayout()

        self.questionDisp = myqwebview()
        somestr = mdProcessor.convert("$a=b^2$")
        self.questionDisp.setHtmlString(somestr)
        self.answerDisp = myqwebview()
        somestr = mdProcessor.convert("$s = \pi \\times r^2$")
        self.answerDisp.setHtmlString(somestr)

        layout.addWidget(self.questionDisp, 0, 0)
        layout.addWidget(self.answerDisp, 0, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        self.quesDispGroupBox.setLayout(layout)

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
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()

        btnFresh = QPushButton("预览")
        btnSave = QPushButton("保存")
        btnClean = QPushButton("清空")
        btnClose = QPushButton("关闭")

        layout.addWidget(btnFresh)
        layout.addWidget(btnSave)
        layout.addWidget(btnClean)
        layout.addWidget(btnClose)

        btnFresh.clicked.connect(self.refreshDisp)
        btnClose.clicked.connect(self.accept)
        self.horizontalGroupBox.setLayout(layout)

    def createQuestionEditor(self):
        self.quesEditorGroupBox = QGroupBox("题目信息填写")
        layout = QGridLayout()


        self.questionEditor = QTextEdit()
        self.questionEditor.setPlainText("题目信息填写")
        self.answerEditor = QTextEdit()
        self.answerEditor.setPlainText("答案信息填写")

        layout.addWidget(self.questionEditor, 0, 0)
        layout.addWidget(self.answerEditor, 0, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        self.quesEditorGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
