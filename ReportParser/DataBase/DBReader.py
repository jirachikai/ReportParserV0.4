__author__ = 'Administrator'
import sqlite3
from ..Model import Test
from datetime import *
import socket
class DBReader(object):
	def ReadSingleDay(self,date,productName):
		conn = sqlite3.connect("Result.db")
		cursor = conn.execute('SELECT DT_ID,Link,DocumentName,Type FROM DailyTest WHERE Date=? and productName=?',(date,productName,))
		docs = []
		for line in cursor.fetchall():
			doc = Test.Document()
			doc.DocumentTime = date
			doc.Link = line[1]
			doc.DocumentName = line[2]
			doc.DocumentType = line[3]
			doc.Test = self.__readDocumentTest(conn,line[0]) #line[0] is dailyTestID
			docs.append(doc)
		conn.close()
		return docs
	
	def ReadReportDate(self,date,productName):
		date = ''.join(date.split('-'))#change Year-Month-Day to YearMonthDay for DB Search
		date = date + '%'
		conn = sqlite3.connect("Result.db")
		cursor = conn.execute('SELECT Date FROM DailyTest WHERE Date LIKE ? and ProductName=?',(date,productName,))
		list = cursor.fetchall()
		l = [i[0] for i in list]
		if l:
			return max(l)
		else:
			return None

	def ReadPeriodDays(self,start,end,productName):
		conn = sqlite3.connect("Result.db")
		sd = self.__getDate(start)
		ed = self.__getDate(end)
		tempDate = sd
		if (ed - sd).days < 0 or (ed - sd).days > 31:
			return None
		d = []
		total = []
		passed = []
		link = []
		ip = socket.gethostbyname(socket.gethostname())
		while tempDate <= ed:
			DateString = self.__getDateString(tempDate)
			cursor = conn.execute('SELECT Total,Passed FROM BirdsView WHERE Date=? and productName=?',(DateString,productName,))
			line = cursor.fetchone()
			d.append(tempDate.strftime("%d") )
			link.append('/'+productName+'/Date/' + tempDate.strftime("%Y-%m-%d"))
			if not line:
				total.append(0)
				passed.append(0)
				tempDate += timedelta(days = 1,seconds =0, microseconds = 0)
				continue
			total.append(line[0])
			passed.append(line[1])
			tempDate += timedelta(days = 1,seconds =0, microseconds = 0)
		return total,passed,d,link

	def __getDate(self,d):
		splitDate = d.split('-')
		return date(int(splitDate[0]),int(splitDate[1]),int(splitDate[2]))

	def __getDateString(self,day):
		dateString = day.strftime('%Y-%m-%d')
		s = ""
		for item in dateString.split('-'):
			s = s + str(int(item)) + '-'
		return s[0:len(s)-1]

	def __readDocumentTest(self,conn,DT_ID):
		cursor = conn.execute('SELECT TestName,Result FROM Result WHERE DT_ID = ?',(DT_ID,))
		tests = []
		for line in cursor.fetchall():
			test = Test.TestWithoutTable()
			test.TestName = line[0]
			test.TestResult = line[1]
			tests.append(test)
		return tests
