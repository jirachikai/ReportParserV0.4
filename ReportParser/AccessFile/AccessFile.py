__author__ = 'Administrator'
import configparser
import sqlite3,os
DBPath = "Result.db"
class GetFilePath(object):
	def get(self,productName):
		os.system("net use \\\\cn-sha-rdfs01 welcome /user:apac\\testfarm")
		config = configparser.ConfigParser()
		config.read('TestInfo.ini')
		pathInfo = self.__getSinglePath(config.get('reportPath',productName))
		reportCategory = self.__getReportCategory(productName)
		if type(reportCategory) is type(''):
			return self.__specificCategory(reportCategory,pathInfo)
		classfiedDict = self.__fileClassify(reportCategory,pathInfo)
		return classfiedDict
		
	def __getReportCategory(self,productName):
		config = configparser.ConfigParser()
		config.read('TestInfo.ini')
		testCategory = {}
		if config.has_option('Functionality',productName):
			testCategory['Functionality'] = self.__getOption(config,'Functionality',productName)
			if testCategory['Functionality'] == "*":
				return "Functionality"
		if config.has_option('Performance',productName):
			testCategory['Performance'] = self.__getOption(config,'Performance',productName)
			if testCategory['Performance'] == "*":
				return "Performance"
		if config.has_option('RT_Certification',productName):
			testCategory['RT_Certification'] = self.__getOption(config,'RT_Certification',productName)
			if testCategory['RT_Certification'] == "*":
				return "RT_Certification"
		return self.__inverseTable(testCategory)
	
	def __getOption(self,config,section,productName):
		option = config.get(section,productName)
		if option == "*":
			return "*"
		else:
			return eval(option)
	
	def __inverseTable(self,reportCategory):
		inverse = {}
		for category in reportCategory:
			for file in reportCategory[category]:
				inverse[file] = category
		return inverse
	
	def __fileClassify(self,inverseReportCategory,fileList):
		finalDict = {}# {key:folder val:{ key:category val:filepath_list}}
		for folder in fileList:
			finalDict[folder] = {"Functionality":[], "Performance":[], "RT_Certification":[]}
			for filePath in fileList[folder]:
				fileTitle = self.__getFileTitle(filePath)
				for configReport in inverseReportCategory:
					if configReport == fileTitle:
						finalDict[folder][inverseReportCategory[configReport]].append(filePath) 
		return finalDict
		
	def __specificCategory(self,category,fileList):
		finalDict = {}# {key:folder val:{ key:category val:filepath_list}}
		for folder in fileList:
			finalDict[folder] = {category:[]}
			for filePath in fileList[folder]:
				finalDict[folder][category].append(filePath) 
		return finalDict
		
	def __getFileTitle(self,filePath):
		f = open(filePath)
		title = f.readline().split('\n')[0]
		f.close()
		return title
	
	def __getSinglePath(self,path):
		lastState = self.__getLastState(path)
		fileList = os.listdir(path)
		flag = True
		if lastState==0:
			flag = False
		fileDict = {}
		for file in fileList:
			if flag and file == lastState:
				flag = False # Find the last file in last deal time
			elif flag == False:
				fileDict[file] = self.__getAllFile(path+'/'+file)
		self.__updateLastState(path,fileList[-1])
		return fileDict

	def __getAllFile(self,fileName):
		fileList = []
		for file in os.listdir(fileName):
			if os.path.isdir(fileName+'/'+file):
				for fileIn in os.listdir(fileName+'/'+file):
					if self.__isValidFile(fileIn):
						fileList.append(fileName+'/'+file+'/'+fileIn)
		return fileList
	
	def __isValidFile(self,fileName):
		return '.csv' in fileName
	
	def __getLastState(self,key):
		conn = sqlite3.connect(DBPath)
		cursor = conn.execute('SELECT Val FROM State WHERE Key=?',(key,))
		line = cursor.fetchone()
		if line:
			conn.close()
			return line[0]
		else:
			conn.execute('INSERT INTO State VALUES(?,?)',(key,'Start'))
			conn.commit()
			conn.close()
			return 0
	
	def __updateLastState(self,key,newVal):
		conn = sqlite3.connect(DBPath)
		conn.execute('UPDATE State SET Val=? WHERE Key=?',(newVal,key,))
		conn.commit()
		conn.close()
