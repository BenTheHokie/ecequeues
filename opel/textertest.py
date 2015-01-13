#!/usr/bin/env python
from textmachine import texter
t=texter("/home/ben/Documents/opel.db")
t.addmsg("h15a464ddac",0,{'qname':'opel', 'currtime':'4:17', 'name':'ben', 'frm':'3', 'to':'2', 'elapsed':'1:23:43'})
t.sendall()
