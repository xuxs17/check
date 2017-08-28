# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 15:34:19 2017

@author: changjin
"""

import pyodbc

#从Check加载check类
from Check import check

#主方法
def main():
    #数据库参数
    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=xxx.xxx.xxx.xxx;DATABASE=xxx;UID=sa;PWD=xxx;charset=utf8")
    #获取游标
    cur = conn.cursor()
    #连接数据库
    Check = check(conn,cur)
    #清洗数据
    Check.cleandata(cur)
    #查找chucuoUserID与出错金额
    Check.checkID(cur)
    #查找出错人员姓名
    Check.checkName(cur)
    conn.close() 
    
if __name__ == '__main__':
    main()
    
