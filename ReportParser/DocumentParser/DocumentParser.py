__author__ = 'Administrator'
import csv
import copy
from ..Model import Test
import ConfigParser

class Parser(object):
    def isTestCase(self,line):
        return line[0] == "Test Case:"

    def isTestResult(self,line):
        return line[0] == "Test Result:"

    def retrieveTestName(self,listString):
        return listString[0].split(',')[1]

    def retrieveTestCase(self,line,T):
        TC = Test.TestCase()
        TC.CaseName=','.join(line[1:len(line)])
        T.TestCase.append(TC)

    def retrieveTestCaseResult(self,line,TC):
        TC.CaseResult = line[1]

    def retrieveTestResult(self,line,T):
        T.TestResult = line[1]

    def setTestState(self,T):
        if T.TestResult == "":
            if len(T.TestCase) != 0:
                T.TestResult = "Passed"
                for TC in T.TestCase:
                    if TC.CaseResult == 'Failed' and TC.CaseResult != 'Error'and TC.CaseResult != 'Avoided':
                        T.TestResult = 'Failed'
                    elif TC.CaseResult == 'Error'and TC.CaseResult != 'Avoided':
                        T.TestResult = 'Error'
                    elif TC.CaseResult == 'Avoided':
                        T.TestResult = 'Avoided'

                        
class FunctionalityParser(Parser):
    def F_Parse(self,documentString):
        listString = documentString.split('\n')
        FT = Test.TestWithoutTable() #FT means Functionality Test
        FT.TestName = self.retrieveTestName(listString)
        listString[0] = ''
        resultType = True # False for TestCase Result, True for Test Result
        reader = csv.reader(listString)
        for line in reader:
            if len(line)==0:
                continue
            else:
                if self.isTestCase(line):
                    self.retrieveTestCase(line,FT)
                    resultType = False
                elif self.isTestResult(line):
                    if resultType:
                        self.retrieveTestResult(line,FT)
                    else:
                        self.retrieveTestCaseResult(line,FT.TestCase[-1])
        self.setTestState(FT)
        return FT


class PerformanceParser(Parser):
    def P_Parse(self,documentString):
        PT = Test.TestWithTable()
        listString = documentString.split('\n')
        PT.TestName = self.retrieveTestName(listString)
        listString[0] = ''
        resultType = True # False for TestCase Result, True for Test Result
        reader = csv.reader(listString)
        table = {}
        l = [i for i in reader]
        #for i in reader:
        #    l.append(i)
        for i in range(0,len(l)):
            if len(l[i]) == 0:
                continue
            if self.__isTable(l[i]):
                for j in range(0,len(l[i])):
                    table[l[i][j].lower()] = l[i+1][j]
            else:
                if self.isTestCase(l[i]):
                    self.retrieveTestCase(l[i],PT)
                    PT.TestCase[-1].CaseTable = copy.copy(table)
                    table = {}
                    resultType = False
                elif self.isTestResult(l[i]):
                    if resultType:
                        self.retrieveTestResult(l[i],PT)
                        PT.TestTable = copy.copy(table)
                        table = {}
                    else:
                        self.retrieveTestCaseResult(l[i],PT.TestCase[-1])
        self.setTestState(PT)
        return PT

    def __isTable(self,line):
        return line[0] == 'Iteration '


class DocumentParser(object):
    def Parse(self,filename,date,type):
        self.SplitDocument(filename,date,type)
        self.doc.Link = filename
        if self.doc.DocumentType == 'Functionality':
            return self.FunctionalityDocumentParser()
        elif self.doc.DocumentType == 'Performance':
            return self.PerformanceDocumentParser()
        else:
            return self.RT_CertificationDocumentParser()

    def SplitDocument(self,filename,date,type):
        f = open(filename)
        list = f.read().split("Test Name:")
        self.doc = Test.Document()
        self.doc.DocumentName = list[0].split('\n')[0]
        self.doc.DocumentTime = date
        self.doc.DocumentType = type
        
        for i in range(1,len(list)):
            self.doc.TestString.append(list[i])
        self.doc.TestString[-1] = self.doc.TestString[-1].split('<results>')[0]

    def FunctionalityDocumentParser(self):
        F_Parser = FunctionalityParser()
        for testString in self.doc.TestString:
            self.doc.Test.append(F_Parser.F_Parse(testString))
        return self.doc

    def PerformanceDocumentParser(self):
        P_Parser = PerformanceParser()
        for testString in self.doc.TestString:
            self.doc.Test.append(P_Parser.P_Parse(testString))
        self.__setPerformanceResult()
        return self.doc

    def RT_CertificationDocumentParser(self):
        RT_Parser = PerformanceParser()
        baseline = 0
        for testString in self.doc.TestString:
            self.doc.Test.append(RT_Parser.P_Parse(testString))
            if "Baseline" in self.doc.Test[-1].TestName:
                baseline = float(self.doc.Test[-1].TestTable['max jitter (us)'])
        self.__setRT_CertificationResult(baseline)
        return self.doc

    def __setRT_CertificationResult(self,baseline):
        minBaseline = baseline / 10.0
        maxBaseline = baseline * 10.0
        for test in self.doc.Test:
            if 'max jitter (us)' in test.TestTable:
                if float(test.TestTable['max jitter (us)']) > minBaseline and float(test.TestTable['max jitter (us)']) <maxBaseline:
                    test.TestResult = 'Passed'

    def __setPerformanceResult(self):
        config = ConfigParser.ConfigParser()
        config.read('Configure.ini')
        sections = set(config.sections())
        for test in self.doc.Test:
            if (test.TestName in sections) and test.TestResult == 'Passed':
                for key in  config.options(test.TestName):
                    baseline = float(config.get(test.TestName,key))
                    minBaseline = baseline / 10
                    maxBaseline = baseline * 10
                    if float(test.TestTable[key]) < minBaseline or float(test.TestTable[key])>maxBaseline:
                        test.TestResult = 'Failed'
