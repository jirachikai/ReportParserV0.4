__author__ = 'Administrator'
from ReportParser.AccessFile import AccessFile
from ReportParser.DocumentParser import DocumentParser
from ReportParser.DataBase import DBWriter,DBReader
from datetime import *

def getDate(Date):
	Date = Date.split('_')[0]
	return Date[0:4] + '-' + Date[4:6] + '-' + Date[6:8]

def countPassed(Doc):
	passed = 0
	for test in Doc.Test:
		if test.TestResult == 'Passed':
			passed += 1
	return passed

def getBirdView(Date,productName):
	DBR = DBReader.DBReader()
	reportDate = ReadReportDate(Date,productName)
	singleDayDocs = DBReader.ReadSingleDay(reportDate,productName)
	total = 0
	passed = 0
	for doc in singleDayDocs:
		total += len(doc.Test)  # Total Test
		passed += countPassed(doc)# Passed Test
	return total,passed
	
def deal(productName):
	GFP = AccessFile.GetFilePath()
	pathInfo = GFP.get(productName)# {key:folder val:{ key:testType val:filepath_list}}
	DocList = []
	DBW = DBWriter.DBWriter()
	BirdView = {}
	for dateFolder in sorted(pathInfo.keys()):
		#print '------------------------------------------------------------'
		d = getDate(dateFolder)
		BirdView[d] = [0,0]
		for testType in pathInfo[dateFolder]:
			if pathInfo[dateFolder][testType]:
				for csvfile in pathInfo[dateFolder][testType]:
					#print '***********************************'
					DP = DocumentParser.DocumentParser()
					doc = DP.Parse(csvfile,dateFolder,testType)
					BirdView[d][0] += len(doc.Test)  # Total Test
					BirdView[d][1] += countPassed(doc) #Passed Test
					#DP.TestFun_print()
					DBW.WriteSingleDay(doc,productName)
	for date in BirdView:
		DBW.WriteBirdsView(date,BirdView[date][0],BirdView[date][1],productName)
	
deal("FRC")	
print("OK")

