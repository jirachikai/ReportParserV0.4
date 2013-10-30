import sqlite3
import logging
DBPath = "Result.db"
class DBWriter(object):
	def WriteSingleDay(self,doc,productName):
		try:
			DT_ID = self.__writeDailyTestTable(doc,productName)
			self.__writeTest(doc,DT_ID)
		except Exception as err:
			self.__writeLog("Logging.log","WriteSingleDay: " + str(err))
			
	def WriteBirdsView(self,date,total,passes,productName):
		try:
			conn = sqlite3.connect(DBPath)
			cursor = conn.execute('SELECT Date FROM BirdsView WHERE Date=? and productName=?',(date,productName,))
			line = cursor.fetchone()
			if line:
				conn.execute('UPDATE BirdsView SET Total = ?, Passed = ? WHERE Date = ? and ProductName = ?',(total,passes,date,productName))
				conn.commit()
				conn.close()
				return 
			list = [date,total,passes,productName]
			conn.execute('INSERT INTO BirdsView VALUES(?,?,?,?)',list)
			conn.commit()
			conn.close()
		except Exception as err:
			self.__writeLog("Logging.log","WriteBirdsView: " + str(err))
			conn.close()
	
	def __writeLog(self,filePath,errorMessage):
		logger = logging.getLogger("database")
		formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',) 
		file_handler = logging.FileHandler(filePath) 
		file_handler.setFormatter(formatter) 
		logger.addHandler(file_handler)  
		logger.error(errorMessage)
		logger.removeHandler(file_handler) 
		
	def __writeDailyTestTable(self,doc,productName):
		conn = sqlite3.connect(DBPath)
		list = [doc.DocumentTime,self.__getLink(doc.Link),doc.DocumentName,doc.DocumentType,productName]
		conn.execute('INSERT INTO DailyTest VALUES(NULL,?,?,?,?,?)',list)
		conn.commit()
		cursor = conn.execute('SELECT max(DT_ID) FROM DailyTest')
		Recently_DT_ID = cursor.fetchone()[0]
		conn.close()
		return Recently_DT_ID

	def __writeTest(self,Document,DT_ID):
		for test in Document.Test:
			conn = sqlite3.connect(DBPath)
			list = [DT_ID,test.TestName,test.TestResult]
			conn.execute('INSERT INTO Result VALUES(NULL,?,?,?)',list)
			conn.commit()
			conn.close()

	def __getLink(self,link):
		l = link.split('Report')[1]
		l = l[0:len(l)-3] #change .csv to .html
		l = l.replace('\\','/') #For firefox browser
		return 'http://cn-sha-rdfs01.apac.corp.natinst.com' + l + 'html'