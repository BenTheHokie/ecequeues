import datetime
def parsetime(timestr): # Turn a string into a time
    return datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S') # Takes input in the style of the OpEL output eg, 2014-09-23 19:24:59
