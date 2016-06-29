#!/usr/bin/env python

import sys
from PyQt4.QtCore import QFile, QFileInfo, QTextStream, QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView, QWebSettings

pageSource = """<html><head>

<script type="text/javascript" async src="MathJax2.6/MathJax.js?config=TeX-MML-AM_CHTML"></script>
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
myset = webView.settings()
myset.setFontSize(QWebSettings.MinimumFontSize, 20)

sys.exit(app.exec_())
