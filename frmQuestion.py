from resources import *

class QuestionDlg(QDialog):
    # 自定义信号
    # jumpNewQuestion = pyqtSignal()
    jumpModifyQuestion = pyqtSignal(str, str)

    def __init__(self, parent=None, db="", curuser=""):
        super(QuestionDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.createQuestionInfo()

        tabtitle = QLabel()
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("题目列表")
        tabtitle.setStyleSheet("border: 1px solid blue; color:rgba(0,0,255, 220);\
            background-color:rgba(201,201,201,60);\
            border-radius: 6px; \
            padding: 1px 18px 1px 20px;\
            min-width: 8em;")
        tabtitle.setMinimumHeight(50);
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(tabtitle)
        titleLayout.setAlignment(tabtitle, Qt.AlignCenter)

        self.QuestionView = QTableView()
        self.QuestionModel = QSqlTableModel(self.QuestionView)
        self.QuestionModel.setTable("questiontable")

        self.QuestionModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.QuestionModel.select()

        for indx, iheader in enumerate(["题目", "答案", "类别", "题型", "年度", "备注"]):
            self.QuestionModel.setHeaderData(indx, Qt.Horizontal, iheader)

        self.QuestionView.setModel(self.QuestionModel)
        self.QuestionView.setColumnWidth(0, 600)
        self.QuestionView.setColumnWidth(1, 400)
        self.QuestionView.setColumnWidth(2, 100)
        self.QuestionView.setColumnWidth(3, 100)
        self.QuestionView.setColumnWidth(4, 100)
        self.updateList()

        # self.QuestionView.setColumnHidden(0, True)
        # self.QuestionView.show()
        self.QuestionView.verticalHeader().setFixedWidth(30)
        self.QuestionView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.QuestionView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        self.QuestionView.setStyleSheet("font-size:16px; ");
        self.QuestionView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.createQuestionDisp()

        btn_layout = QHBoxLayout()
        newusrbtn       = QPushButton("新增")
        modifybtn       = QPushButton("修改")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        exportBtn       = QPushButton("导出至Word文档...")

        btn_layout.addStretch(10)
        btn_layout.addWidget(newusrbtn)
        btn_layout.addWidget(modifybtn)
        btn_layout.addWidget(savebtn)
        btn_layout.addWidget(revertbtn)
        btn_layout.addWidget(removebtn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(exportBtn)

        newusrbtn.clicked.connect(self.newQuestion)
        modifybtn.clicked.connect(self.modifyQuestion)
        savebtn.clicked.connect(self.saveQuestion)
        revertbtn.clicked.connect(self.revertQuestion)
        removebtn.clicked.connect(self.removeQuestion)
        exportBtn.clicked.connect(self.exportWord)

        self.QuestionView.doubleClicked.connect(self.dbclick)
        self.QuestionView.clicked.connect(self.viewclick)
        self.QuestionView.selectionModel().currentChanged.connect(self.viewDataCursorChanged)
        # self.connect(self.QuestionView.selectionModel(), \
        #     SIGNAL("currentChanged(QModelIndex, QModelIndex)"), \
        #     SLOT(self.viewDataCursorChanged(QModelIndex, QModelIndex)))
        # self.QuestionView.currentChanged.connect(self.viewDataCursorChanged)

        lst_layout = QVBoxLayout()
        lst_layout.addWidget(self.quesInfoGroupBox)
        lst_layout.addWidget(self.QuestionView)
        lst_layout.addWidget(self.quesDispGroupBox)
        lst_layout.addLayout(btn_layout)
        # lst_layout.setStretch(0, 1)
        lst_layout.setStretch(1, 10)
        lst_layout.setStretch(2, 1)
        # lst_layout.setStretch(3, 1)

        self.setLayout(lst_layout)

    def exportWord(self):
        # print(self.QuestionModel.record(0))
        # print(self.QuestionModel.record(0).value(0))
        # print(self.QuestionModel.record(1).value(2))
        # print(self.QuestionModel.rowCount())

        while self.QuestionModel.canFetchMore():
            self.QuestionModel.fetchMore()

        # print(self.QuestionModel.rowCount())

        dictQuesInfo = {}
        for indx in range(0, self.QuestionModel.rowCount()):
            quesstr     = self.QuestionModel.record(indx).value(0)
            answstr     = self.QuestionModel.record(indx).value(1)
            classstr    = self.QuestionModel.record(indx).value(2)
            typestr     = self.QuestionModel.record(indx).value(3)
            yearstr     = self.QuestionModel.record(indx).value(4)
            demostr     = self.QuestionModel.record(indx).value(5)
            # tmplst = [quesstr, answstr, classstr, typestr, yearstr]
            tmplst = [quesstr, answstr]

            if typestr not in list(dictQuesInfo.keys()):
                dictQuesInfo[typestr] = []
            dictQuesInfo[typestr].append(tmplst)
            print(tmplst)

        for item in dictQuesInfo:
            print(item, dictQuesInfo[item])

    def viewDataCursorChanged(self, curindx, preindx):
        questionhtml = curindx.sibling(curindx.row(),0).data()
        answerhtml = curindx.sibling(curindx.row(),1).data()
        if questionhtml is None:
            questionhtml = ""
        if answerhtml is None:
            answerhtml = ""        
        self.questionDisp.setHtmlString(questionhtml)
        self.answerDisp.setHtmlString(answerhtml)
        

    def viewclick(self, indx):
        # print(indx.data())
        questionhtml = indx.sibling(indx.row(),0).data()
        answerhtml   = indx.sibling(indx.row(),1).data()
        self.questionDisp.setHtmlString(questionhtml)
        self.answerDisp.setHtmlString(answerhtml)

        # print("viewclick")

    def createQuestionDisp(self):
        self.quesDispGroupBox = QGroupBox("题目预览")
        layout = QHBoxLayout()

        self.questionDisp = myqwebview()
        self.questionDisp.setFixedHeight(100)
        self.questionDisp.setHtmlString("")
        self.answerDisp = myqwebview()
        self.answerDisp.setFixedHeight(100)
        self.answerDisp.setHtmlString("")

        layout.addWidget(self.questionDisp)
        layout.addWidget(self.answerDisp)

        # layout.setColumnStretch(0, 10)
        # layout.setColumnStretch(1, 10)
        # layout.setRowMinimumHeight(0, 40)
        # layout.setRowMinimumHeight(1, 40)
        self.quesDispGroupBox.setLayout(layout)

    def updateList(self):
        self.QuestionView.setItemDelegateForColumn(2, ComboBoxDelegate(self, self.selectComboxItems("select category  from categorytable")))
        self.QuestionView.setItemDelegateForColumn(3, ComboBoxDelegate(self, self.selectComboxItems("select questiontype  from questypetable")))
        self.QuestionView.setItemDelegateForColumn(4, ComboBoxDelegate(self, self.selectComboxItems("select whichyear  from yearstable")))

    def selectComboxItems(self, sqlstr):
        query = QSqlQuery(self.db)
        ret= query.exec_(sqlstr)
        lstitems = []
        while query.next():
            lstitems.append(query.value(0))
        return lstitems

    def createQuestionInfo(self):
        self.quesInfoGroupBox = QGroupBox("题目属性")
        layout = QHBoxLayout()
        layout.setMargin(10)
        layout.setAlignment(Qt.AlignHCenter)

        layout.addStretch(10)
        label1 = QLabel("类别")
        self.quesCategoryCombox = QComboBox()
        lstitems = self.selectComboxItems("select category  from categorytable")
        self.quesCategoryCombox.addItems(lstitems)
        self.quesCategoryCombox.insertItem(0, "")
        self.quesCategoryCombox.setCurrentIndex(0)
        layout.addWidget(label1)
        layout.addWidget(self.quesCategoryCombox)

        layout.addStretch(10)
        label2 = QLabel("题型")
        self.quesTypeCombox = QComboBox()
        lstitems = self.selectComboxItems("select questiontype  from questypetable")
        self.quesTypeCombox.addItems(lstitems)
        self.quesTypeCombox.insertItem(0, "")
        self.quesTypeCombox.setCurrentIndex(0)
        layout.addWidget(label2)
        layout.addWidget(self.quesTypeCombox)

        layout.addStretch(10)
        label3 = QLabel("年份")
        self.quesWhichyearCombox = QComboBox()
        lstitems = self.selectComboxItems("select whichyear  from yearstable")
        self.quesWhichyearCombox.addItems(lstitems)
        self.quesWhichyearCombox.insertItem(0, "")
        self.quesWhichyearCombox.setCurrentIndex(0)
        layout.addWidget(label3)
        layout.addWidget(self.quesWhichyearCombox)

        layout.addStretch(10)
        label4 = QLabel("关键字")
        self.selectText = QLineEdit()
        layout.addWidget(label4)
        layout.addWidget(self.selectText)

        layout.addStretch(10)
        btnSelect = QPushButton("查询")
        layout.addWidget(btnSelect)
        layout.addStretch(10)

        btnSelect.clicked.connect(self.selectQuestion)
        self.quesInfoGroupBox.setLayout(layout)

    def selectQuestion(self):
        quesCategory    = self.quesCategoryCombox.currentText()
        quesType        = self.quesTypeCombox.currentText()
        quesWhichyear   = self.quesWhichyearCombox.currentText()
        selectText      = self.selectText.text()
        strwhere = "1=1"
        if quesCategory != "":
            strwhere += " and category like '%s'" % quesCategory
        if quesType != "":
            strwhere += " and questiontype like '%s'" % quesType
        if quesWhichyear != "":
            strwhere += " and whichyear like '%s'" % quesWhichyear
        strwhere += " and questionhtml like '%" + selectText + "%'"

        # print(strwhere)
        self.QuestionModel.setFilter(strwhere)
        self.QuestionModel.select()

    def dbclick(self, indx):
        if indx.column() == 0 or indx.column() == 1:
            self.QuestionView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.modifyQuestion()
        else:
            self.QuestionView.setEditTriggers(QAbstractItemView.DoubleClicked)

    #######======= QuestionModel ============###############

    def modifyQuestion(self):
        index = self.QuestionView.currentIndex()
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return
        if index.sibling(index.row(),0).data().strip() == "":
            return

        questionstr = index.sibling(index.row(),0).data()
        answerstr   = index.sibling(index.row(),1).data()

        self.jumpModifyQuestion.emit(questionstr, answerstr)

    def newQuestion(self):
        # index = self.QuestionView.currentIndex()
        # print(self.QuestionView.record())
        # print(index.data())
        # print(index.sibling(1,0).data())

        self.jumpModifyQuestion.emit("", "")

        # Items = self.QuestionModel.match(self.QuestionModel.index(2,1),
        #     Qt.DisplayRole,
        #     "ssd",
        #     -1,
        #     Qt.MatchStartsWith )

        # for i1 in Items:
        #     print(i1.sibling(0,0).data())
        #     print(i1.sibling(1,0).data())
            # print(i1.sibling(2,0).data())
        # print(Items[0].sibling(0,1).data())
        # Items = model->match(
        #     model->index(0, 0),
        #     Qt::DisplayRole,
        #     QVariant::fromValue(item),
        #     2, // look *
        #     Qt::MatchRecursive);

    def removeQuestion(self):
        index = self.QuestionView.currentIndex()
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return

        if QMessageBox.question(self, "删除确认", "是否要删除当前选中题目？", "确定", "取消") == 0:
            self.QuestionModel.removeRows(index.row(), 1)
            self.QuestionModel.submitAll()
            self.QuestionModel.database().commit()

    def revertQuestion(self):
        self.QuestionModel.revertAll()
        self.QuestionModel.database().rollback()

    def saveQuestion(self):
        self.QuestionModel.database().transaction()
        if self.QuestionModel.submitAll():
            self.QuestionModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查是否出现同名题目！")
            self.QuestionModel.revertAll()
            self.QuestionModel.database().rollback()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()
