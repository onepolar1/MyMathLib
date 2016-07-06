from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4.QtWebKit import *
from myQwebview import myqwebview
import markdown
try: import mdx_mathjax
except: pass

mdProcessor = markdown.Markdown(extensions=['mathjax'])

CUR_VERSION = "广东省育苗杯电子题库\n版本：2016.0706.1.0"
CUR_CONTACT = "如有任何问题请联系：mybsppp@163.com\n\n程序开发：赵小娜\n2016"

def globaldb():
    db = QSqlDatabase.addDatabase("QSQLITE");
    db.setDatabaseName("myQuestion.db")
    if not db.open():
        QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % db.lastError().text())
        sys.exit(1)
    return db