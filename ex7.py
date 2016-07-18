from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class BrowserScreen(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.baseUrl = QUrl.fromLocalFile(QDir.current().absoluteFilePath("dummy.html"));

        self.resize(800, 600)
        self.show()
        self.htmlheadstr = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>MathJax TeX to MathML Page</title>
            <meta charset="UTF-8">            
            <script type="text/x-mathjax-config">
              MathJax.Hub.Config({
                tex2jax: {inlineMath: [["$","$"],["\\(","\\)"]]}
              }); 
              MathJax.Hub.Config({
                  SVG: {
                    scale: 180
                  }
                }); 
            </script>

            <script type="text/javascript" src="MathJax2.6/MathJax.js?config=TeX-AMS-MML_SVG"></script>
            </head>
            <body>
        """
        self.htmlendstr = """</body>
                            </html>"""

        self.setHtml(self.htmlheadstr + """
           <script>function message() { return "Clicked!"; }</script>
           <h1>QtWebKit + Python sample program</h1>
           <input type="button" value="TheFirstClickPy!"
                  onClick="alert('[javascript] ' + message())"/>
           <input type="button" value="Click Python!"
                  onClick="python.alert('[python] ' +
                                        python.message())"/>
           <br />
           
           <script>
              function messageCESHI() {  
                alert("haha")
                var jax = MathJax.Hub.getAllJax();  
                alert(jax.length)
                //var arr = new Array()
                for (var i = 0; i < jax.length; i++) {
                    alert(jax[i]);
                    alert(jax[i].root.toMathML(""))                    
                }
                //alert(arr)
                /**/
                return "Clicked!"; 

              }
            </script>      
            
            <input type="button" value="TheSecond!!!"
                              onClick="alert('[!!!!] ' + messageCESHI())"/>

            <p>当 $a < 0$ 时, 有两个解决方法 $ax^2 + bx + c = 0$ and  
            they are
            $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
            </p>

        """ + self.htmlendstr, self.baseUrl)

        self.setZoomFactor(1)
        self.createTrayIcon()
        self.trayIcon.show()

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
