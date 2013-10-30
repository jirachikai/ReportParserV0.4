import socket,os,ParserMain,time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('sh-rd-lvrhost', 8001))  
sock.listen(5)  
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
	except socket.timeout:  
		print ('time out')  
connection.close()  