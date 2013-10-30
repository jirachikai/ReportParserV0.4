__author__ = 'Administrator'
import sqlite3
conn = sqlite3.connect("Result.db")
conn.execute("DELETE FROM BirdsView")
conn.execute('DELETE FROM DailyTest')
conn.execute('DELETE FROM Result')
conn.execute('DELETE FROM State')
conn.execute('UPDATE sqlite_sequence SET seq = 0')
conn.commit()
conn.close()