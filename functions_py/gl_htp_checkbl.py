#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 28/7/2025
# if available
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def gl_htp_checkbl(pvilanguage:int, htp_number:int, htgrp_number:int, intval:int, decval:Decimal, dateval:date, logval:bool, charval:string, user_init:string, i:int, d:Decimal, l:bool, dd:date, s:string):

    prepare_cache ([Htparam])

    msg_str = ""
    do_it = True
    wert = ""
    logv = False
    flag = False
    lvcarea:string = "gl-htp-check-closing-date"
    htparam = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr
        nonlocal pvilanguage, htp_number, htgrp_number, intval, decval, dateval, logval, charval, user_init, i, d, l, dd, s

        return {"msg_str": msg_str, "do_it": do_it, "wert": wert, "logv": logv, "flag": flag}

    def check_closing_date():

        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr
        nonlocal pvilanguage, htp_number, htgrp_number, intval, decval, dateval, logval, charval, user_init, i, d, l, dd, s

        d1:date = None
        d2:date = None
        mm:int = 0
        yy:int = 0
        close_date:date = None
        date1:date = None
        date2:date = None
        m1:int = 0

        if htp_number == 1118 or htp_number == 1123 or htp_number == 1003 or htp_number == 1035 or htp_number == 269 or htp_number == 1014:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
            close_date = htparam.fdate
            date1 = date_mdy(get_month(close_date) , 1, get_year(close_date))
            date2 = date1 - timedelta(days=1)

            if dateval < date2:
                do_it = False
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong date value in Parameter", lvcarea, "") + " " + to_string(htp_number) + " - " + to_string(dateval) + chr_unicode(10) + translateExtended ("Current G/l closing date:", lvcarea, "") + " " + to_string(close_date)

                return

        if htgrp_number == 38 and htp_number == 597:
            m1 = get_month(dateval) + 1
            date1 = date_mdy(m1, 1, get_year(dateval))
            date2 = date1 - timedelta(days=1)

            if get_month(dateval) == 12:
                d2 = date_mdy(12, 31, get_year(dateval))
            else:
                d2 = date2
            d1 = date_mdy(get_month(dateval) , 1, get_year(dateval))

            gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, 1)],"datum": [(le, d2),(ge, d1)]})

            if gl_jouhdr:
                do_it = False
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Closed GL journal(s) found for that period.", lvcarea, "")

        if htgrp_number == 38 and htp_number == 558:
            mm = get_month(dateval) + 1
            yy = get_year(dateval)

            if mm > 12:
                mm = mm - 12
                yy = yy + 1


            d1 = date_mdy(mm, 1, yy)
            m1 = mm + 1
            date1 = date_mdy(m1, 1, yy)
            date2 = date1 - timedelta(days=1)

            if mm == 12:
                d2 = date_mdy(12, 31, yy)
            else:
                d2 = date2

            gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(ge, d1),(le, d2)],"activeflag": [(eq, 1)]})

            if gl_jouhdr:
                do_it = False
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Closed GL journal(s) found for next period.", lvcarea, "")


    def update_htparam():

        nonlocal msg_str, do_it, wert, logv, flag, lvcarea, htparam, gl_jouhdr
        nonlocal pvilanguage, htp_number, htgrp_number, intval, decval, dateval, logval, charval, user_init, i, d, l, dd, s

        # Rd, 24/11/2025, get htparam dengan for update
        # htparam = get_cache (Htparam, {"paramnr": [(eq, htp_number)]})
        htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == htp_number)).with_for_update().first()
        
        # Rd 28/7/2025
        # if available
        if htparam is None:
            return generate_output()

        # Rd 28/7/2025
        if htparam and htparam.feldtyp == 1:
            htparam.finteger = intval
            wert = to_string(htparam.finteger)

        elif htparam and htparam.feldtyp == 2:
            htparam.fdecimal =  to_decimal(decval)
            wert = to_string(htparam.fdecimal)

        elif htparam and htparam.feldtyp == 3:
            htparam.fdate = dateval
            wert = to_string(htparam.fdate)

        elif htparam and htparam.feldtyp == 4:
            htparam.flogical = logval
            wert = to_string(htparam.flogical)
            logv = htparam.flogical
            flag = True

        elif htparam and htparam.feldtyp == 5:
            htparam.fchar = charval
            wert = to_string(htparam.fchar)

        htparam.lupdate = get_current_date()
        htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:mm:SS")
        pass


    check_closing_date()

    if msg_str != "" or not do_it:

        return generate_output()
    else:

        if i != intval or d != decval or dd != dateval or l != logval or s.lower()  != (charval).lower() :
            update_htparam()

    return generate_output()