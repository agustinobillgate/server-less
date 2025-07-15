#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener

def pswd_validation_cldbl(user_name:string, inp_pswd:string):
    pswd_ok = False
    pswd_level = 0
    heute:date = None
    sindata_pswd:string = ""
    dd_str:string = ""
    mm_str:string = ""
    yy_str:string = ""
    nr:int = 0
    dd:int = 0
    tot_digit:int = 0
    tot_special:int = 0
    tot_char:int = 0
    curr_i:int = 0
    tot_lower_char:int = 0
    tot_upper_char:int = 0
    month_str:List[string] = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "FalseV", "DEC"]
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, tot_lower_char, tot_upper_char, month_str, bediener
        nonlocal user_name, inp_pswd

        return {"pswd_ok": pswd_ok, "pswd_level": pswd_level}

    def check_pswd_strength(in_passwd:string):

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_char, curr_i, tot_lower_char, tot_upper_char, month_str, bediener
        nonlocal user_name, inp_pswd

        pswd_level = 0
        upper_case:List[string] = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "j", "K", "L", "M", "N", "O", "P", "Q", "R", "s", "T", "U", "V", "W", "X", "Y", "Z"]
        lower_case:List[string] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        numbers:List[string] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        strstatus:string = " "
        pointer:string = ""
        tot_up:int = 0
        tot_low:int = 0
        tot_num:int = 0
        tot_special:int = 0
        i:int = 0
        index1:int = 0
        longer:int = 0
        intscore:int = 0

        def generate_inner_output():
            return (pswd_level)

        longer = length(in_passwd)

        if longer < 4:
            intscore = intscore + 3

        elif longer > 5 and longer < 7:
            intscore = intscore + 6

        elif longer > 8 and longer < 15:
            intscore = intscore + 12

        elif longer > 16:
            intscore = intscore + 18
        for i in range(1,longer + 1) :
            for index1 in range(1,26 + 1) :
                pointer = substring(in_passwd, i - 1, 1)

                if pointer == upper_case[index1 - 1]:
                    tot_up = tot_up + 1

                elif matches(pointer,lower_case[index1 - 1]):
                    tot_low = tot_low + 1
        for i in range(1,longer + 1) :
            for index1 in range(1,10 + 1) :
                pointer = substring(in_passwd, i - 1, 1)

                if matches(pointer,numbers[index1 - 1]):
                    tot_num = tot_num + 1
        tot_special = longer - (tot_up + tot_low + tot_num)

        if tot_up == 0 and tot_low == 0:
            intscore = intscore + 0

        elif tot_up == 0 and tot_num == 0 and tot_special == 0:
            intscore = intscore + 5

        elif tot_up != 0 and tot_low != 0:
            intscore = intscore + 7

        if tot_num == 0:
            intscore = intscore + 0

        elif tot_num == 1:
            intscore = intscore + 5

        elif tot_num > 3:
            intscore = intscore + 7

        if tot_special == 0:
            intscore = intscore + 0

        elif tot_special == 1:
            intscore = intscore + 5

        elif tot_special > 1:
            intscore = intscore + 10

        if tot_up != 0 and tot_num != 0 or tot_low != 0 and tot_num != 0:
            intscore = intscore + 1

        if tot_up != 0 and tot_low != 0:
            intscore = intscore + 1

        if tot_up != 0 and tot_num != 0 and tot_special != 0 or tot_low != 0 and tot_num != 0 and tot_special != 0:
            intscore = intscore + 2

        if tot_up != 0 and tot_num != 0 and tot_special != 0 and tot_low != 0:
            intscore = intscore + 2

        if intscore < 16:
            pswd_level = 1

        elif intscore > 15 and intscore < 25:
            pswd_level = 2

        elif intscore > 24 and intscore < 35:
            pswd_level = 3

        elif intscore > 34 and intscore < 45:
            pswd_level = 4
        else:
            pswd_level = 5

        return generate_inner_output()


    def decode_usercode():

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, tot_lower_char, tot_upper_char, month_str, bediener
        nonlocal user_name, inp_pswd

        nr = -1
        found:bool = False
        passwd:string = ""
        usr = None

        def generate_inner_output():
            return (nr)

        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (Usr.username == (user_name).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1)).first()
        while None != usr and not found:
            passwd = decode_string1(usr.usercode)

            if passwd.lower()  == (inp_pswd).lower() :
                nr = usr.nr
                found = True
            else:

                curr_recid = usr._recid
                usr = db_session.query(Usr).filter(
                         (Usr.username == (user_name).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1) & (Usr._recid > curr_recid)).first()

        return generate_inner_output()


    def decode_string1(in_str:string):

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, tot_lower_char, tot_upper_char, month_str, bediener
        nonlocal user_name, inp_pswd

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()

    if length(inp_pswd) < 10:
        pswd_level = -1

        return generate_output()
    for curr_i in range(1,length(inp_pswd)  + 1) :

        if substring(inp_pswd, curr_i - 1, 1) >= ("0").lower()  and substring(inp_pswd, curr_i - 1, 1) <= ("9").lower() :
            tot_digit = tot_digit + 1

        elif asc(substring(inp_pswd, curr_i - 1, 1)) >= asc("a") and asc(substring(inp_pswd, curr_i, 1)) <= asc("z"):
            tot_lower_char = tot_lower_char + 1

        elif asc(substring(inp_pswd, curr_i - 1, 1)) >= asc("A") and asc(substring(inp_pswd, curr_i, 1)) <= asc("Z"):
            tot_upper_char = tot_upper_char + 1
        else:
            tot_special = tot_special + 1

    if tot_digit < 2 or tot_special == 0 or tot_upper_char == 0 or tot_lower_char == 0:
        pswd_level = -2

        return generate_output()
    pswd_ok = True


    pswd_level = check_pswd_strength(inp_pswd)

    return generate_output()