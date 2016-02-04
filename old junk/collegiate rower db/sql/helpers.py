import re
from types import *

def sub(item):
    return re.sub(u'[\n\t]+', u'', item).strip()

def quotify(s):
    if type(s) == NoneType:
        return u'""'
    elif type(s) == ListType:
        return [quotify(x) for x in s]
    elif type(s) == DictType:
        temp = {}
        for key in s:
            temp[key] = quotify(s[key])
        return temp
    elif type(s) != UnicodeType:
        s = unicode(s)
    return u'"' + sub(s).strip() + u'"'
