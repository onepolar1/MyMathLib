#!/usr/bin/env python
from resources import *

class QuesModifyDlg(QDialog):
    def __init__(self, parent=None,  db="", curuser=""):
        super(QuesModifyDlg, self).__init__()

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.createQuestionDisp()
        self.createQuestionInfo()
        self.createQuestionEditor()
        self.createButtons()

        # mainLayout = QVBoxLayout()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.quesInfoGroupBox, 0, 0)
        mainLayout.addWidget(self.quesDispGroupBox, 1, 0)
        mainLayout.addWidget(self.quesEditorGroupBox, 2, 0)
        mainLayout.addWidget(self.horizontalGroupBox, 3, 0)

        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 10)
        mainLayout.setRowStretch(2, 10)
        mainLayout.setRowStretch(3, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("题目信息维护")

    def refreshQuestionDisp(self):
        questionstr = self.questionEditor.toPlainText()
        self.questionDisp.setHtmlString(mdProcessor.convert(questionstr))

    def refreshAnswerDisp(self):
        answerstr = self.answerEditor.toPlainText()
        self.answerDisp.setHtmlString(mdProcessor.convert(answerstr))

    def createQuestionDisp(self):
        self.quesDispGroupBox = QGroupBox("题目显示效果")
        layout = QGridLayout()

        self.questionDisp = myqwebview()
        # somestr = mdProcessor.convert("$a=b^2$")
        self.questionDisp.setHtmlString("")
        self.answerDisp = myqwebview()
        # somestr = mdProcessor.convert("$s = \pi \\times r^2$")
        self.answerDisp.setHtmlString("")

        layout.addWidget(self.questionDisp, 0, 0)
        layout.addWidget(self.answerDisp, 0, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        # layout.setRowMinimumHeight(0, 100)
        # layout.setRowMinimumHeight(1, 100)
        self.quesDispGroupBox.setLayout(layout)

    def selectComboxItems(self, sqlstr):
        query = QSqlQuery(self.db)
        ret= query.exec_(sqlstr)
        lstitems = []
        while query.next():
            lstitems.append(query.value(0))
        return lstitems

    def createQuestionInfo(self):
        self.quesInfoGroupBox = QGroupBox("设置题目属性")
        layout = QHBoxLayout()
        layout.setMargin(10)
        layout.setAlignment(Qt.AlignHCenter)

        layout.addStretch(10)
        label1 = QLabel("类别")
        self.quesCategoryCombox = QComboBox()
        lstitems = self.selectComboxItems("select category  from categorytable")
        self.quesCategoryCombox.addItems(lstitems)
        # self.quesCategoryCombox.insertItem(0, "")
        self.quesCategoryCombox.setCurrentIndex(0)
        layout.addWidget(label1)
        layout.addWidget(self.quesCategoryCombox)

        layout.addStretch(10)
        label2 = QLabel("题型")
        self.quesTypeCombox = QComboBox()
        lstitems = self.selectComboxItems("select questiontype  from questypetable")
        self.quesTypeCombox.addItems(lstitems)
        # self.quesTypeCombox.insertItem(0, "")
        self.quesTypeCombox.setCurrentIndex(0)
        layout.addWidget(label2)
        layout.addWidget(self.quesTypeCombox)

        layout.addStretch(10)
        label3 = QLabel("年份")
        self.quesWhichyearCombox = QComboBox()
        lstitems = self.selectComboxItems("select whichyear  from yearstable")
        self.quesWhichyearCombox.addItems(lstitems)
        # self.quesWhichyearCombox.insertItem(0, "")
        self.quesWhichyearCombox.setCurrentIndex(0)
        layout.addWidget(label3)
        layout.addWidget(self.quesWhichyearCombox)

        layout.addStretch(10)
        # layout.addStretch(10)
        # label.setBuddy(lineEdit)

        # layout.setColumnStretch(0, 1)
        # layout.setColumnMinimumWidth(0,20)
        # layout.setColumnMinimumWidth(1,20)
        # layout.setColumnStretch(1, 10)
        self.quesInfoGroupBox.setLayout(layout)

    def createButtons(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()

        # btnFresh = QPushButton("预览")
        btnSave = QPushButton("保存")
        btnClean = QPushButton("清空")
        btnClose = QPushButton("关闭")

        # layout.addWidget(btnFresh)
        layout.addStretch(10)
        layout.addWidget(btnSave)
        layout.addWidget(btnClean)
        layout.addWidget(btnClose)

        # btnFresh.clicked.connect(self.refreshDisp)
        btnSave.clicked.connect(self.saveQuestion)
        btnClose.clicked.connect(self.accept)
        self.horizontalGroupBox.setLayout(layout)

    def saveQuestion(self):
        quesCategory    = self.quesCategoryCombox.currentText()
        quesType        = self.quesTypeCombox.currentText()
        quesWhichyear   = self.quesWhichyearCombox.currentText()
        question        = self.questionEditor.toPlainText()
        answer          = self.answerEditor.toPlainText()
        print(quesCategory, quesType, quesWhichyear, question, answer)

        query = QSqlQuery(self.db)
        query.prepare("insert into questiontable \
            (questionhtml, answerhtml, category, questiontype, whichyear, demo) \
            values (:questionhtml, :answerhtml, :category, :questiontype, :whichyear, :demo)")
        query.bindValue(":questionhtml", question)
        query.bindValue(":answerhtml", answer)
        query.bindValue(":category", quesCategory)
        query.bindValue(":questiontype", quesType)
        query.bindValue(":whichyear", quesWhichyear)
        query.bindValue(":demo", '')
        query.exec_()

    def insertImg(self):
        tmpstr = self.questionEditor.toPlainText()
        tmpstr += '''<img src="images/trash.png" height="20" width="20" />'''
        self.questionEditor.setPlainText(tmpstr)

    def insertImg2(self):
        tmpstr = self.answerEditor.toPlainText()
        tmpstr += '''<img src="images/trash.png" height="20" width="20" />'''
        self.answerEditor.setPlainText(tmpstr)


    def createQuestionEditor(self):
        self.quesEditorGroupBox = QGroupBox("题目信息填写")
        layout = QGridLayout()

        btnInsertImg = QPushButton("插入图片")
        btnInsertImg2 = QPushButton("插入图片")

        self.questionEditor = QTextEdit()
        self.questionEditor.setPlainText("题目信息填写")
        self.questionEditor.textChanged.connect(self.refreshQuestionDisp)
        self.answerEditor = QTextEdit()
        self.answerEditor.setPlainText("答案信息填写")
        self.answerEditor.textChanged.connect(self.refreshAnswerDisp)

        btnInsertImg.clicked.connect(self.insertImg)
        btnInsertImg2.clicked.connect(self.insertImg2)

        layout.addWidget(btnInsertImg, 0, 0, Qt.AlignLeft)
        layout.addWidget(btnInsertImg2, 0, 1, Qt.AlignLeft)
        layout.addWidget(self.questionEditor, 1, 0)
        layout.addWidget(self.answerEditor, 1, 1)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 10)
        self.quesEditorGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dlg = QuesModifyDlg()
    sys.exit(dlg.exec_())
