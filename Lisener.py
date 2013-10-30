import socket,os,ParserMain,time,logging
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('sh-rd-lvrhost', 8001))  
sock.listen(5)  
def writeLog(filePath,errorMessage):
	logger = logging.getLogger("database")
	formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',) 
	file_handler = logging.FileHandler(filePath) 
	file_handler.setFormatter(formatter) 
	logger.addHandler(file_handler)  
	logger.error(errorMessage)
	logger.removeHandler(file_handler) 
	
while True:  
	connection,address = sock.accept()  
	try:  
		connection.settimeout(5)  
		buf = connection.recv(1024)
		#os.system("python " + '"F:/myRIO,FRC ReportParser/'+buf.decode("utf-8")+'.py"')
		#exec("import "+buf.decode("utf-8"))
		ParserMain.deal(buf.decode("utf-8"))
		print (buf.decode("utf-8") + " is done well")
		f = open("Trigger_History.txt",'a')
		f.write(buf.decode("utf-8") + ' '+ time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+'\n')
		connection.send(b'OK')  
		f.close()
	except Exception as err:  
		print ('time out')  
		writeLog("Logging.log",str(err))
connection.close()  