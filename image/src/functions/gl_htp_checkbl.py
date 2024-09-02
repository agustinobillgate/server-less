from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def gl_htp_checkbl(pvilanguage:int, htp_number:int, htgrp_number:int, intval:int, decval:decimal, dateval:date, logval:bool, charval:str, user_init:str, i:int, d:decimal, l:bool, dd:date, s:str):
    msg_str = ""
    do_it = False
    wert = ""
    logv = False
    flag = False
    lvcarea:str = "gl_htp_check_closing_date"
    htparam = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr


        return {"msg_str": msg_str, "do_it": do_it, "wert": wert, "logv": logv, "flag": flag}

    def check_closing_date():

        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr

        d1:date = None
        d2:date = None
        mm:int = 0
        yy:int = 0
        close_date:date = None
        print("HtpNumber:", htgrp_number, htp_number, dateval)

        if htp_number == 1118 or htp_number == 1123 or \
                htp_number == 1003 or htp_number == 1035 or \
                htp_number == 269 or htp_number == 1014:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 597)).first()
            # 
            close_date = htparam.fdate
            aa = date_mdy(get_month(close_date) , 1, get_year(close_date)) - timedelta(days=1)
            print("Check:", dateval, aa)
            if dateval < (date_mdy(get_month(close_date) , 1, get_year(close_date)) - timedelta(days=1)):
                do_it = False
                msg_str = msg_str + chr(2) + "Wrong date value in Parameter" + " " + to_string(htp_number) + " - " + to_string(dateval) + chr(10) + translateExtended ("Current G/l closing date:", lvcarea, "") + " " + to_string(close_date)
                return

        if htgrp_number == 38 and htp_number == 597:

            if get_month(dateval) == 12:
                d2 = date_mdy(12, 31, get_year(dateval))
            else:
                d2 = date_mdy(get_month(dateval) + 1, 1, get_year(dateval)) - timedelta(days=1)
            d1 = date_mdy(get_month(dateval) , 1, get_year(dateval))

            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.activeflag == 1) and  (Gl_jouhdr.datum <= d2) and  (Gl_jouhdr.datum >= d1)).first()

            if gl_jouhdr:
                do_it = False
                msg_str = msg_str + chr(2) + translateExtended ("Closed GL journal(s) found for that period.", lvcarea, "")

        if htgrp_number == 38 and htp_number == 558:
            mm = get_month(dateval) + 1
            yy = get_year(dateval)

            if mm > 12:
                mm = mm - 12
                yy = yy + 1


            d1 = date_mdy(mm, 1, yy)

            if mm == 12:
                d2 = date_mdy(12, 31, yy)
            else:
                d2 = date_mdy(mm + 1, 1, yy) - timedelta(days=1)

            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= d1) and  (Gl_jouhdr.datum <= d2) and  (Gl_jouhdr.activeflag == 1)).first()

            if gl_jouhdr:
                do_it = False
                msg_str = msg_str + chr(2) + translateExtended ("Closed GL journal(s) found for next period.", lvcarea, "")

    def update_htparam():

        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == htp_number)).first()
        print("Type:", htparam.feldtyp, dateval)
        if htparam.feldtyp == 1:
            htparam.finteger = intval
            wert = to_string(htparam.finteger)

        elif htparam.feldtyp == 2:
            htparam.fdecimal = decval
            wert = to_string(htparam.fdecimal)

        elif htparam.feldtyp == 3:
            htparam.fdate = dateval
            wert = to_string(htparam.fdate)

        elif htparam.feldtyp == 4:
            htparam.flogical = logval
            wert = to_string(htparam.flogical)
            logv = htparam.flogical
            flag = True

        elif htparam.feldtyp == 5:
            htparam.fchar = charval
            wert = to_string(htparam.fchar)
        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(time, "HH:mm:SS")

        htparam = db_session.query(Htparam).first()

    check_closing_date()
    print("M:", msg_str, do_it)

    if msg_str != "" or not do_it:
        print("M Kosong")
        return generate_output()
    else:
        print("dateval/dd:", dateval,dd)
        if i != intval or d != decval or dd != dateval or l != logval or s.lower()  != charval.lower() :
            update_htparam()

    return generate_output()