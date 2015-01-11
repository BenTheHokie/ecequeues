from parsetime import parsetime
def data2dict(data): # extract data into a dictionary
    return {'time' : parsetime(data[0].string), 'room' : data[1].string , 'course' : data[2].string, 'vorq' : data[3].string.lower(), 'name' : data[4].string} # we parse the time into a datetime object so it can be subtracted from other times and formatted into text
