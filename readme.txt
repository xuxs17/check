1.如果需要添加新一季度,在Check.py的__init__的SQL语句尾部直接添加union all select * FROM 表名 ,这样就可以了
2.使用时运行testCheck.py

