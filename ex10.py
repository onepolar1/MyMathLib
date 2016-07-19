#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import win32com
from win32com.client import Dispatch, constants
import time
import os
from resources import *

def GenBarCode(text):
    try:
        import huBarcode.code128 as hc
#        path = os.getcwd() + "\\tmp.png"
        path = "c:\\tmp.png"
        hc.Code128Encoder(str(text)).save(path,1)
        return True
    except:
        return False

def TransYMD2(date):
    numDict = {}
    numDict['0'] = u"〇"
    numDict['1'] = u"一"
    numDict['2'] = u"二"
    numDict['3'] = u"三"
    numDict['4'] = u"四"
    numDict['5'] = u"五"
    numDict['6'] = u"六"
    numDict['7'] = u"七"
    numDict['8'] = u"八"
    numDict['9'] = u"九"

    ymd = date.split('-')

    strYMD = ""
    tmpymd = [str(int(ymd[0])), str(int(ymd[1])), str(int(ymd[2]))]
    tmpymd2 = [u"年", u"月", u"日"]
    for item in zip(tmpymd, tmpymd2):
        for i in item[0]:
            strYMD += numDict[i]
        strYMD += item[1]
    return strYMD

def TransYMD(date):
    ymd = date.split('-')
    strYMD = str(int(ymd[0])) + u"年" + str(int(ymd[1])) + u"月" + str(int(ymd[2])) + u"日"
    return strYMD

def GenWordList(strlstword):
    try:
        w = win32com.client.Dispatch('Word.Application')
    except:
        QMessageBox.information("提示", "本机没有安装 MS WORD，或者 MS WORD 未被正确安装！请检查！")
        return

    strSn = strlstword[0]
    strName = strlstword[1]
    strUnit = strlstword[2]
    strDemo = strlstword[3]
    strDateStart = strlstword[4]
    strDateEnd = strlstword[5]
    strPUnit = strlstword[6]

    date = time.localtime()[0] + '-' + time.localtime()[1] + '-' +time.localtime()[2]
    strYMD = TransYMD(date)
#    print strSn.encode('gbk')
#    print strName.encode('gbk')
#    print strUnit.encode('gbk')
#    print strDemo.encode('gbk')
#    print strDateStart.encode('gbk')
#    print strDateEnd.encode('gbk')
#    print strYMD.encode('gbk')
    dotnum = 117
    title1 = u"军人请（休）假通知单"
    title2 = u"军人销假回执单"
    strword = title1 + "\r\n"
    strword += strUnit + u"：" + "\r\n"
    strword += u"　　同意你单位" + strName + u"同志休" + strDemo
    strword += u"从" + TransYMD(strDateStart) + u"至" + TransYMD(strDateEnd) + u"。"
    strword += "\r\n" + u"　　特此通知。" + "\r\n\r\n"
    strword += "\t" + strPUnit + "  ."
    strword += "\r\n"
    strword += u"编号：" + strSn + u"　　" + strYMD + "\r\n"

    strword += "."*dotnum + "\r\n"
    strword += title2 + "\r\n"
    strword += strPUnit + u"：" + "\r\n"
    strword += u"　　我单位" + strName + u"同志于_______年___月___日归队，休假____天，余（超）假____天。"
    strword += "\r\n\r\n"
    strword += "\t" + strUnit + u"领导签字：" + "\r\n"
    strword += u"编号：" + strSn + u"　　　" + u"____年__月__日"
#    print strword.encode('gbk')
#    return

    w.Visible = 1
    w.DisplayAlerts = 0
    doc = w.Documents.Add()
    myRange = doc.Range(0,0)
    myRange.InsertAfter(strword)

    #Set the page
    w.ActiveDocument.PageSetup.TopMargin = 1.5*28.35
    w.ActiveDocument.PageSetup.BottomMargin = 1.5*28.35
    w.ActiveDocument.PageSetup.LeftMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.RightMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.PageWidth = 13*28.35
    w.ActiveDocument.PageSetup.PageHeight = 18.4*28.35
    # Arrange the paper type
    w.Selection.WholeStory()
    w.Selection.Font.Size = 14
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.LineSpacingRule = 4
    w.Selection.ParagraphFormat.LineSpacing = 20

    # find and set font
