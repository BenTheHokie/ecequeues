#!/usr/bin/env python

import sys
sys.path.append('/home/bwengert/lib')

from parse import parse
from threading import Timer
from hashlib import md5
from time import strftime
from sanitize import scrubhtml


def hash_it(s):
    m = md5()
    m.update(s)
    return m.hexdigest()[-10:]

def update(prevu):
    with open('head.html') as f:
        final = f.read()
    with open('body.html') as f:
        body = f.read()

    users = parse('page.htm')
    for u in users:
        tstr = u['time'].strftime("%Y-%m-%d %H:%M:%S")
        final += body.format(
            name = scrubhtml(u['name']),
            clas = scrubhtml(u['course']), # python keywords prevent using of class
            room = scrubhtml(u['room']),
            vorq = scrubhtml(u['vorq']),
            time = scrubhtml(tstr),
            smhash = hash_it(tstr+u['name'])
            )

    final += "              <!-- Updated {}-->\n".format(strftime("%x %X"))
    with open('tail.html') as f:
        final += f.read()

    f = open('index.html', 'w')
    f.write(final)
    f.close()


    print strftime("%x %X: Updated...")
    t = Timer(20, update, args=(users[:],))
    t.start()


update(parse('page.htm'))
