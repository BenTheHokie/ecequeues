#!/usr/bin/env python

import cgi, cgitb
import sqlite3
import sys, re

cgitb.enable(display=0, logdir="/home/bwengert/logs/opel.log")
form = cgi.FieldStorage()

print "Content-Type: text/html\r\n\r\n"

try:
    number = form['phone'].value
    hashed = form['hash'].value
    carrier = form['carrier'].value
    if not any((number, hashed, carrier)):
	print "<html><head>\r\nThere's nothing here.\r\n</html></head>\r\n\r\n"
	sys.exit(0)
    if int(number) != float(number) or carrier not in ['v','a','s','t','vm'] or not re.match('^h[a-z|0-9]{10}$',hashed):
        raise
except:
    f = open('pissoff.html')
    r = f.read()
    f.close()
    print r+'\r\n\r\n'
    sys.exit(1)

print "<html><body>"

e=None
try:
    conn = sqlite3.connect('/home/bwengert/db/opel.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?)", (number, carrier, hashed))
    conn.commit()
    conn.close()
except Exception as e:
    print "{}: {}".format(type(e).__name__, e)
finally:
    if not e:
        print "everything worked."
    print "</body></html>\r\n\r\n"