#    w.Selection.HomeKey(6)
#    w.Selection.Find.ClearFormatting()
#    w.Selection.Find.Text = strUnit
#    while w.Selection.Find.Execute():
#        w.Selection.ParagraphFormat.Alignment = 0
#        w.Selection.Font.Name = u"楷体_GB2312"
#        w.Selection.Font.Underline = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strPUnit + "  ."
    w.Selection.Find.Execute()
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.ParagraphFormat.TabStops.Add(Position=9.5*28.35, Alignment=2, Leader=0)
    w.Selection.Font.Underline = 0

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = u"领导签字："
    w.Selection.Find.Execute()
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.ParagraphFormat.TabStops.Add(Position=9.5*28.35, Alignment=2, Leader=0)
    w.Selection.Font.Underline = 0

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strUnit
    w.Selection.Find.Execute()
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.Font.Name = u"楷体_GB2312"
    w.Selection.Font.Underline = 1

#    w.Selection.HomeKey(6)
#    w.Selection.Find.ClearFormatting()
#    w.Selection.Find.Text = strPUnit + u"："
#    w.Selection.Find.Execute()
#    w.Selection.ParagraphFormat.Alignment = 0
#    w.Selection.Font.Name = u"楷体_GB2312"
#    w.Selection.Font.Underline = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strName
    while w.Selection.Find.Execute():
        w.Selection.Font.Name = u"楷体_GB2312"
        w.Selection.Font.Underline = 1

    for item in [title1, title2]:
        w.Selection.HomeKey(6)
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Text = item
        while w.Selection.Find.Execute():
            w.Selection.Font.Name = u"宋体"
            w.Selection.Font.Size = 16
            w.Selection.ParagraphFormat.Alignment = 1
            w.Selection.ParagraphFormat.LineSpacingRule = 0
            w.Selection.ParagraphFormat.LineUnitAfter = 0.5

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = u"编号"
    while w.Selection.Find.Execute():
        w.Selection.Font.Name = u"黑体"
        w.Selection.ParagraphFormat.LineUnitBefore = 0.5
        w.Selection.ParagraphFormat.LineUnitAfter = 0

    # set dotline
    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "."*dotnum
    w.Selection.Find.Execute()
    w.Selection.ParagraphFormat.LeftIndent = -0.9*28.35
    w.Selection.ParagraphFormat.RightIndent = -0.9*28.35
    w.Selection.Font.Name = u"宋体"
    w.Selection.Font.Spacing = -4

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "_"
    while w.Selection.Find.Execute():
        w.Selection.Font.Name = u"宋体"

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "  ."
    w.Selection.Find.Execute()
    w.Selection.Delete(Unit=1, Count=1)
    w.Selection.HomeKey(6)
    w.ActiveWindow.ActivePane.View.Zoom.Percentage = 100

def GenWordList2(strlstword):
    try:
        w = win32com.client.Dispatch('Word.Application')
    except:
        wx.MessageBox(u"本机没有安装 MS WORD，或者 MS WORD 未被正确安装！请检查！", u"提示")
        return

    strSnPng = os.getcwd() + "\\tmp.png"
    strName = strlstword[1]
    strUnit = strlstword[2]
    strDemo = strlstword[3]
    strDateStart = strlstword[4]
    strDateEnd = strlstword[5]
    strPUnit = strlstword[6]

    date = time.localtime()[0] + '-' + time.localtime()[1] + '-' +time.localtime()[2]
    strYMD = TransYMD(date)
#    print strSn.encode('gbk')
#    print strName.encode('gbk')
#    print strUnit.encode('gbk')
#    print strDemo.encode('gbk')
#    print strDateStart.encode('gbk')
#    print strDateEnd.encode('gbk')
#    print strYMD.encode('gbk')
    dotnum = 117
    title1 = u"军人请（休）假通知单"
    title2 = u"军人销假回执单"
    strword = title1 + "\r\n"
    strword += strUnit + u"：" + "\r\n"
    strword += u"　　同意你单位" + strName + u"同志休" + strDemo
    strword += u"从" + TransYMD(strDateStart) + u"至" + TransYMD(strDateEnd) + u"。"
    strword += "\r\n" + u"　　特此通知。" + "\r\n\r\n"
    strword += "\t" + strPUnit + "  ." + "\r\n"
    strword += u"MM\t" + strYMD + "\r\n"
    strword += "."*dotnum + "\r\n"
    strword += title2 + "\r\n"
    strword += strPUnit + ":" + "\r\n"
    strword += u"　　我单位" + strName + u"同志于_______年___月___日归队，休假____天，余（超）假____天。"
    strword += "\r\n\r\n"
    strword += "\t" + strUnit + u"领导签字：" + "\r\n"
    strword += "MM\t" + u"____年__月__日"

    w.Visible = 1
    w.DisplayAlerts = 0
    doc = w.Documents.Add()
    myRange = doc.Range(0,0)
    myRange.InsertAfter(strword)

    #Set the page
    w.ActiveDocument.PageSetup.TopMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.BottomMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.LeftMargin = 1.1*28.35
    w.ActiveDocument.PageSetup.RightMargin = 1.1*28.35
    w.ActiveDocument.PageSetup.PageWidth = 13*28.35
    w.ActiveDocument.PageSetup.PageHeight = 18.4*28.35
    # Arrange the paper type
    w.Selection.WholeStory()
    w.Selection.Font.Size = 14
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.LineSpacingRule = 4
    w.Selection.ParagraphFormat.LineSpacing = 20

    # find and set font
