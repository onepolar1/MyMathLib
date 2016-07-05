from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

class QuesTypeDlg(QDialog):
    def __init__(self, parent=None):
        super(QuesTypeDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")

        self.db = QSqlDatabase.addDatabase("QSQLITE");
        self.db.setDatabaseName("myQuestion.db")
        if not self.db.open():
            QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % self.db.lastError().text())
            sys.exit(1)

        tabtitle = QLabel()
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("题目类型信息维护")
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

        # Create the question category View
        self.QuestionTypeView = QTableView()
        self.QuestionTypeModel = QSqlTableModel(self.QuestionTypeView)
        self.QuestionTypeModel.setTable("questypetable")
        # self.QuestionTypeModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.QuestionTypeModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.QuestionTypeModel.select()
        self.QuestionTypeModel.setHeaderData(0, Qt.Horizontal, "题目类型名称")


        # for indx, iheader in enumerate(["categoryid", "QuesQuesType"]):
        #     self.QuestionTypeModel.setHeaderData(indx+1, Qt.Horizontal, iheader)

        self.QuestionTypeView.setModel(self.QuestionTypeModel)
        # self.QuestionTypeView.setColumnHidden(0, True)
        # self.QuestionTypeView.show()
        self.QuestionTypeView.verticalHeader().setFixedWidth(30)
        self.QuestionTypeView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.QuestionTypeView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        self.QuestionTypeView.setStyleSheet("font-size:16px; ");
        self.QuestionTypeView.setSelectionMode(QAbstractItemView.SingleSelection)

        btn_layout = QHBoxLayout()
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")

        btn_layout.addStretch(10)
        btn_layout.addWidget(newusrbtn)
        btn_layout.addWidget(savebtn)
        btn_layout.addWidget(revertbtn)
        btn_layout.addWidget(removebtn)

        newusrbtn.clicked.connect(self.newQuesType)
        savebtn.clicked.connect(self.saveQuesType)
        revertbtn.clicked.connect(self.revertQuesType)
        removebtn.clicked.connect(self.removeQuesType)

        self.QuestionTypeView.doubleClicked.connect(self.dbclick)

        lst_layout = QVBoxLayout()
        lst_layout.addLayout(titleLayout)
        lst_layout.addWidget(self.QuestionTypeView)
        lst_layout.addLayout(btn_layout)

        self.setLayout(lst_layout)

    def dbclick(self, indx):
        pass
        # if type(indx.sibling(indx.row(),1).data()) != QPyNullVariant:
        #     category = indx.sibling(indx.row(),1).data()
        #
        #     strwhere = "category like '" + category + "'"
        #     self.QuestionModel.setFilter(strwhere)
        #     self.QuestionModel.setSort(2, Qt.AscendingOrder)
        #     self.QuestionModel.select()

            # self.g_curcategory = category
            # self.tabWidget.setTabText(0, self.g_curcategory)

    #######======= QuesTypeModel ============###############
    def newQuesType(self):
        row = self.QuestionTypeModel.rowCount()
        self.QuestionTypeModel.insertRow(row)

    def removeQuesType(self):
        index = self.QuestionTypeView.currentIndex()
        # print(type(index.sibling(index.row(),0).data()) == QPyNullVariant)
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return

        row = index.row()
        curQuesTypename =  index.sibling(index.row(),0).data()
        strwhere = "questiontype like '" + curQuesTypename + "'"
        self.QuestionModel.setFilter(strwhere)
        self.QuestionModel.select()

        # print(self.QuestionModel.rowCount(), "----", )
        if QMessageBox.question(self, "删除确认", "删除题目类型意味着删除所有该类型题目。是否要删除当前选中记录？", "确定", "取消") == 0:
            self.QuestionTypeModel.removeRows(row, 1)
            self.QuestionTypeModel.submitAll()
            self.QuestionTypeModel.database().commit()

            self.QuestionModel.removeRows(0, self.QuestionModel.rowCount())
            self.QuestionModel.submitAll()
            self.QuestionModel.database().commit()

    def revertQuesType(self):
        self.QuestionTypeModel.revertAll()
        self.QuestionTypeModel.database().rollback()

    def saveQuesType(self):
        # Update the QuesType Table
        self.QuestionTypeModel.database().transaction()
        if self.QuestionTypeModel.submitAll():
            self.QuestionTypeModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查题型名称，不能出现同名题型！")
            self.QuestionTypeModel.revertAll()
            self.QuestionTypeModel.database().rollback()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuesTypeDlg()
    dialog.show()
    app.exec_()
