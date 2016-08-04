#!/usr/bin/env python
# from myimport import *
from resources import *

from frmModify import QuesModifyDlg
from frmCategory import CategoryDlg
from frmQuestion import QuestionDlg
from frmQuesType import QuesTypeDlg
from frmWhichyear import WhichyearDlg

class MainWindow(QMainWindow):
    def __init__(self, db="", curuser = {}):
        super(MainWindow, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tabWidget=QTabWidget(self)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeMyTab)

        self.setCentralWidget(self.tabWidget)

        self.createActions()
        self.createMenus()

        message = "欢迎使用广东省育苗杯电子题库！"
        self.statusBar().showMessage(message)

        if self.curuser == {}:
            userInfoStr = "当前登录属于调试操作！"
        else:
            userInfoStr = "当前用户编码：%s，单位：%s，操作人员姓名：%s" % (self.curuser["unitsn"], self.curuser["unitname"], self.curuser["unitman"])
        self.userlabel = QLabel(userInfoStr)
        self.statusBar().addPermanentWidget(self.userlabel)

        # dispSystemInfo = QLabel("汕头市残联精防基金结算\n\n       业务系统", self)
        # dispSystemInfo.setGeometry(300,200,820,200)
        # dispSystemInfo.setStyleSheet("font-size:60px; color:blue;font-weight:bold;")
        # self.setStyleSheet("background-color:red;")

        self.setWindowIcon(QIcon("images/login.png"))
        self.setWindowTitle("广东省育苗杯电子题库")
        self.setMinimumSize(480,320)
        self.showMaximized()
        # self.resize(720,600)

        self.setStyleSheet("font-size:14px;")

        # self.createDb()

    def closeEvent(self, event):
        # pass
        # print(1)
        # print(self.tabWidget.count())
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == "新增/修改题目":
                self.closeMyTab(tabindx)
        self.db.close()
        # QSqlDatabase.removeDatabase(self.db.connectionName())
        # print(2)

    def closeMyTab(self, tabindx):
        if self.tabWidget.tabText(tabindx) == "新增/修改题目":            
            widget = self.tabWidget.widget(tabindx)

            if widget.flag_IsChanged == 0: #不保存
                widget.removeNotUseImgs()
            else:
                if QMessageBox.question(self, "确认", "是否要新增/修改已有题目？", "确定", "取消") == 0:
                    widget.saveQuestion()
                else:
                    widget.removeNotUseImgs()
        self.tabWidget.removeTab (tabindx)

    def modifyPwd(self):
        QMessageBox.warning(self, "提示", "待添加")

        # dialog=frmPwd(self, db=self.db, curuser=self.curuser)
        # # dialog.show()
        # # dialog.accepted.connect(self.resetMain)
        # # self.connect(dialog, SIGNAL("accepted"), self.refreshTable)
        # dialog.show()
        # if dialog.exec_() == QDialog.Accepted:
        #     self.close()
        #     # print(1)
        #     # print(dialog.mmm)

    def userManage(self):
        QMessageBox.warning(self, "提示", "待添加")

        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联":
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        # curTabText = "用户管理"
        # for tabindx in list(range(0, self.tabWidget.count())):
        #     if self.tabWidget.tabText(tabindx) == curTabText:
        #         self.tabWidget.setCurrentIndex(tabindx)
        #         return

        # widget = UserDlg(db=self.db)
        # self.tabWidget.addTab(widget,curTabText)
        # self.tabWidget.setCurrentWidget(widget)

    def QuestionManage(self):
        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "区残联":
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        curTabText = "题库查询浏览"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = QuestionDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)
        widget.jumpModifyQuestion.connect(self.questionModify)

    @pyqtSlot(str, str)
    def questionModify(self, questionstr="", answerstr=""):
        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "区残联":
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        curTabText = "新增/修改题目"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                self.tabWidget.currentWidget().setQuestionAndAnswerstr(questionstr, answerstr)
                return

        widget = QuesModifyDlg(db=self.db, curuser=self.curuser, questionstr=questionstr, answerstr=answerstr)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    def quesTypeManage(self):
        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联" :
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        curTabText = "题型维护"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = QuesTypeDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    def QuesCategoryManage(self):
        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联" :
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        curTabText = "题目类别管理"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = CategoryDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    def quesWhichyearManage(self):
        # if self.curuser != {}:
        #     if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "医院" :
        #         QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
        #         return

        curTabText = "试题年份"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = WhichyearDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)


    def about(self):
        QMessageBox.about(self, "关于...",
                "本程序为广东省育苗杯电子题库! \n\n%s \n\n%s " % (CUR_VERSION, CUR_CONTACT))

    def aboutQt(self):
        pass

    def QuestionImport(self):
        filedialog = QFileDialog()
        fileName = filedialog.getOpenFileName(self,  "打开excel题目文件", QDir.homePath (), "excel文件 (*.xls *.xlsx)")
        if fileName != "":            
            book = xlrd.open_workbook(fileName)
            sh = book.sheet_by_index(0)
            
            lsthead = ["序号","题目","答案","分类","题目类型","年份","备注"]
            for indx, ihead in enumerate(lsthead):
                if sh.row(0)[indx].value != ihead:
                    QMessageBox.warning(self, "提示", "请将所导入的excel文件第一行标题按照\n\n" + "-".join(lsthead) + "\n\n的方式排列!")
                    return

            query = QSqlQuery(self.db)
            for indx in range(1, sh.nrows):
                questionstr         = sh.row(indx)[1].value
                answerstr           = sh.row(indx)[2].value
                quescategorystr     = sh.row(indx)[3].value
                questypestr         = sh.row(indx)[4].value
                queswhichyearstr    = sh.row(indx)[5].value
                quesdemostr         = sh.row(indx)[6].value

                query.prepare("insert into questiontable \
                    (questionhtml, answerhtml, category, questiontype, whichyear, demo) \
                    values (:questionhtml, :answerhtml, :category, :questiontype, :whichyear, :demo)")
                query.bindValue(":questionhtml", questionstr)
                query.bindValue(":answerhtml", answerstr)
                query.bindValue(":category", quescategorystr)
                query.bindValue(":questiontype", questypestr)
                query.bindValue(":whichyear", queswhichyearstr)
                query.bindValue(":demo", quesdemostr)
                query.exec_()

            QMessageBox.information(self, "提示", "导入成功!")
                
                # print([questionstr,answerstr,quescategorystr,questypestr,queswhichyearstr,quesdemostr])
                
    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def createActions(self):
        self.userAct            = self.createAction("用户管理(&U)", self.userManage,   "", "", "用户管理")
        self.modifyPwdAct       = self.createAction("修改密码", self.modifyPwd,   "", "", "修改用户密码")
        self.exitAct        = self.createAction("退出(&X)", self.close,   "Ctrl+Q", "", "退出系统")

        self.questionAct        = self.createAction("题库(&M)", self.QuestionManage,   "", "", "所有题目列表")
        self.quesmodifyAct      = self.createAction("添加题目(&A)", self.questionModify,   "", "", "新增加题目")
        self.quesImportAct      = self.createAction("导入...(&I)", self.QuestionImport,   "", "", "从excel表格导入题目")

        self.quesCategoryAct    = self.createAction("题目分类(&C)", self.QuesCategoryManage,   "", "", "题目分类")
        self.quesTypeAct        = self.createAction("题型维护(&T)", self.quesTypeManage,   "", "", "题型维护")
        self.quesWhichyearAct   = self.createAction("试题年份(&W)", self.quesWhichyearManage,   "", "", "试题年份")

        self.aboutAct       = self.createAction("关于(&A)", self.about,   "", "", "显示当前系统的基本信息")
        self.aboutQtAct     = self.createAction("关于Qt(&Q)", self.aboutQt,   "", "", "显示Qt库的基本信息")
        self.aboutQtAct.triggered.connect(qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("系统管理(&S)")
        self.fileMenu.addAction(self.userAct)
        self.fileMenu.addAction(self.modifyPwdAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("题库总览(&F)")
        self.editMenu.addAction(self.questionAct)
        self.editMenu.addAction(self.quesmodifyAct)
        self.editMenu.addAction(self.quesImportAct)

        self.approvalMenu = self.menuBar().addMenu("分类信息(&A)")
        self.approvalMenu.addAction(self.quesCategoryAct)
        self.approvalMenu.addAction(self.quesTypeAct)
        self.approvalMenu.addAction(self.quesWhichyearAct)

        self.helpMenu = self.menuBar().addMenu("关于(&H)")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('cleanlooks'))
    window = MainWindow()
    # app.lastWindowClosed.connect(window.closeWindow())
    window.show()
sys.exit(app.exec_())