#    w.Selection.HomeKey(6)
#    w.Selection.Find.ClearFormatting()
#    w.Selection.Find.Text = strUnit
#    while w.Selection.Find.Execute():
#        w.Selection.ParagraphFormat.Alignment = 0
#        w.Selection.Font.Name = u"楷体_GB2312"
#        w.Selection.Font.Underline = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strPUnit + "  ."
    w.Selection.Find.Execute()
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.ParagraphFormat.TabStops.Add(Position=9.5*28.35, Alignment=2, Leader=0)
    w.Selection.Font.Underline = 0

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = u"领导签字："
    w.Selection.Find.Execute()
    w.Selection.Font.Name = u"仿宋_GB2312"
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.ParagraphFormat.TabStops.Add(Position=9.5*28.35, Alignment=2, Leader=0)
    w.Selection.Font.Underline = 0

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strUnit
    w.Selection.Find.Execute()
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.Font.Name = u"楷体_GB2312"
    w.Selection.Font.Underline = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strPUnit + ":"
    w.Selection.Find.Execute()
    w.Selection.ParagraphFormat.Alignment = 0
    w.Selection.Font.Name = u"楷体_GB2312"
    w.Selection.Font.Underline = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = strName
    while w.Selection.Find.Execute():
        w.Selection.Font.Name = u"楷体_GB2312"
        w.Selection.Font.Underline = 1

    for item in [title1, title2]:
        w.Selection.HomeKey(6)
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Text = item
        while w.Selection.Find.Execute():
            w.Selection.Font.Name = u"宋体"
            w.Selection.Font.Size = 16
            w.Selection.ParagraphFormat.Alignment = 1
            w.Selection.ParagraphFormat.LineSpacingRule = 0
            w.Selection.ParagraphFormat.LineUnitAfter = 0.5

    # set dotline
    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "."*dotnum
    w.Selection.Find.Execute()
    w.Selection.ParagraphFormat.LeftIndent = -0.9*28.35
    w.Selection.ParagraphFormat.RightIndent = -0.9*28.35
    w.Selection.Font.Name = u"宋体"
    w.Selection.Font.Spacing = -4

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "_"
    while w.Selection.Find.Execute():
        w.Selection.Font.Name = u"宋体"

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "  ."
    w.Selection.Find.Execute()
    w.Selection.Delete(Unit=1, Count=1)

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "MM"
    while w.Selection.Find.Execute():
        w.Selection.Delete(Unit=1, Count=1)
        w.Selection.ParagraphFormat.LeftIndent = -0.19 *28.35
        w.Selection.ParagraphFormat.TabStops.Add(Position=10.5*28.35, Alignment=2, Leader=0)
        w.Selection.ParagraphFormat.AutoAdjustRightIndent = False
        w.Selection.ParagraphFormat.DisableLineHeightGrid = True
        w.Selection.ParagraphFormat.LineSpacingRule = 0
        w.Selection.InlineShapes.AddPicture(FileName=strSnPng, LinkToFile=False, SaveWithDocument=True)
    w.Selection.HomeKey(6)
    w.ActiveWindow.ActivePane.View.Zoom.Percentage = 100

def MyGenWordList(strlstword):
    path = os.getcwd() + "\\tmp.png"
    if os.path.exists(path):
        GenWordList2(strlstword)
    else:
        GenWordList(strlstword)

def GenStatWord(title, picpath, listData):
    try:
        w = win32com.client.Dispatch('Word.Application')
    except:
        wx.MessageBox(u"本机没有安装 MS WORD，或者 MS WORD 未被正确安装！请检查！", u"提示")
        return

    w.Visible = 1
    w.DisplayAlerts = 0
    doc = w.Documents.Add()
    myRange = doc.Range(0,0)

    #Set the page
    w.ActiveDocument.PageSetup.TopMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.BottomMargin = 1.2*28.35
    w.ActiveDocument.PageSetup.LeftMargin = 1.1*28.35
    w.ActiveDocument.PageSetup.RightMargin = 1.1*28.35
    w.ActiveDocument.PageSetup.PageWidth = 18.4*28.35
    w.ActiveDocument.PageSetup.PageHeight = 26*28.35

    pieDes = u"正在休假人员比例(所有人员)\t已经休假人员比例(只含士官)"
    barDes = str(time.localtime()[0])+u"本年度各月休假人次统计"
    myRange.InsertAfter(title + "legend\r\n")
    myRange.InsertAfter("pie1\tpie2\r\n")
