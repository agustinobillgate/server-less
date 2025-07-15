from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener

def pswd_validation(user_name:str, inp_pswd:str):
    pswd_ok = False
    pswd_level = 0
    heute:date = None
    sindata_pswd:str = ""
    dd_str:str = ""
    mm_str:str = ""
    yy_str:str = ""
    nr:int = 0
    dd:int = 0
    tot_digit:int = 0
    tot_special:int = 0
    tot_char:int = 0
    curr_i:int = 0
    month_str:List[str] = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "FalseV", "DEC"]
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, month_str, bediener
        nonlocal user_name, inp_pswd

        return {"pswd_ok": pswd_ok, "pswd_level": pswd_level}

    def check_pswd_strength(pass:str):

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_char, curr_i, month_str, bediener
        nonlocal user_name, inp_pswd

        pswd_level = 0
        upper_case:List[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "j", "K", "L", "M", "N", "O", "P", "Q", "R", "s", "T", "U", "V", "W", "X", "Y", "Z"] CASE_SENSITIVE
        lower_case:List[str] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"] CASE_SENSITIVE
        numbers:List[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] CASE_SENSITIVE
        strstatus:str = " "
        pointer:str = ""
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

        longer = len(pass)

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
                pointer = substring(pass, i - 1, 1)

                if pointer == upper_case[index1 - 1]:
                    tot_up = tot_up + 1

                elif re.match(lower_case[index1 - 1],pointer, re.IGNORECASE):
                    tot_low = tot_low + 1
        for i in range(1,longer + 1) :
            for index1 in range(1,10 + 1) :
                pointer = substring(pass, i - 1, 1)

                if re.match(numbers[index1 - 1],pointer, re.IGNORECASE):
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

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, month_str, bediener
        nonlocal user_name, inp_pswd

        nr = -1
        found:bool = False
        passwd:str = ""
        usr = None

        def generate_inner_output():
            return (nr)

        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (func.lower(Usr.username) == (user_name).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1)).first()
        while None != usr and not found:
            passwd = decode_string1(usr.usercode)

            if passwd.lower()  == (inp_pswd).lower() :
                nr = usr.nr
                found = True
            else:

                curr_recid = usr._recid
                usr = db_session.query(Usr).filter(
                         (func.lower(Usr.username) == (user_name).lower()) & (Usr.flag == 0) & (Usr.betriebsnr == 1) & (Usr._recid > curr_recid)).first()

        return generate_inner_output()


    def decode_string1(in_str:str):

        nonlocal pswd_ok, pswd_level, heute, sindata_pswd, dd_str, mm_str, yy_str, nr, dd, tot_digit, tot_special, tot_char, curr_i, month_str, bediener
        nonlocal user_name, inp_pswd

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))

        return generate_inner_output()

    if user_name.lower()  == ("Sindata").lower() :
        heute = get_current_date()
        dd = get_day(heute)
        mm_str = month_str[get_month(heute) - 1]
        yy_str = to_string(get_year(heute))
        yy_str = substring(yy_str, 3, 1) + substring(yy_str, 2, 1) +\
                substring(yy_str, 1, 1) + substring(yy_str, 0, 1)

        if dd == 1 or dd == 21 or dd == 31:
            dd_str = to_string(dd, "99") + "st"

        elif dd == 2 or dd == 22:
            dd_str = to_string(dd, "99") + "nd"

        elif dd == 3 or dd == 23:
            dd_str = to_string(dd, "99") + "rd"
        else:
            dd_str = to_string(dd, "99") + "th"
        sindata_pswd = "*" + dd_str + mm_str + yy_str + "#"
        pswd_ok = inp_pswd == sindata_pswd

        if pswd_ok:

            return generate_output()
        nr = decode_usercode()

        if nr <= 0:

            return generate_output()

    if len(inp_pswd) < 10:
        pswd_level = -1

        return generate_output()
    for curr_i in range(1,len(inp_pswd)  + 1) :

        if substring(inp_pswd, curr_i - 1, 1) >= ("0").lower()  and substring(inp_pswd, curr_i - 1, 1) <= ("9").lower() :
            tot_digit = tot_digit + 1

        elif substring(inp_pswd, curr_i - 1, 1) >= ("a").lower()  and substring(inp_pswd, curr_i - 1, 1) <= ("z").lower() :
            tot_char = tot_char + 1
        else:
            tot_special = tot_special + 1

    if tot_digit < 2 or tot_special == 0 or tot_char < 5:
        pswd_level = -2

        return generate_output()
    pswd_ok = True


    pswd_level = check_pswd_strength(inp_pswd)

    return generate_output()