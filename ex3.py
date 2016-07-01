from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class BrowserScreen(QWebView):
    def __init__(self):
        QWebView.__init__(self)

        baseUrl = QUrl.fromLocalFile(QDir.current().absoluteFilePath("dummy.html"));

        # self.resize(800, 600)
        myset = self.settings()
        # myset.setFontSize(QWebSettings.DefaultFontSize, 20)
        myset.setFontSize(QWebSettings.MinimumFontSize, 20)
        myset.setObjectCacheCapacities(0, 0, 0)

        self.setHtml("""
            <head>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
                });
            </script>
            <script type="text/javascript" async src="MathJax2.6/MathJax.js?config=TeX-MML-AM_HTMLorMML"></script>
            <style>
                p { color: #ff0000; }
                strong {color: #222233}
            </style>
            </head>

            <body>
            <p>hello <strong>world</strong></p>
            <p>$x+y=z \pi$</p>
            <p>$a \div b = z^2$</p>
            <p>$\\frac{2}{3}=5$</p>
            <p>$$\\frac{2}{3}=5$$</p>
            <p>欧拉公式：Euler's identity, <mathjax>$e^{i\pi} = -1$</mathjax>, is widely considered the most beautiful theorem in
            mathematics.</p>
            </body>
        """, baseUrl)

        self.show()

        # self.createTrayIcon()
        # self.trayIcon.show()

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("images/trash.png"))

    def showMessage(self, msg):
        self.trayIcon.showMessage("This is Python", msg,
            QSystemTrayIcon.MessageIcon(0), 15 * 1000)

class PythonJS(QObject):
    __pyqtSignals__ = ("contentChanged(const QString &)")
    @pyqtSignature("QString")
    def alert(self, msg):
        self.emit(SIGNAL('contentChanged(const QString &)'), msg)

    @pyqtSignature("", result="QString")
    def message(self):
        return "Click!"

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    browser = BrowserScreen()
    pjs = PythonJS()
    browser.page().mainFrame().addToJavaScriptWindowObject("python", pjs)
    QObject.connect(pjs, SIGNAL("contentChanged(const QString &)"),
                    browser.showMessage)

    sys.exit(app.exec_())
