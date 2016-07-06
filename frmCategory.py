#!/usr/bin/env python
from resources import *

class CategoryDlg(QDialog):
    def __init__(self, parent=None, db="", curuser=""):
        super(CategoryDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")

        if db == "":
            self.db = globaldb()
        else:
            self.db = db 

        tabtitle = QLabel()
        tabtitle.setFont(QFont('Courier New', 20))
        tabtitle.setText("题目类别信息维护")
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
        self.QuesCategoryView = QTableView()
        self.QuesCategoryModel = QSqlTableModel(self.QuesCategoryView)
        self.QuesCategoryModel.setTable("categorytable")
        # self.QuesCategoryModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.QuesCategoryModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.QuesCategoryModel.select()
        self.QuesCategoryModel.setHeaderData(0, Qt.Horizontal, "题目类别名称")


        # for indx, iheader in enumerate(["categoryid", "QuesCategory"]):
        #     self.QuesCategoryModel.setHeaderData(indx+1, Qt.Horizontal, iheader)

        self.QuesCategoryView.setModel(self.QuesCategoryModel)
        # self.QuesCategoryView.setColumnHidden(0, True)
        # self.QuesCategoryView.show()
        self.QuesCategoryView.verticalHeader().setFixedWidth(30)
        self.QuesCategoryView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.QuesCategoryView.setStyleSheet("QTableView{background-color: rgb(250, 250, 200, 0);"
                    "alternate-background-color: rgb(141, 163, 0);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        self.QuesCategoryView.setStyleSheet("font-size:16px; ");
        self.QuesCategoryView.setSelectionMode(QAbstractItemView.SingleSelection)

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

        newusrbtn.clicked.connect(self.newCategory)
        savebtn.clicked.connect(self.saveCategory)
        revertbtn.clicked.connect(self.revertCategory)
        removebtn.clicked.connect(self.removeCategory)

        self.QuesCategoryView.doubleClicked.connect(self.dbclick)

        lst_layout = QVBoxLayout()
        lst_layout.addLayout(titleLayout)
        lst_layout.addWidget(self.QuesCategoryView)
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

    #######======= CategoryModel ============###############
    def newCategory(self):
        row = self.QuesCategoryModel.rowCount()
        self.QuesCategoryModel.insertRow(row)

    def removeCategory(self):
        index = self.QuesCategoryView.currentIndex()
        # print(type(index.sibling(index.row(),0).data()) == QPyNullVariant)
        if type(index.sibling(index.row(),0).data()) == type(None):
            return
        if type(index.sibling(index.row(),0).data()) == QPyNullVariant:
            return

        row = index.row()
        curCategoryname =  index.sibling(index.row(),0).data()
        strwhere = "Categoryname like '" + curCategoryname + "'"
        self.QuestionModel.setFilter(strwhere)
        self.QuestionModel.select()

        # print(self.QuestionModel.rowCount(), "----", )
        if QMessageBox.question(self, "删除确认", "删除题目类别意味着删除所有该类别题目。是否要删除当前选中记录？", "确定", "取消") == 0:
            self.QuesCategoryModel.removeRows(row, 1)
            self.QuesCategoryModel.submitAll()
            self.QuesCategoryModel.database().commit()

            self.QuestionModel.removeRows(0, self.QuestionModel.rowCount())
            self.QuestionModel.submitAll()
            self.QuestionModel.database().commit()

    def revertCategory(self):
        self.QuesCategoryModel.revertAll()
        self.QuesCategoryModel.database().rollback()

    def saveCategory(self):
        # Update the Category Table
        self.QuesCategoryModel.database().transaction()
        if self.QuesCategoryModel.submitAll():
            self.QuesCategoryModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查类别名称，不能出现同名类别！")
            self.QuesCategoryModel.revertAll()
            self.QuesCategoryModel.database().rollback()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=CategoryDlg()
    dialog.show()
    app.exec_()
