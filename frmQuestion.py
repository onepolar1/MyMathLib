from resources import *

class QuestionDlg(QDialog):
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
        # self.QuestionView.setColumnHidden(0, True)
        # self.QuestionView.show()
        self.QuestionView.verticalHeader().setFixedWidth(30)
        self.QuestionView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.QuestionView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        self.QuestionView.setStyleSheet("font-size:16px; ");
        self.QuestionView.setSelectionMode(QAbstractItemView.SingleSelection)

        btn_layout = QHBoxLayout()
        newusrbtn       = QPushButton("新增")
        modifybtn       = QPushButton("修改")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")

        btn_layout.addStretch(10)
        btn_layout.addWidget(newusrbtn)
        btn_layout.addWidget(modifybtn)
        btn_layout.addWidget(savebtn)
        btn_layout.addWidget(revertbtn)
        btn_layout.addWidget(removebtn)

        newusrbtn.clicked.connect(self.newQuestion)
        modifybtn.clicked.connect(self.modifyQuestion)
        savebtn.clicked.connect(self.saveQuestion)
        revertbtn.clicked.connect(self.revertQuestion)
        removebtn.clicked.connect(self.removeQuestion)

        self.QuestionView.doubleClicked.connect(self.dbclick)

        lst_layout = QVBoxLayout()
        lst_layout.addWidget(self.quesInfoGroupBox)        
        lst_layout.addWidget(self.QuestionView)
        lst_layout.addLayout(btn_layout)

        self.setLayout(lst_layout)

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

        self.quesInfoGroupBox.setLayout(layout)

    def dbclick(self, indx):
        if indx.column() == 0 or indx.column() == 1:
            self.StudentView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.StudentView.setEditTriggers(QAbstractItemView.DoubleClicked)

    #######======= QuestionModel ============###############
    def newQuestion(self):
        pass
        
    def removeQuestion(self):
        index = self.QuestionView.currentIndex()
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return

        if QMessageBox.question(self, "删除确认", "是否要删除当前选中题目？", "确定", "取消") == 0:
            self.QuestionModel.removeRows(row, 1)
            self.QuestionModel.submitAll()
            self.QuestionModel.database().commit()

    def revertQuestion(self):
        self.QuestionModel.revertAll()
        self.QuestionModel.database().rollback()

    def modifyQuestion(self):
        pass
       
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