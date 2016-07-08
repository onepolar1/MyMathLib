#!/usr/bin/env python
from resources import *

class QuesModifyDlg(QDialog):
    def __init__(self, parent=None,  db="", curuser="", questionstr="", answerstr=""):
        super(QuesModifyDlg, self).__init__()

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.old_questionstr = questionstr
        self.curRowid = -1

        self.createQuestionDisp()
        self.createQuestionInfo()
        self.createQuestionEditor()
        self.createButtons()
        self.setQuestionAndAnswerstr(questionstr, answerstr)

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
        self.quesTypeCombox.setCurrentIndex(1)
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

        btnNew = QPushButton("新增")
        btnSave = QPushButton("保存")
        btnClean = QPushButton("全部清空")
        # btnClose = QPushButton("关闭")

        layout.addStretch(10)
        layout.addWidget(btnNew)
        layout.addWidget(btnSave)
        layout.addWidget(btnClean)
        # layout.addWidget(btnClose)

        btnNew.clicked.connect(self.newQuestion)
        btnSave.clicked.connect(self.saveQuestion)
        btnClean.clicked.connect(self.clearQuesAndAnsStr)
        # btnClose.clicked.connect(self.accept)
        self.horizontalGroupBox.setLayout(layout)

    def newQuestion(self):
        self.curRowid = -1
        self.questionEditor.setPlainText("")
        self.answerEditor.setPlainText("")

    def clearQuesAndAnsStr(self):
        if QMessageBox.question(self, "清空确认", "是否要清空当前题目和答案？", "确定", "取消") == 0:
            self.setQuestionAndAnswerstr("", "")

    def saveQuestion(self):
        quesCategory    = self.quesCategoryCombox.currentText()
        quesType        = self.quesTypeCombox.currentText()
        quesWhichyear   = self.quesWhichyearCombox.currentText()
        question        = self.questionEditor.toPlainText()
        answer          = self.answerEditor.toPlainText()
        # print(quesCategory, quesType, quesWhichyear, question, answer)
        if question.strip() == "":
            QMessageBox.information(self, "提示", "当前题目为空，无法保存!")
            return

        query = QSqlQuery(self.db)
        if self.curRowid != -1: #正在修改已有题目
            if QMessageBox.question(self, "确认", "是否要修改已有题目？", "确定", "取消") == 0:
                updatestr = "update questiontable \
                    set questionhtml = '%s', answerhtml='%s', category='%s', questiontype='%s', whichyear='%s' \
                    where rowid='" % (question, answer, quesCategory, quesType, quesWhichyear) \
                     + str(self.curRowid)+"'"
                # print(updatestr)
                query.exec_(updatestr)
                QMessageBox.information(self, "提示", "题目更改成功!")

        elif self.curRowid == -1: #插入新的题目
            if question.strip() == self.old_questionstr.strip():
                QMessageBox.information(self, "提示", "当前题目已经存在，请无需增加同样题目!")
                return

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
            QMessageBox.information(self, "提示", "新题目添加成功!")

    def insertImg(self):
        tmpstr = self.questionEditor.toPlainText()
        tmpstr += '''<img src="images/请修改名称.png" alt="Smiley face" width="100" height="100" align="right"> '''
        self.questionEditor.setPlainText(tmpstr)

    def insertImg2(self):
        tmpstr = self.answerEditor.toPlainText()
        tmpstr += '''<img src="images/请修改名称.png" alt="Smiley face" width="100" height="100" align="right"> '''
        self.answerEditor.setPlainText(tmpstr)

    def setQuestionAndAnswerstr(self, questionstr, answerstr):
        self.questionEditor.setPlainText(questionstr)
        self.answerEditor.setPlainText(answerstr)
        query = QSqlQuery(self.db)
        query.exec_("select rowid, category, questiontype, whichyear from questiontable where questionhtml ='" + questionstr + "'")
        category      = ""
        questiontype  = ""
        whichyear     = ""
        while(query.next()):
            self.curRowid = query.value(0)
            category      = query.value(1)
            questiontype  = query.value(2)
            whichyear     = query.value(3)

        pos1 = self.quesCategoryCombox.findText(category)
        if pos1 != -1:
            self.quesCategoryCombox.setCurrentIndex(pos1)
        pos2 = self.quesTypeCombox.findText(questiontype)
        if pos2 != -1:
            self.quesTypeCombox.setCurrentIndex(pos2)
        pos3 = self.quesWhichyearCombox.findText(whichyear)
        if pos3 != -1:
            self.quesWhichyearCombox.setCurrentIndex(pos3)
        # print(pos, "------")
        # print(self.curRowid, "setQuestionAndAnswerstr")

    def createQuestionEditor(self):
        self.quesEditorGroupBox = QGroupBox("题目信息填写")
        layout = QGridLayout()

        lable1 = QLabel("请在下框中输入题目：")
        lable2 = QLabel("请在下框中输入答案：")
        btnInsertImg = QPushButton("插入图片")
        btnInsertImg2 = QPushButton("插入图片")

        self.questionEditor = QTextEdit()
        self.questionEditor.textChanged.connect(self.refreshQuestionDisp)
        # self.questionEditor.setPlainText(self.questionstr)
        self.answerEditor = QTextEdit()
        self.answerEditor.textChanged.connect(self.refreshAnswerDisp)
        # self.answerEditor.setPlainText(self.answerstr)

        btnInsertImg.clicked.connect(self.insertImg)
        btnInsertImg2.clicked.connect(self.insertImg2)

        layout.addWidget(lable1, 0, 0, Qt.AlignLeft)
        layout.addWidget(btnInsertImg, 0, 1, Qt.AlignLeft)
        layout.addWidget(lable2, 0, 2, Qt.AlignLeft)
        layout.addWidget(btnInsertImg2, 0, 3, Qt.AlignLeft)
        layout.addWidget(self.questionEditor, 1, 0, 1, 2)
        layout.addWidget(self.answerEditor, 1, 2, 1, 2)

        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(2, 10)
        self.quesEditorGroupBox.setLayout(layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dlg = QuesModifyDlg()
    sys.exit(dlg.exec_())
