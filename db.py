import MySQLdb,sys,os


def connectMysql():
	conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123",db="lists")
        return conn



def importMysql():
	conn=connectMysql()


	f=open("white_list","r")
	for line in f.readlines():
	  line_list=line.strip().split(" ")
	  sql='insert into white_list(url) values(\'' + line_list[0] + '\')'
	  conn.cursor().execute(sql)
	  conn.commit()
	  conn.cursor().close()

	f=open("black_list","r")
	for line in f.readlines():
	  line_list=line.strip().split(" ")
	  sql='insert into black_list(url) values(\'' + line_list[0] + '\')'
	  conn.cursor().execute(sql)
	  conn.commit()
	  conn.cursor().close()

        conn.close()



def iswhite_list(url):
	conn=connectMysql()
	cursor=conn.cursor()
	sql='select * from white_list where url="'+url+'"'
	result=cursor.execute(sql)

        cursor.close()
        conn.close()
        return result



def isblack_list(url):
	conn=connectMysql()
	cursor=conn.cursor()
	sql='select * from black_list where url="'+url+'"'
	result=cursor.execute(sql)


        conn.close()
        cursor.close()
	return result



def insertblack_list(url):
        conn=connectMysql()
        cursor=conn.cursor()

        sql='insert into black_list(url) values(\'' + url + '\')'
        cursor.execute(sql)
        conn.commit()


        cursor.close()
        conn.close()


def getWhite_list():
	conn = connectMysql()
	cursor = conn.cursor()

	cursor.execute('select * from white_list')

	white_lists = []
	for list in cursor.fetchall():
		white_lists.append(list[0])



        cursor.close()
        conn.close()
	return white_lists
