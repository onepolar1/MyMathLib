from resources import *

def genImg2(strques = ""):
    tmplst1 = re.split("/>", strques)
    alllst = []
    # print(1, tmplst1, len(tmplst1))
    curdir = os.getcwd() + os.path.sep
    for istr in tmplst1[:-1]:
        if istr.strip() != "":
            tmplst2 = re.split("<img", istr)
            # print(2, tmplst2, len(tmplst2))
            if tmplst2[0].strip() != "":
                alllst.append(tmplst2[0])
            tmpImgStr = "<img " + tmplst2[1] + " />"
            soup = BeautifulSoup(tmpImgStr, "lxml")
            imglst = soup.findAll('img')
            tmpdict = {}
            tmpdict['filename'] = curdir + imglst[0]['src']
            tmpdict['height'] = imglst[0]['height']
            tmpdict['width'] = imglst[0]['width']
            tmpdict['width'] = imglst[0]['width']
            tmpdict['align'] = imglst[0]['align']
            alllst.append(tmpdict)

    if tmplst1[-1] != "":
        alllst.append(tmplst1[-1])

    return alllst


def genImg(strques = ""):
    soup = BeautifulSoup(strques, "lxml")
    imglst = soup.findAll('img')

    if len(imglst) == 0:
        return [strques]

    for i in range(len(imglst)):
        strques = strques.replace(str(imglst[i]), "!img!")

    strqueslst = re.split("!img!", strques)

    lastLstQues = []
    resuLstQues = []
    indx = 0
    tmpdict = {}
    curdir = os.getcwd() + os.path.sep
    for istr in strqueslst[:-1]:
        lastLstQues.append(istr)
        tmpdict['filename'] = curdir + imglst[indx]['src']
        tmpdict['height'] = imglst[indx]['height']
        tmpdict['width'] = imglst[indx]['width']
        tmpdict['width'] = imglst[indx]['width']
        tmpdict['align'] = imglst[indx]['align']
        lastLstQues.append(tmpdict)
        tmpdict = {}
        indx += 1

    lastLstQues.append(strqueslst[-1])
    for ivalue in lastLstQues:
        if ivalue != "":
            resuLstQues.append(ivalue)

    # print(strques)
    return resuLstQues


def getMathml(strques = ""):

    strques = strques.replace("\$", "!!")
    if strques.count("$") == 0 or strques.count("$") % 2 == 1:
        strques = strques.replace("!!", "$")
        return strques

    strsplit = re.split("\$", strques)
    laststr = []

    for i in range(len(strsplit)):
        if strsplit[i] == "":
            continue;

        if i%2 == 1: # math
            latex_input = strsplit[i]
            # print("=====", latex_input, len(latex_input))
            if latex_input != "":
                mathml_output = latex2mathml.convert(latex_input)
                # laststr += mathml_output.replace("<math>", '<math xmlns="http://www.w3.org/1998/Math/MathML">')
                laststr.append(mathml_output.replace("<math>", '<math xmlns="http://www.w3.org/1998/Math/MathML">'))
        else:
            laststr.append(strsplit[i])
            # laststr += strsplit[i]

    for i in range(len(laststr)):
        laststr[i] = laststr[i].replace("!!", "$")
    return laststr

def generateWordList():
    s = """这是计算题$3232+3232=$（    ）\r\n<img align="right" alt="Smiley face" height="100" src="images/login.png" width="100"/><img align="right" alt="Smiley face" height="100" src="images/trash.png" width="100"/>\n再试试"""
    quesImgList = genImg2(s)
    # quesImgList = genImg(s)
    allList = []
    for istr in quesImgList:
        if type(istr) != type({}):
            allList.extend(getMathml(istr))
        else:
            allList.append(istr)
    return allList

def GenWordFile(title, listData):
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

    w.Selection.WholeStory()
    w.Selection.ParagraphFormat.Alignment = 1

    w.Selection.HomeKey(6)
    w.Selection.Font.Name = u"黑体"
    w.Selection.Font.Size = 16
    w.Selection.ParagraphFormat.LineSpacingRule = 0
    w.Selection.TypeText(Text=title+"\r\n")
    w.Selection.EndKey(6)

    # type the question
    w.Selection.ParagraphFormat.Alignment =  0
    w.Selection.Font.Name = "宋体"
    w.Selection.Font.Size = 12
    w.Selection.EndKey(6)
    # w.Selection.TypeText(Text=listData)

    for item in listData:
        if type(item) == type(""):
            if item[1:5] != "math":
                w.Selection.TypeText(Text=item)
            else:
                pyperclip.copy(item)
                w.Selection.Paste()
                w.Selection.EndKey(6)
            w.Selection.ParagraphFormat.Alignment = 0
        elif type(item) == type({}):
            if item['align'] == "right":
                w.Selection.ParagraphFormat.Alignment = 2
            imgshape = w.Selection.InlineShapes.AddPicture(FileName=item['filename'], LinkToFile=False, SaveWithDocument=True)
            imgshape.width = item['width']
            imgshape.height = item['height']
            if item['align'] == "right":
                w.Selection.ParagraphFormat.Alignment = 2
            w.Selection.EndKey(6)


if __name__ == '__main__':
    tmpques = generateWordList()
    GenWordFile("题库", tmpques)

    # print(tmpques)
    # s = 'ccc\$'
    # s = """这是计算题$3232+3232=$（    ）\r\n<img align="right" alt="Smiley face" height="100" src="images/login.png" width="100"/><img align="right" alt="Smiley face" height="100" src="images/trash.png" width="100"/>\n再试试"""
    #
    # print(genImg2(s))
    # print(genImg(s))
    # print(getMathml(s))
