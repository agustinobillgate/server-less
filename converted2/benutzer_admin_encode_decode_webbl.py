#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
import random

def benutzer_admin_encode_decode_webbl(case_type:int, usercode:string, passwd:string):


    db_session = local_storage.db_session

    def generate_output():
        nonlocal case_type, usercode, passwd

        return {"usercode": usercode, "passwd": passwd}

    def decode_string():

        nonlocal case_type, usercode, passwd

        s:string = ""
        j:int = 0
        len_:int = 0
        s = usercode
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(usercode) - 1
        s = substring(usercode, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            passwd = passwd + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        passwd = substring(passwd, 4, (length(passwd) - 4))


    def encode_string():

        nonlocal case_type, usercode, passwd

        s:string = ""
        j:int = 0
        len_:int = 0
        ch:string = ""
        j = random.randint(1, 9)
        passwd = to_string(j) + passwd
        j = random.randint(1, 9)
        passwd = to_string(j) + passwd
        j = random.randint(1, 9)
        passwd = to_string(j) + passwd
        j = random.randint(1, 9)
        passwd = to_string(j) + passwd
        j = random.randint(1, 9)
        ch = chr_unicode(asc(to_string(j)) + 23)
        usercode = ch
        j = asc(ch) - 71
        for len_ in range(1,length(passwd)  + 1) :
            usercode = usercode + chr_unicode(asc(substring(passwd, len_ - 1, 1)) + j)
        passwd = ""

    if passwd == None:
        passwd = ""

    if case_type == 1:
        decode_string()

    elif case_type == 2:
        encode_string()

    return generate_output()