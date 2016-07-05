from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

class CategoryDlg(QDialog):
    def __init__(self, parent=None):
        super(CategoryDlg,self).__init__(parent)
        # self.setStyleSheet("background-image:url('image/panelbg.jpg'); border: 2px; border-radius 2px;")
        
        self.db = QSqlDatabase.addDatabase("QSQLITE");  
        self.db.setDatabaseName("myQuestion.db")
        if not self.db.open():
            QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % self.db.lastError().text())
            sys.exit(1)

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
        self.QuesCategoryModel.setHeaderData(0, Qt.Horizontal, "序号")
        self.QuesCategoryModel.setHeaderData(1, Qt.Horizontal, "类别名称")
        

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
        if type(indx.sibling(indx.row(),1).data()) != QPyNullVariant:
            category = indx.sibling(indx.row(),1).data()
            
            strwhere = "category like '" + category + "'"
            self.QuestionModel.setFilter(strwhere)
            self.QuestionModel.setSort(2, Qt.AscendingOrder)
            self.QuestionModel.select()
            
            # self.g_curcategory = category
            # self.tabWidget.setTabText(0, self.g_curcategory)

    #######======= CategoryModel ============###############
    def newCategory(self):
        row = self.QuesCategoryModel.rowCount()
        self.QuesCategoryModel.insertRow(row)

    def removeCategory(self):
        index = self.QuesCategoryView.currentIndex()        
        if type(index.sibling(index.row(),1).data()) == type(None):            
            return        
        if len(index.sibling(index.row(),1).data()) == 0:            
            return
            
        row = index.row()   
        curCategoryname =  index.sibling(index.row(),1).data()
        strwhere = "Categoryname like '" + curCategoryname + "'"
        self.QuestionModel.setFilter(strwhere)
        self.QuestionModel.select()

        # print(self.QuestionModel.rowCount(), "----", )
        if QMessageBox.question(self, "删除确认", "删除班级意味着会删除本班所有人员信息。是否要删除当前选中记录？", "确定", "取消") == 0:
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
        query = QSqlQuery(self.db)

        # record the old Category name
        lstOldCategoryName = {}
        lstOldCategoryid = []
        query.exec_("select rowid, Categoryname from Categorytable" )        
        while(query.next()):
            lstOldCategoryName[query.value(0)] = query.value(1)
            lstOldCategoryid.append(query.value(0))
        # print(lstOldCategoryName)

        # Update the Category Table
        self.QuesCategoryModel.database().transaction()
        if self.QuesCategoryModel.submitAll():
            self.QuesCategoryModel.database().commit()
            # print("save success!  ->commit")
        else:
            QMessageBox.warning(None, "错误",  "请检查班级中名称，不能出现同名班级！")
            self.QuesCategoryModel.revertAll()
            self.QuesCategoryModel.database().rollback()

        # print(lstOldCategoryid)

        lstNewCategoryName = {}
        query.exec_("select rowid, Categoryname from Categorytable where rowid in " + str(tuple(lstOldCategoryid)) )        
        while(query.next()):
            lstNewCategoryName[query.value(0)] = query.value(1)            

        # print(lstOldCategoryName, '=========')
        # print(lstNewCategoryName, '~~~~~~~~~')

        for i in lstOldCategoryName:
            oldCategoryname = lstOldCategoryName[i]
            newCategoryname = lstNewCategoryName[i]
            if oldCategoryname != newCategoryname:
                # print(oldCategoryname, newCategoryname, '++++++++')
                # print("update student set Categoryname=" + newCategoryname + " where Categoryname='" + oldCategoryname + "'")
                query.exec_("update student set Categoryname='" + newCategoryname + "' where Categoryname='" + oldCategoryname + "'")
                self.QuestionModel.setFilter("Categoryname = '" + newCategoryname + "'")
                self.QuestionModel.select()

        lstCategoryName = []      
        query.exec_("select Categoryname from Categorytable" ) 
        while(query.next()):
            lstCategoryName.append(query.value(0))
        # self.QuestionView.setItemDelegateForColumn(1,  ComboBoxDelegate(self, lstCategoryName, self.db, newCategoryname))


if __name__ == "__main__":    
    import sys
    app=QApplication(sys.argv)
    dialog=CategoryDlg()
    dialog.show()
    app.exec_()