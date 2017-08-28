# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:07:37 2017

@author: changjin
"""

#创建check类
class check():
    #连接数据库
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        #如果存在newtb则删除
        cur.execute("IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[newtb]') AND type in (N'U'))DROP TABLE [dbo].[newtb]")
        #将多个季度用户消费记录表合并为一张名为newtb的新表(字段不变)
        cur.execute("SELECT * into newtb FROM Record201602 union all select * FROM Record201603 union all select * FROM Record201604 union all select * FROM Record201701 union all select * FROM Record201702 union all select * FROM Record201703")
        #如果需要在上一SQL语句尾部新一季度的表名,例如直接添加union all select * FROM Record201704,将2016年记录与2017记录汇总合成一张新表
        conn.commit()
       
    #清洗数据
    def cleandata(self,cur):
        #从用户消费记录汇总表中,按照UserID汇总查询用户消费记录,并且剔除UserID为0,1,2,4,10的测试账号
        cur.execute("SELECT UserID,sum(Rate) FROM newtb where UserID not in (0,1,2,3,4,10) group by UserID ORDER BY UserID")
        a=cur.fetchall()
        #将查询结果保存至一个名为record的字典中
        global record,zengRecharge,recharge
        record= dict(a) 
        #从用户充值表中,按照UserID汇总查询用户充值金额(只取增款)并且不计算因错退还的金额
        cur.execute("SELECT UserID,sum(Rate) FROM Recharge_Info where RType not in ('因错退还') and IDType in ('增款') GROUP BY UserID ORDER BY UserID")
        b = cur.fetchall()
        #将查询结果保存到一个名为 zengRecharge的字典中
        zengRecharge = dict(b)
        #从用户充值表中,按照UserID汇总查询用户充值金额(只取减款)
        cur.execute("select UserID,sum(Rate) from Recharge_Info where IDType in ('减款') GROUP BY UserID ORDER BY UserID")
        c = cur.fetchall()
        #将查询结果保存到一个名为 jianRecharge的字典中
        jianRecharge = dict(c)
        #新建一个名为Recharge的空字典        
        recharge = {}
        #用增款减去减款得到用户纯充值金额,并且将其存入recharge中
        for m,n in jianRecharge.items():
             if m in zengRecharge.keys():
                 zengRecharge[m] -= n
        recharge = zengRecharge

    #查找出错UserID与出错金额
    def checkID(self,cur):
        #从用户信息表中按照UserID汇查询用户余额
        cur.execute("SELECT UserID,SUM(UserAmount) FROM User_Info WHERE UserID not in (1,2,3,4,10) GROUP BY UserID ORDER BY UserID")
        d = cur.fetchall()
        #将查询结果保存至一个名为amount的空字典中
        amount = dict(d)
        global usid,wrong
        #新建usid与wrong的两个列表,用来存放出错UserID与出错金额
        usid = []
        wrong = [] 
        #按照对应UserID将用户充总值金额减去总消费金额减去用户余额,以此检验金额是否出错
        for k,v in record.items():
            if k in recharge.keys() and k in amount.keys():
                #判断是否出错
                if recharge[k] - record[k] - amount[k] != 0:
                    #若出错,将UserID添加至usid列表中
                    usid.append(k)
                    #将出错金额保存到wrong列表中
                    wrong.append(recharge[k] - record[k] - amount[k])
        #将出错UserID与出错金额打印出来
        wrong = list(map(str,wrong))
        print(usid)
        print(wrong)
        
    #查找出错人员姓名
    def checkName(self,cur):
        us = list(map(str,usid))
        #按照UserID在用户信息表中查找用户姓名
        for i in range(len(us)):
            strI = us[i]
            sql="SELECT UserName FROM User_Info WHERE UserID in("+strI+") ORDER BY UserID"
            cur.execute(sql)
            t = cur.fetchall()
            t = list(map(str,t))
            #打印用户姓名
            print(t)
    
   
    
