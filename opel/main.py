#!/usr/bin/env python

import sys
sys.path.append('/home/bwengert/lib')

from parse import parse
from threading import Timer
from hashlib import md5
from time import strftime
from sanitize import scrubhtml
from textmachine import texter
from getpass import getuser


def hash_it(s):
    m = md5()
    m.update(s)
    return m.hexdigest()[-10:]

def getelapsed(td): # must pass in a datetime.timedelta object
    r = td.seconds # remainder
    secs = td.seconds % 60
    
    r/=60
    mins = r % 60

    r/=60
    hrs = r + td.days*24

    return "%d:%s%d:%s%d" % (hrs, '0'*(mins<10), mins, '0'*(secs<10), secs)

def tfmt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def update(prevu):
    global txt
    with open('head.html') as f:
        final = f.read()
    with open('body.html') as f:
        body = f.read()

    users = parse('page.htm')
    for i in range(len(users)):
        tstr = tfmt(users[i]['time'])
	users[i]['hash'] = hash_it(tstr+users[i]['name'])
	final += body.format(
            name = scrubhtml(users[i]['name']),
            clas = scrubhtml(users[i]['course']), # python keywords prevent using of class
            room = scrubhtml(users[i]['room']),
            vorq = scrubhtml(users[i]['vorq']),
            time = scrubhtml(tstr),
            smhash = users[i]['hash']
            )

    final += "              <!-- Updated {}-->\n".format(strftime("%x %X"))
    with open('tail.html') as f:
        final += f.read()

    f = open('index.html', 'w')
    f.write(final)
    f.close()

    for i in range(len(prevu)):
	try:
	    newidx = users.index(prevu[i])
	    if i != newidx:
		print "Name {} switched from pos {} to {}".format(prevu[i]['name'], i, newidx)
		txt.addmsg(u'h'+prevu[i]['hash'], 0,
		    {
			'qname' :   'OpEL',
			'currtime': strftime('%a %m/%d %I:%M:%S %p'),
			'name':	    prevu[i]['name'],
			'frm':	    i,
			'to':	    newidx,
			'elapsed':  getelapsed(prevu[i]['time'].now()-prevu[i]['time'])
		    })
	except ValueError:
	    print "Name {} has been removed".format(prevu[i]['name'])

    txt.sendall()
    print strftime("%x %X: Updated...")
    t = Timer(20, update, args=(users[:],))
    t.start()

if __name__ == '__main__':
    global txt
    txt = texter('/home/%s/db/opel.db' % ('bwengert' if getuser()=='www-data' else getuser()))
    users = parse('page.htm')
    for i in range(len(users)):
	tstr = tfmt(users[i]['time'])
	users[i]['hash']=hash_it(tstr+users[i]['name'])

    update( users )
