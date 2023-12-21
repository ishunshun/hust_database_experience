# -*- coding:utf-8 -*-
from mysql.connector import connect,Error

try:
      cnn=connect(
            host="localhost",
            user="",
            password="",
            database=""
      )
except Error as e:
      print(e)

choice=0
choice=input("请输入你要选择的功能号\n"
             "1.新生入学信息增加，学生信息修改。\n"
             "2.课程信息维护（增加新课程，修改课程信息，删除没有选课的课程信息）。\n"
             "3.录入学生成绩，修改学生成绩。\n"
             "4.按系统计学生的平均成绩、最好成绩、最差成绩、优秀率、不及格人数。\n"
             "5.按系对学生成绩进行排名，同时显示出学生、课程和成绩信息。\n"
             "6.输入学号，显示该学生的基本信息和选课信息。\n"
             "7.退出\n")
while choice !="7" and choice!=0:
    if choice == "1":
        choice=0
        opt=input("请输入你的选择代码"
                  "1.增加一条学生入学信息"
                  "2.修改学生的信息")
        while opt!=0:
            if opt=="1":
                sno=input("Sno:")
                sname=input("Sname:")
                ssex=input("Ssex:")
                sage=input("Sage:")
                sdept=input("Sdept:")
                scholarship=input("Scholarship:")
                mycursor=cnn.cursor()
                sql=(
                    "insert "
                    "into "
                    "student "
                    "(Sno,Sname,Ssex,Sage,Sdept,Scholarship) "
                    "values(%s,%s,%s,%s,%s,%s)")
                info=(sno,sname,ssex,sage,sdept,scholarship)
                mycursor.execute(sql,info)
                cnn.commit()
                opt=input("还想要插入吗？如果还想要插入请输入1，否则0")
            elif opt=="2":
                sno=input("请告诉我对象的学号：")
                tochange=input("请告诉我要修改的属性：Sno，Sname，Ssex，Sage，Sdept，Scholarship")
                value=input("请告诉我要修改成多少：")
                mycursor = cnn.cursor()
                sql = (
                    "update student set "+tochange+" =%s where sno=%s")
                info=(value,sno)
                mycursor.execute(sql,info)
                cnn.commit()
                opt = input("还想要修改吗？如果还想要修改请输入2，否则0")

    if choice=="2":
        opt = input("请输入你的选择代码"
                    "1.增加一条课程信息"
                    "2.修改课程的信息"
                    "3.删除没有选课的课程信息")
        if opt=="1":
            cno=input("cno")
            cname=input("cname")
            cpno=input("cpno")
            ccredit=input("ccredit")
            mycursor = cnn.cursor()
            sql = (
                "insert "
                "into "
                "course "
                "(cno,cname,cpno,ccredit) "
                "values(%s,%s,%s,%s)")
            info = (cno, cname, cpno, ccredit)
            mycursor.execute(sql, info)
            cnn.commit()
            opt = input("还想要插入吗？如果还想要插入请输入1，否则0")
        elif opt=="2":
            sno=input("请告诉我对象的课程号：")
            tochange=input("请告诉我要修改的属性：cno，cname，cpno，ccredit")
            value=input("请告诉我要修改成多少：")
            mycursor = cnn.cursor()
            sql = (
                "update course set "+tochange+" =%s where cno=%s")
            info=(value,sno)
            mycursor.execute(sql,info)
            cnn.commit()
            opt = input("还想要修改吗？如果还想要修改请输入2，否则0")
        elif opt=="3":
            mycursor=cnn.cursor()
            sql="select cno from sc "
            mycursor.execute(sql)
            courses=[]
            for (course,) in mycursor:
                courses.append(course)
            mycursor.close()

            mycursor=cnn.cursor()
            sql="SET FOREIGN_KEY_CHECKS = 0"
            mycursor.execute(sql)
            cnn.commit()
            mycursor.close()

            mycursor = cnn.cursor()
            sql="delete from course where cno not in (select cno from sc)"
            mycursor.execute(sql)
            cnn.commit()
            mycursor.close()

            mycursor = cnn.cursor()
            sql = "SET FOREIGN_KEY_CHECKS = 1"
            mycursor.execute(sql)
            cnn.commit()
            mycursor.close()

    if choice=="3":
        opt = input("请输入你的选择代码"
                    "1.增加一条学生成绩信息"
                    "2.修改学生的成绩")
        while opt != 0:
            if opt == "1":
                sno = input("Sno:")
                cno = input("Cno:")
                grade = input("Grade:")
                mycursor = cnn.cursor()
                sql = (
                    "insert "
                    "into "
                    "sc "
                    "(Sno,Cno,Grade) "
                    "values(%s,%s,%s)")
                info = (sno, cno,grade)
                mycursor.execute(sql, info)
                cnn.commit()
                opt = input("还想要插入吗？如果还想要插入请输入1，否则0")
            elif opt == "2":
                sno = input("请告诉我对象的学号：")
                tochange = input("请告诉我要修改的属性：Sno，cno，grade")
                value = input("请告诉我要修改成多少：")
                mycursor = cnn.cursor()
                sql = (
                        "update sc set " + tochange + " =%s where sno=%s")
                info = (value, sno)
                mycursor.execute(sql, info)
                cnn.commit()
                opt = input("还想要修改吗？如果还想要修改请输入2，否则0")

    if choice=="4":
        mycursor=cnn.cursor()
        sql=("select sdept,avg(grade),max(grade),min(grade),"
             "SUM(CASE WHEN grade >= 90 THEN 1 ELSE 0 END) / COUNT(*) * 100 AS excellence_rate,"
             "SUM(CASE WHEN grade < 60 THEN 1 ELSE 0 END) AS fail_count from "
                "student,sc where student.sno=sc.sno group by sdept")
        mycursor.execute(sql)
        result=mycursor.fetchall()
        for row in result:
            print(row)
        cnn.commit()
        break
    if choice=="5":
        mycursor = cnn.cursor()
        sql = ("SELECT * FROM sc ORDER BY grade DESC")
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for row in result:
            print(row)
        cnn.commit()
        break
    if choice=="6":
        sno=input("请输入你要查询的学号：")
        mycursor = cnn.cursor()
        sql = ("select * from student left outer join sc using(sno) where sno="+sno)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for row in result:
            print(row)
        cnn.commit()
        break
    if choice=="7":
        break