__author__ = 'Administrator'
class Daily(object):
	def __init__(self,docs):
		self.TableReport = self.__getTableReport(docs)
		self.BirdView = self.__getBirdView(self.TableReport)
		self.DetailedInformation = self.__getDetailedInformation(self.TableReport)

	def __getDate(self,D):
		DL = D.split('-')
		s = str(int(DL[1])) + '/' + str(int(DL[2])) + '/' + str(int(DL[0]))
		return s

	def __getTableReport(self,docs):
		TableReport = []
		color = {'Passed':"green" ,"Failed": "#993399", "Error":"red", "Avoided":"black"}
		for doc in docs:
			flag = True
			for test in doc.Test:
				tempList = {}
				tempList['#'] = str(len(TableReport)+1)
				tempList['DocumentName'] = doc.DocumentName
				tempList['DocumentLink'] = doc.Link
				tempList['TestName'] = test.TestName
				tempList['TestResult'] = test.TestResult
				tempList['RowSpan'] = '0'
				tempList['Color'] = "black"
				if test.TestResult: #maybe color is not exist
					tempList['Color'] = color[test.TestResult]
				if flag:
					flag = False
					tempList['RowSpan'] = str(len(doc.Test))
				TableReport.append(tempList)
		return TableReport

	def __getBirdView(self,TableReport):
		BirdView = {}
		BirdView['Passed'] = 0
		BirdView['Failed'] = 0
		BirdView['Avoided'] = 0
		BirdView['Total'] = 0
		for test in TableReport:
			if test['TestResult']!='Passed' and test['TestResult']!='Avoided':
				BirdView['Failed'] +=1
			else:
				if test['TestResult']:
					BirdView[test['TestResult']] +=1
			BirdView['Total'] += 1
		for i in BirdView:
			BirdView[i] = str(BirdView[i])
		return BirdView

	def __getDetailedInformation(self,TableReport):
		Detailed = {}
		Detailed['Passed'] = []
		Detailed['Failed'] = []
		Detailed['Error'] = []
		Detailed['Avoided'] = []
		Detailed['Total'] = []
		Detailed['Crashed'] = []
		for test in TableReport:
			if test['TestResult'] in Detailed:
				Detailed[test['TestResult']].append(['0',test['DocumentName'],test['TestName'],test['DocumentLink']])
			else:
				Detailed['Crashed'].append(['0',test['DocumentName'],test['TestName'],test['DocumentLink']])
		for testType in Detailed:
			count = 0
			lastIndex = 0
			if Detailed[testType]:
				lastDocLink = Detailed[testType][0][3]
			for i in range(0,len(Detailed[testType])):
				if Detailed[testType][i][3] == lastDocLink:
					count+=1
					if i == len(Detailed[testType])-1:
						Detailed[testType][lastIndex][0] = str(count)
				else:
					Detailed[testType][lastIndex][0] = str(count)
					if i == len(Detailed[testType])-1:
						Detailed[testType][i][0] = "1"
					count=1
					lastIndex=i
					lastDocLink=Detailed[testType][i][3]			
		return Detailed

