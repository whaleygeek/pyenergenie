'''
Created on 15 Oct 2015

@author: ed
'''
def toHexListString(buf):
    result = '['
    for b in buf:
        if len(result) > 1:
            result += ','
        result += hex(b)
    return result + ']'

