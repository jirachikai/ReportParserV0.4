__author__ = 'Administrator'
class Document(object):
    def __init__(self):
        self.DocumentName = ""
        self.DocumentType = ""
        self.DocumentTime = ""
        self.TestString = []
        self.Test = []
        self.Link = ""

        
class TestCase(object):
    def __init__(self):
        self.CaseName = ""
        self.CaseResult = ""
        self.CaseTable = {}

    def __str__(self):
        return self.CaseName+' '+self.CaseResult + ' ' + str(self.CaseTable)


class TestWithoutTable(object):
    def __init__(self):
        self.TestCase = []
        self.TestName = ""
        self.TestResult = ""

    def __str__(self):
        return self.TestName + ' ' + self.TestResult

    
class TestWithTable(object):
    def __init__(self):
        self.TestName = ""
        self.TestResult = ""
        self.TestTable = {}
        self.TestCase = []

    def __str__(self):
        return self.TestName + ' ' + self.TestResult + ' ' + str(self.TestTable)
