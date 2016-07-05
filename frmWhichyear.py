from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

class WhichyearDlg(QDialog):
    def __init__(self, parent=None):
        super(WhichyearDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")

        self.db = QSqlDatabase.addDatabase("QSQLITE");
        self.db.setDatabaseName("myQuestion.db")
        if not self.db.open():
            QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % self.db.lastError().text())
            sys.exit(1)

        tabtitle = QLabel()
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("题目所属学年维护")
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
        self.WhichyearView = QTableView()
        self.WhichyearModel = QSqlTableModel(self.WhichyearView)
        self.WhichyearModel.setTable("yearstable")
        # self.WhichyearModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.WhichyearModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.WhichyearModel.select()
        self.WhichyearModel.setHeaderData(0, Qt.Horizontal, "题目所属学年")


        # for indx, iheader in enumerate(["categoryid", "QuesWhichyear"]):
        #     self.WhichyearModel.setHeaderData(indx+1, Qt.Horizontal, iheader)

        self.WhichyearView.setModel(self.WhichyearModel)
        # self.WhichyearView.setColumnHidden(0, True)
        # self.WhichyearView.show()
        self.WhichyearView.verticalHeader().setFixedWidth(30)
        self.WhichyearView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.WhichyearView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        self.WhichyearView.setStyleSheet("font-size:16px; ");
        self.WhichyearView.setSelectionMode(QAbstractItemView.SingleSelection)

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

        newusrbtn.clicked.connect(self.newWhichyear)
        savebtn.clicked.connect(self.saveWhichyear)
        revertbtn.clicked.connect(self.revertWhichyear)
        removebtn.clicked.connect(self.removeWhichyear)

        self.WhichyearView.doubleClicked.connect(self.dbclick)

        lst_layout = QVBoxLayout()
        lst_layout.addLayout(titleLayout)
        lst_layout.addWidget(self.WhichyearView)
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

    #######======= WhichyearModel ============###############
    def newWhichyear(self):
        row = self.WhichyearModel.rowCount()
        self.WhichyearModel.insertRow(row)

    def removeWhichyear(self):
        index = self.WhichyearView.currentIndex()
        # print(type(index.sibling(index.row(),0).data()) == QPyNullVariant)
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return

        row = index.row()
        curWhichyearname =  index.sibling(index.row(),0).data()
        strwhere = "whichyear like '" + curWhichyearname + "'"
        self.QuestionModel.setFilter(strwhere)
        self.QuestionModel.select()

        # print(self.QuestionModel.rowCount(), "----", )
        if QMessageBox.question(self, "删除确认", "删除该条目意味着删除所有该学年的题目。是否要删除当前选中记录？", "确定", "取消") == 0:
            self.WhichyearModel.removeRows(row, 1)
            self.WhichyearModel.submitAll()
            self.WhichyearModel.database().commit()

            self.QuestionModel.removeRows(0, self.QuestionModel.rowCount())
            self.QuestionModel.submitAll()
            self.QuestionModel.database().commit()

    def revertWhichyear(self):
        self.WhichyearModel.revertAll()
        self.WhichyearModel.database().rollback()

    def saveWhichyear(self):
        # Update the Whichyear Table
        self.WhichyearModel.database().transaction()
        if self.WhichyearModel.submitAll():
            self.WhichyearModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查学年名称，不能出现同名学年！")
            self.WhichyearModel.revertAll()
            self.WhichyearModel.database().rollback()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=WhichyearDlg()
    dialog.show()
    app.exec_()
