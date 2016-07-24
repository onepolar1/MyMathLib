#!/usr/bin/env python
#-*- coding:utf-8 -*-

from resources import *

class DragImgTextEditEX(QTextEdit):
    mousePressedSignal = pyqtSignal(QPoint)

    def __init__(self, type, parent=None):
        super(DragImgTextEditEX, self).__init__(parent)
        self.setAcceptDrops(True)
        # self.setIconSize(QtCore.QSize(72, 72))

    def mousePressEvent(self, event):
        # print('a')
        if event.button() == Qt.RightButton:
            QTextEdit.mousePressEvent(self,event)
            return
        # print(event.sender(), event.button())
        # self.offset = event.pos()
        self.mousePressedSignal.emit(event.pos())
        # print(self.offset)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"), links)
        else:
            event.ignore()

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.pushButtonImage = QPushButton(self)
        self.btn2 = QPushButton(self)
        self.pushButtonImage.setText("Insert Image!")
        self.btn2.setText("测试")
        self.pushButtonImage.clicked.connect(self.on_pushButtonImage_clicked)
        self.btn2.clicked.connect(self.resizeImage)

        self.textEditImage = DragImgTextEditEX(self)
        self.textEditImage.mousePressedSignal.connect(self.OnMousePressed)

        self.textEditImage.setPlainText("Insert an image here:")

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonImage)
        self.layoutVertical.addWidget(self.btn2)
        self.layoutVertical.addWidget(self.textEditImage)

        # self.resizeImage()

    def OnMousePressed(self, pos):
        cursor = self.textEditImage.cursorForPosition(pos)
        rect1 = self.textEditImage.cursorRect(cursor)
        pos1 = QPoint(rect1.top(), rect1.left())
        # print(rect1.bottomRight)
        print(rect1, pos)
        print(self.textEditImage.viewport(), "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(self.textEditImage.mapToGlobal(pos1), "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # print(self.textEditImage.mapFromGlobal(pos), "=====================")
        # print(self.textEditImage.cursorRect(cursor), "~~~~~")
        # print(pos, "~~~~~")
        # print(cursor)
        position = cursor.position()
        print(position, '========================', cursor.charFormat().isImageFormat(), "\n\n")
        # print(self.textEditImage.)
        cursor.setPosition(position)
        self.textEditImage.setTextCursor(cursor)
        self.getEditImage()

    def getEditImage(self):
        currentBlock = self.textEditImage.textCursor().block()
        it = QTextBlock.iterator()
        it = currentBlock.begin()
        while it != currentBlock.end():
            currentFragment = it.fragment()
            it += 1
            if currentFragment.isValid():
                # print(currentFragment.position(), "11111qtextfragment")
                if currentFragment.charFormat().isImageFormat ():
                    # print(it)
                    newImageFormat = currentFragment.charFormat().toImageFormat()
                    # print(newImageFormat)
                    helper = self.textEditImage.textCursor()
                    # print(helper.selection())
                    # print(newImageFormat, '-------')
                    # print(currentFragment.position(), "qtextfragment")

    def resizeImage(self):
        currentBlock = self.textEditImage.textCursor().block()
        it = QTextBlock.iterator()
        it = currentBlock.begin()
        while it != currentBlock.end():
            currentFragment = it.fragment()
            # print(currentFragment.position())
            it += 1
            # print(it)

            if currentFragment.isValid():
                # print(currentFragment.charFormat())
                if currentFragment.charFormat().isImageFormat ():
                    newImageFormat = currentFragment.charFormat().toImageFormat()
                    # print(newImageFormat.name())
                    size = [newImageFormat.width(), newImageFormat.height()]
                    # print(size)
                    newImageFormat.setWidth(size[0]*0.8)
                    newImageFormat.setHeight(size[1]*0.8)

                    if  newImageFormat.isValid():
                        helper = self.textEditImage.textCursor()
                        helper.setPosition(currentFragment.position());
                        helper.setPosition(currentFragment.position() + currentFragment.length(), QTextCursor.KeepAnchor);
                        helper.setCharFormat(newImageFormat)



        # print(self.textEditImage.textCursor().block())


        # QTextBlock currentBlock = m_textEdit->textCursor().block();



    def on_pushButtonImage_clicked(self):
        filePath = QFileDialog.getOpenFileName(
            self,
            "Select an image",
            ".",
            "Image Files(*.png *.gif *.jpg *jpeg *.bmp)"
        )

        # print(filePath)
        if filePath:
            self.insertImage(filePath)

    def insertImage(self, filePath):
        imageUri = QUrl("file://{0}".format(filePath))
        # print(imageUri, "===")
        image    = QImage(QImageReader(filePath).read())

        self.textEditImage.document().addResource(
            QTextDocument.ImageResource,
            imageUri,
            image
        )

        imageFormat = QTextImageFormat()
        imageFormat.setWidth(100)
        # imageFormat.setWidth(image.width())
        imageFormat.setHeight(100)
        # imageFormat.setHeight(image.height())
        imageFormat.setName(imageUri.toString())

        textCursor = self.textEditImage.textCursor()
        # textCursor.movePosition(
        #     QTextCursor.End,
        #     QTextCursor.MoveAnchor
        # )
        textCursor.insertImage(imageFormat)

        # This will hide the cursor
        # blankCursor = QCursor(Qt.BlankCursor)
        # self.textEditImage.setCursor(blankCursor)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
