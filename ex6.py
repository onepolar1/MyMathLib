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
            <html>
            <head>
            <script type="text/x-mathjax-config">
                MathJax.Hub.Config({
                    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
                });
            </script>
            <script type="text/javascript" src="MathJax2.6/MathJax.js?config=TeX-MML-AM_HTMLorMML"></script>
            <style>
                p { color: #00008B; font-weight: 900; font-family: verdana; line-height:100%}
                strong {color: #222233}
                body {background-color: #99caff}
                <img align="right">
            </style>
            </head>

            <body>
            """
        self.htmlStr2 = """
            </body>
            </html>
            """

        tmpstr =  """
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
        self.setZoomFactor(1)


        # self.setUrl(QUrl(url))
        self.printer = QPrinter(QPrinterInfo.defaultPrinter(),QPrinter.HighResolution)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setOrientation(QPrinter.Portrait)
        self.printer.setPaperSize(QPrinter.A4)
        self.printer.setFullPage(True)
        #self.printer.setResolution(72)
        filename = desktop + r"printYou.pdf"
        print(filename)

    def genPdf(self):
        self.printer.setOutputFileName("printYou.pdf")
        # self.loadFinished.connect(self.execpreview)

    def genUrl(self):
        pageSource = """<html><head>

        <script type="text/javascript" async src="MathJax2.6/MathJax.js?config=TeX-MML-AM_CHTML"></script>
        </head><body>
        <p><mathjax>$$
        \imath x+y=z
        \pi \\\\
        \\frac{1}{3}
        $$</mathjax></p>
        </body></html>"""

        tempFile = QFile('mathjax_ex.html')
        tempFile.open(QFile.WriteOnly)
        stream = QTextStream(tempFile)
        stream << pageSource
        tempFile.close()
        fileUrl = QUrl.fromLocalFile(QFileInfo(tempFile).canonicalFilePath())
        return fileUrl

    def execpreview(self,arg):
        self.print_(self.printer)


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
        self.questionDisp.genPdf()
        print("hello")



if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=QuestionDlg()
    dialog.show()
    app.exec_()
