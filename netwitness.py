"""
This module parse useful data from RSA NetWitness Rules. That's usually unreadable, contains byte code.
My development environment is RSA NetWitness 10.6.0.1. Maybe you can read the other version too.
Please tell me if you happen any problem. I welcome for your comment.
Thank you.
"""
from pathlib import *
from pprint import pprint
import json


__end_rulename = 0
__end_fullpath = 0
__end_select = 0
__end_where = 0
__end_mode = 0
__end_order = 0
__end_then = 0


def __read_rules(path):
    """read all rule's bytes in the path"""
    p_list = Path(path).glob("*")
    p_list = [p for p in p_list]
    return [p.read_bytes() for p in p_list]


def __get_rulename(b):
    global __end_rulename
    start_rulename = 2
    __end_rulename = start_rulename + b[start_rulename-1]
    return b[start_rulename: __end_rulename].decode()


def __get_fullpath(b):
    global __end_rulename, __end_fullpath
    start_fullpath = __end_rulename + 4
    __end_fullpath = start_fullpath + b[start_fullpath-1]
    return b[start_fullpath: __end_fullpath].decode()


def __get_select(b):
    global __end_fullpath, __end_select
    start_select = __end_fullpath + b[__end_fullpath:].find(0x0a) + 2  # find(0x0a) because that's Variable Length
    __end_select = start_select + b[start_select-1]
    return b[start_select: __end_select].decode()


def __get_where(b):
    global __end_select, __end_where
    start_where = __end_select + 2
    if b[start_where] < 0x20:  # sometimes, there is 1 byte after length byte. I don't know why.
        start_where += 1
    __end_where = start_where + b[start_where:].find(0x1a)  # where string end mark is '0x1a'
    return b[start_where: __end_where].decode()


def __get_mode(b):
    global __end_where, __end_mode
    start_mode = __end_where + 2
    __end_mode = start_mode + b[start_mode-1]
    return b[start_mode: __end_mode].decode()


def __get_order(b):
    global __end_mode, __end_order
    j = []
    start_order = __end_mode
    __end_order = __end_mode
    while (b[start_order:].find(bytes([0x22])) != -1):
        start_order += b[start_order:].find(bytes([0x22])) + 4
        __end_order = start_order + b[start_order-1]
        r = b[start_order: __end_order].decode()
        r += " ASC" if b[__end_order+1] == 0x00 else " DSC"
        j.append(r)
        if b[start_order + b[start_order-1] + 2] != 0x22:
            break
    return j


def __get_then(b):
    global __end_order, __end_then
    r = []
    start_then = __end_order
    __end_then = __end_order
    while b[start_then:].find(bytes([0x3a])) != -1:
        start_then += b[start_then:].find(bytes([0x3a])) + 2
        __end_then = start_then + b[start_then-1]
        r.append(b[start_then: __end_then].decode())
    return r


def __get_group(b):
    global __end_then
    r = []
    start_group = __end_then
    end_group = __end_then
    while b[start_group:].find(bytes([0x5a])) != -1:
        start_group += b[start_group:].find(bytes([0x5a])) + 2
        end_group = start_group + b[start_group-1]
        t = b[start_group: end_group].decode()
        if len(t) > 0:
            r.append(t)
    return r


def __get_alignment(b):
    """method call order is absolute. this module use global variable :("""
    try:
        r = {
                'RULE'   : __get_rulename(b),
                'PATH'   : __get_fullpath(b),
                'SELECT' : __get_select(b),
                'WHERE'  : __get_where(b),
                'MODE'   : __get_mode(b),
                'ORDERBY': __get_order(b),
                'THEN'   : __get_then(b),
                'GROUPBY': __get_group(b)
                }
    except Exception as e:
        print("Error: %s" % __get_fullpath(b))
        print("-------------------------------")
        print(e.args)
        r = {}
    return r


def read_rules(path="D:/Downloads/RULES", out=""):
    titles = ["RULE","PATH","SELECT","WHERE","MODE","GROUPBY","ORDERBY","THEN"]
    o = []
    if out == "":
        for b in __read_rules(path):
            r = __get_alignment(b)
            t = ""
            for title in titles:
                t += "%s\t:%s\n" % (title, r[title])
            o.append(t)
        [print(s) for s in set(o)]
    else:
        for b in __read_rules(path):
            r = __get_alignment(b)
            o.append("%s\n" % json.dumps(r, ensure_ascii=False))
        with open(out, "a") as f:
            o = set(o)
            for line in o:
                f.write(line)


if __name__ == "__main__":
    read_rules()