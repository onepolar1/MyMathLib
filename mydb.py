# 生成数据库

import sqlite3

def createDb():
    conn = sqlite3.connect("myQuestion.db")
    cur = conn.cursor()
    sqlstr1 = 'create table questiontable (questionhtml varchar(1000) primary key, \
        answerhtml varchar(2000), \
        category varchar(100), \
        questiontype varchar(50), \
        whichyear varchar(20), \
        demo varchar(500))'
    # print(sqlstr)

    sqlstr2 = 'create table categorytable (category varchar(100) primary key)'
    sqlstr3 = 'create table questypetable (questiontype varchar(50) primary key)'
    sqlstr4 = 'create table yearstable (whichyear varchar(20) primary key)'

    sqlstr5 = 'create table usertable ( username varchar(20) primary key, \
        password varchar(20), \
        unitname varchar(100), \
        adminlevel varchar(20))'

    for istr in [sqlstr1, sqlstr2, sqlstr3, sqlstr4, sqlstr5]:
        cur.execute(istr)
        conn.commit()

    # strdelete = "delete from student where 1=1"
    # cur.execute(strdelete)
    # conn.commit()
    # strdelete = "delete from tmprecord where 1=1"
    # cur.execute(strdelete)
    # conn.commit()
    # print(sqlstr2)

    # cur.execute(sqlstr)
    # conn.commit()
    # cur.execute(sqlstr2)
    # conn.commit()

    # insert example data
    # strsql = "insert into classtable values (?)"
    # cur.execute(strsql, ("三（3）班",))
    # conn.commit()
    # cur.execute(strsql, ("三（4）班",))
    # conn.commit()


    # a03lst = ["曾忆谊","赵佳泉","翁文秀","林珑","郑铭洁","林泽思","吴崇霖","陈思嘉","欧阳月孜","郭展羽","詹伟哲","黄佳仪","杨秋霞","周奕子","林楚杰","欧伊涵","许腾誉","陈唯凯","陈树凯","林彦君","张钰佳","高锴","杨博凯","林妙菲","林楚鸿","陈展烯","姚静茵","吴欣桐","范思杰","肖佳","马思广","许一帆","姚奕帆","陈海珣","吴黛莹","吴育桐","肖凯帆","林欣阳","叶茂霖","姚楷臻","陈嘉豪","陈琦","杨子楷","陈炎宏","陈幸仪","杨景畅","罗暖婷","郑馨"]
    # a04lst = ["罗恩琪","王可","曾祥威","谢濡婷","温嘉凯","许洁仪","肖欣淇","陈凯佳","林天倩","李乐海","吴文慧","黄文婷","万誉","陈进盛","张裕涵","陈振嘉","王巧玲","林珮琪","陈炜楷","杨健","赵泽锴","张凤临","蔡子丹","陈烨杰","廖妍希","林树超","夏培轩","陈锦森","李星","蔡依婷","姚容创","姚凯扬","沈嘉克","周凡","张玉川","邱金迅","陈菲敏","陈星翰","朱煜楷","郑泽洪","钱剑非","罗奕丰","陈杜炜","林知钦"]
    # strsql = "insert into student values (?, ?, ?, ?,?,?)"
    # for i in list(range(0,len(a03lst))):
    #     cur.execute(strsql, (None, "三（3）班", str(i+1).zfill(2), a03lst[i], 0, 0))
    #     conn.commit()
    # strsql = "insert into student values (?, ?, ?, ?,?,?)"
    # for i in list(range(0,len(a04lst))):
    #     cur.execute(strsql, (None, "三（4）班", str(i+1).zfill(2), a04lst[i], 0, 0))
    #     conn.commit()
    cur.close()

if __name__ == "__main__":
    createDb()
