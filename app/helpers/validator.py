import re

def isValidEmail(email):
    res = re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email)
    return False if res==None else True
    

def isValidText(value):
    res = re.match("^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$", value)
    return False if res==None else True

def isNotXSSFormat(value):
    res = re.match("<([A-Za-z_{}()/]+(\s|=)*)+>(.*<[A-Za-z/>]+)*", value)
    return True if res==None else False

def isNum(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

def isValidCoordinates(value):
    list = value.split(sep=', ')
    if(not ((len(list) == 2) and (isNum(list[0])) and (isNum(list[1])))):
        return False
    return True

def isPhoneNumber(value):
    list = value.split(sep='-')
    if(not ((len(list) == 2) and (isNum(list[0])) and (isNum(list[1])))):
        return False
    if(not (len(value) < 20)):
        return False
    return True

#print(isNotXSSFormat("<img />"))