#    myRange.InsertAfter("legend\r\n")
    myRange.InsertAfter(pieDes + "\r\n")
    myRange.InsertAfter("bar1\r\n")
    myRange.InsertAfter(barDes + "\r\n")

    w.Selection.WholeStory()
    w.Selection.ParagraphFormat.Alignment = 1

    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = title
    w.Selection.Find.Execute()
    w.Selection.Font.Name = u"黑体"
    w.Selection.Font.Size = 16
    w.Selection.ParagraphFormat.LineSpacingRule = 0
#    w.Selection.ParagraphFormat.LineUnitAfter = 0.5

    lstmark = ["pie1", "pie2", "bar1"]
    for imark, ipath in zip(lstmark, picpath):
        w.Selection.HomeKey(6)
        w.Selection.Find.ClearFormatting()
        w.Selection.Find.Text = imark
        w.Selection.Find.Execute()
        w.Selection.Delete(Unit=1, Count=1)
        w.Selection.InlineShapes.AddPicture(FileName=ipath, LinkToFile=False, SaveWithDocument=True)

    # Insert legend
    w.Selection.HomeKey(6)
    w.Selection.Find.ClearFormatting()
    w.Selection.Find.Text = "legend"
    w.Selection.Find.Execute()
    w.Selection.Delete(Unit=1, Count=1)
    w.ActiveDocument.Tables.Add(Range=w.Selection.Range, NumRows=2, \
        NumColumns=1, DefaultTableBehavior=1, AutoFitBehavior= 0)
    w.Selection.Tables(1).Columns.PreferredWidth = 4*28.35
    w.Selection.Cells.Shading.BackgroundPatternColor = 32768
    w.Selection.Font.Color = 16777215
    w.Selection.TypeText(Text=u"在位（或未休假）")
    w.Selection.Tables(1).Rows.Alignment = 2
    w.Selection.MoveDown(Unit=5, Count=1)
    w.Selection.Cells.Shading.BackgroundPatternColor = 16711680
    w.Selection.Font.Color = 16777215
    w.Selection.TypeText(Text=u"休假（或已休假）")
#    return

    # Insert table
    lstDes = u"各单位休假详情列表"
    myRange.InsertAfter("\r\n" + lstDes )

    w.Selection.ParagraphFormat.Alignment =  0
    w.Selection.EndKey(6)

    import pyperclip
    mathstr = """<math xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <msup>
            <mi>a</mi>
            <mi>b</mi>
        </msup>
    </mrow>
</math>"""
    pyperclip.copy(mathstr)
    w.Selection.Paste()
    # w.Selection.OMaths(1).ParentOMath.Justification = 3
    w.Selection.EndKey(6)

    w.Selection.TypeText(Text="休假（或已休假）")

    mathstr = """<math xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
        <msup>
            <mi>a</mi>
            <mi>b</mi>
        </msup>
    </mrow>
</math>"""
    pyperclip.copy(mathstr)
    w.Selection.Paste()
    # w.Selection.OMaths(1).ParentOMath.Justification = 3
    w.Selection.EndKey(6)


    #
    # rows = len(listData)
    # cols = len(listData[0])
    # w.ActiveDocument.Tables.Add(Range=w.Selection.Range, NumRows=rows, \
    #     NumColumns=cols, DefaultTableBehavior=1, AutoFitBehavior= 0)
    #
    # for irow in listData:
    #     for icol in irow:
    #         w.Selection.TypeText(Text = icol)
    #         w.Selection.MoveRight(Unit=1, Count=1)
    #
    # w.Selection.HomeKey(6)
    # w.Selection.Find.ClearFormatting()
    # w.Selection.Find.Text = lstDes
    # w.Selection.Find.Execute()
    # w.Selection.EndKey(Unit=5)
    # w.Selection.MoveRight(Unit=1, Count=1)
    # w.Selection.Tables(1).AutoFitBehavior (1)
    # w.Selection.Tables(1).Rows.Alignment = 1
    w.Selection.HomeKey(6)


if __name__ == '__main__':
    import os
    curdir = os.getcwd() + os.path.sep
    GenStatWord(u"固体队　统计图表", [curdir+r'images\trash.png', curdir+r'images\trash.png', curdir+r'images\trash.png'], [['1','a','b'], ['2','c','d']])
#
