__author__ = 'Administrator'
import tornado.ioloop
import tornado.web
import tornado.httpserver
from ReportParser.DataBase import DBReader
from datetime import *
import os,InformationClean,logging
from tornado.options import options 
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/([0-9a-zA-Z]+)/Daily/([0-9]+_[0-9]+)",DailyHandler),
			(r"/([0-9a-zA-Z]+)/Date/([0-9]+\-[0-9]+\-[0-9]+)",DateHandler),
			(r"/([0-9a-zA-Z]+)/ChooseDate",ChooseDateHandler),
			(r"/([0-9a-zA-Z]+)/Today",TodayHandler),
			(r"/([0-9a-zA-Z]+)/Yesterday",YesterdayHandler),
			(r"/([0-9a-zA-Z]+)/Period/([0-9]+\-[0-9]+\-[0-9]+)/([0-9]+\-[0-9]+\-[0-9]+)",PeriodHandler),
			(r"/([0-9a-zA-Z]+)/Monthly",MonthlyHandler),
			(r"/",IndexHandler),
		]
		settings = dict(
			static_path = os.path.join(os.path.dirname(__file__),"static"),
			template_path = os.path.join(os.path.dirname(__file__),"template"),
		)
		tornado.web.Application.__init__(self,handlers,**settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		logging.info("**Request to IndexHandler!")
		self.render("Index.html")		
		
		
class DailyHandler(tornado.web.RequestHandler):
	def get(self,productName,date):
		logging.info("**Request to DailyHandler!"+productName+"  "+date)
		DBR = DBReader.DBReader()
		docs = DBR.ReadSingleDay(date,productName)
		IC = InformationClean.Daily(docs)
		self.render("DatePage.html",productName = productName,BV = IC.BirdView,date = date,report = IC.TableReport,DI = IC.DetailedInformation)

		
class DateHandler(tornado.web.RequestHandler):
	def get(self,productName,date):
		logging.info("**Request to DateHandler!"+productName+"  "+date)
		DBR = DBReader.DBReader()
		reportDate = DBR.ReadReportDate(date,productName)
		if reportDate:
			self.redirect('/'+productName+'/Daily/'+reportDate)
		else:
			self.render('Wrong.html',date = date,productName = productName)

			
class ChooseDateHandler(tornado.web.RequestHandler):
	def post(self,productName):
		logging.info("**Request to ChooseDateHandler!" + productName)
		date = self.get_argument('Date')
		if date == "":
			self.render('Wrong.html',date = date,productName = productName)
		else:
			self.redirect('/'+productName+'/Date/'+self.__formatDate(date))
			
	def __formatDate(self,date):
		MDY = date.split('/')# Change Month-Day-year to Year-Month-Day
		return str(int(MDY[2]))+'-'+str(int(MDY[0]))+'-'+str(int(MDY[1]))

		
class TodayHandler(tornado.web.RequestHandler):
	def get(self,productName):
		logging.info("**Request to TodayHandler!"+productName)
		today = str(datetime.today()).split(' ')[0]
		self.redirect('/'+productName+'/Date/'+today)
		
		
class YesterdayHandler(tornado.web.RequestHandler):
	def get(self,productName):
		logging.info("**Request to YesterdayHandler!")
		yesterday = str(datetime.today()-timedelta(days = 1,seconds =0, microseconds = 0)).split(' ')[0]
		self.redirect('/'+productName+'/Date/'+yesterday)

		
class PeriodHandler(tornado.web.RequestHandler):
	def get(self,productName,startDate,endDate):
		logging.info("**Request to PeriodHandler!"+productName+"  "+startDate+"  "+endDate)
		DBR = DBReader.DBReader()
		Total_Passed_Date_Link = DBR.ReadPeriodDays(startDate,endDate,productName)
		total = Total_Passed_Date_Link[0]
		ticks = Total_Passed_Date_Link[2]
		for i in range (0,len(total)):
			total[i] = str(total[i])
		passed = [str(i) for i in Total_Passed_Date_Link[1]]
		date = startDate + '  To  ' + endDate
		self.render("MonthlyReport.html",date = date,productName = productName,passed = passed,total = total,ticks = ticks,link = Total_Passed_Date_Link[3])

		
class MonthlyHandler(tornado.web.RequestHandler):
	def get(self,productName):
		logging.info("**Request to MonthlyHandler!"+productName)
		today = str(datetime.today()).split(' ')[0]# datetime.today() get "Y-M-D  M-S-MS" Format
		start = str(datetime.today() - timedelta(days = 30,seconds =0, microseconds = 0)).split(' ')[0]
		self.redirect('/'+productName+'/Period/'+start+'/'+today)
		
		
if __name__ =="__main__":
	http_server = tornado.httpserver.HTTPServer(Application())
	tornado.options.parse_command_line()  
	http_server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()