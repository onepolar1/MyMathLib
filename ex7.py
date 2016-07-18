#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import os
import platform

userhome = os.path.expanduser('~')
desktop = userhome + os.path.sep +  'Desktop' + os.path.sep

class htmlViewer(QWebView):
    def __init__(self,url, parent=None):
        QWebView.__init__(self,parent)

        self.baseUrl = QUrl.fromLocalFile(QDir.current().absoluteFilePath("dummy.html"));

        self.htmlStr1 = """
            <!DOCTYPE html>
                <html>
                <head>
                <title>MathJax TeX to MathML Page</title>
                <script>
                function toMathML(jax,callback) {
                  var mml;
                  try {
                    mml = jax.root.toMathML("");
                  } catch(err) {
                    if (!err.restart) {throw err} // an actual error
                    return MathJax.Callback.After([toMathML,jax,callback],err.restart);
                  }
                  MathJax.Callback(callback)(mml);
                }
                </script>
                <script type="text/x-mathjax-config">
                  MathJax.Hub.Config({
                    tex2jax: {inlineMath: [["$","$"],["\\(","\\)"]]}
                  });
                  MathJax.Hub.Queue(
                    function () {
                      var jax = MathJax.Hub.getAllJax();
                      for (var i = 0; i < jax.length; i++) {
                        toMathML(jax[i],function (mml) {
                          alert(jax[i].originalText + "\n\n=>\n\n"+ mml);
                        });
                      }
                    }
                  );
                </script>
                <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full
                "></script>
                </head>
            <body>
            """
        self.htmlStr2 = """
            </body>
            </html>
            """

        tmpstr =  """
            <p>
            当 $a \ne 0$ 时, 有两个解决方法 \(ax^2 + bx + c = 0\) and  
            they are
            $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
            </p>
            
            <p>hello <strong>world</strong></p>
            <p>$x+y=z \pi$</p>
            <p>$a \div b = z^2$</p>
            <p>$\\frac{2}{3}=5$</p>
            <p>$$\\frac{2}{3}=5$$</p>
            <p>欧拉公式：Euler's identity, <mathjax>$e^{i\pi} = -1$</mathjax>, is widely considered the most beautiful theorem in
            mathematics.</p>
            <img src="images/trash.png" alt="Smiley face" width="100" height="100" align="right">
            """

        self.setHtml(self.htmlStr1 + tmpstr + self.htmlStr2, self.baseUrl)
        # self.setHtml(svgExStr)
        self.setZoomFactor(1)

        
    def genPdf(self):
        self.printer.setOutputFileName("printYou.pdf")
        # self.loadFinished.connect(self.execpreview)

    # def genUrl(self):
    #     pageSource = """<html><head>

    #     <script type="text/javascript" async src="MathJax2.6/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    #     </head><body>
    #     <p><mathjax>$$
    #     \imath x+y=z
    #     \pi \\\\
    #     \\frac{1}{3}
    #     $$</mathjax></p>
    #     </body></html>"""

    #     tempFile = QFile('mathjax_ex.html')
    #     tempFile.open(QFile.WriteOnly)
    #     stream = QTextStream(tempFile)
    #     stream << pageSource
    #     tempFile.close()
    #     fileUrl = QUrl.fromLocalFile(QFileInfo(tempFile).canonicalFilePath())
    #     return fileUrl
    

class QuestionDlg(QDialog):
    def __init__(self, parent=None, db="", curuser=""):
        super(QuestionDlg,self).__init__(parent)

        self.resize(800, 600)

        titleLayout = QHBoxLayout()
        self.questionDisp = htmlViewer("")
        btn = QPushButton("打印")
        titleLayout.addWidget(self.questionDisp)
        titleLayout.addWidget(btn)
        btn.clicked.connect(self.printview)

        self.setLayout(titleLayout)

    def printview(self):
        # self.questionDisp.genPdf()
        print("hello")



if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()
