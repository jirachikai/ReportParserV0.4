__author__ = 'Administrator'
import sqlite3
from ..Model import Test
from datetime import *
import socket
import logging
class DBReader(object):
	def ReadSingleDay(self,date,productName):
		try:
			docs = []
			conn = sqlite3.connect("Result.db")
			cursor = conn.execute('SELECT DT_ID,Link,DocumentName,Type FROM DailyTest WHERE Date=? and productName=?',(date,productName,))	
			for line in cursor.fetchall():
				doc = Test.Document()
				doc.DocumentTime = date
				doc.Link = line[1]
				doc.DocumentName = line[2]
				doc.DocumentType = line[3]
				doc.Test = self.__readDocumentTest(conn,line[0]) #line[0] is dailyTestID
				docs.append(doc)
			conn.close()
		except Exception as err:
			self.__writeLog("Logging.log","ReadSingleDay: " + str(err)) 
		return docs
	
	def ReadReportDate(self,date,productName):
		try:
			l=[]
			date = ''.join(date.split('-'))#change Year-Month-Day to YearMonthDay for DB Search
			date = date + '%'
			conn = sqlite3.connect("Result.db")
			cursor = conn.execute('SELECT Date FROM DailyTest WHERE Date LIKE ? and ProductName=?',(date,productName,))
			list = cursor.fetchall()
			l = [i[0] for i in list]
		except Exception as err:
			self.__writeLog("Logging.log","ReadReportDate: " + str(err))
		if l:
			return max(l)
		else:
			return None
	
	def ReadPeriodDays(self,start,end,productName):
		try:
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
		except Exception as err:
			self.__writeLog("Logging.log","ReadPeriodDays: " + str(err))
			return [0,0,0,0]
		return total,passed,d,link
	
	def __writeLog(self,filePath,errorMessage):
		logger = logging.getLogger("database")
		formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',) 
		file_handler = logging.FileHandler(filePath) 
		file_handler.setFormatter(formatter) 
		logger.addHandler(file_handler)  
		logger.error(errorMessage)
		logger.removeHandler(file_handler)  
		
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
