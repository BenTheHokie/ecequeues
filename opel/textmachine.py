from threading import Thread
from smtplib import SMTP as smtp
import sqlite3
import time
from emaillogin import emaillogin
from time import strftime

email = emaillogin()

class texter:
    def __init__(self, 
		db, 
		msgs = [    u'{qname} {currtime}\r\n{name} has moved from position {frm} to {to}. Elapsed: {elapsed}', 
			    u"{qname} {currtime}\r\n{name} has been removed from the queue. Elapsed {elapsed}",
			    u'{qname} {currtime}\r\n{name} is in position {pos}. Elasped {elapsed}'
		       ]
	    ):
	
	self._db = db
	self._sendq = []
	self.msgs = msgs

    def strtime(self, t = time.localtime()):
	return time.strftime('%a %m/%d %I:%M:%S %p', t)

    def printable(self, s):
	r = {'\r' : '\\r', '\n' : '\\n'}
	for c in r.keys():
	    s = s.replace(c, r[c])
	
	return s

    def _sendall(self, q):
	domains = { 't' :   '@tmomail.net',
		    'v' :   '@vtext.com',
		    'a' :   '@txt.att.net',
		    's' :   '@messaging.sprintpcs.com',
		    'vm':   '@vmobl.com'
		  }
	client = smtp("smtp.gmail.com", 587)
	client.ehlo()
	client.starttls()
	client.login(email.user, email.pwd)

	for m in q:
	    print strftime("%x %X: ")+self.printable("TO: %s:"%m['number']+m['msg'])
	    to = m['number']+domains[m['carrier']]
	    headers = "To:%s\r\nFrom:%s\r\n\r\n" % (to, email.user)
	    client.sendmail(email.user , to , headers + m['msg'] )
	
	client.close()
	print strftime("%x %X: Sent all...")

    def sendall(self):
	if len(self._sendq) > 0:
	    sthread = Thread( target = self._sendall , args = (self._sendq[:],) )
	    self._sendq = []
	    sthread.start()
	
    def addmsg(self, uhash, msg, data, rm = False):
	conn = sqlite3.connect(self._db)
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE hash=?", (uhash,) )
	phones = c.fetchall()
	
	for p in phones:
	    appval = { 'number' : p[0] , 'carrier' : p[1] }
	    appval['msg'] = self.msgs[msg].format(**data)
	    
	    self._sendq.append(appval)
	
	if rm:
	    c.execute("DELETE FROM users WHERE hash=?", (uhash,) )
	    conn.commit()
	
