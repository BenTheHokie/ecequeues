from parsetime import parsetime

def getcont(bso):
    '''
    @param bso:
    Beautiful soup object
    '''
    return ''.join([unicode(s) for s in bso.contents])

def data2dict(data): # extract data into a dictionary
    return {
	    'time' : parsetime(getcont(data[0])), 
	    'room' : getcont(data[1]), 
	    'course' : getcont(data[2]), 
	    'vorq' : getcont(data[3]).lower(), 
	    'name' : getcont(data[4])
	   } 
    
    # we parse the time into a datetime object so it can be 
    # subtracted from other times and formatted into text
