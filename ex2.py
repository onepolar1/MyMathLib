#!/usr/bin/env python

import sys
from PyQt4.QtCore import QFile, QFileInfo, QTextStream, QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView

pageSource = """<html><head>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
</head><body>
<p><mathjax>$$
\imath x+y=z
$$</mathjax></p>
</body></html>"""

app = QApplication(sys.argv)

tempFile = QFile('mathjax_ex.html')
tempFile.open(QFile.WriteOnly)
stream = QTextStream(tempFile)
stream << pageSource
tempFile.close()
fileUrl = QUrl.fromLocalFile(QFileInfo(tempFile).canonicalFilePath())

webView = QWebView()
webView.load(fileUrl)
webView.show()

sys.exit(app.exec_())
