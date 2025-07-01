#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def gl_linkar_check_datebl(pvilanguage:int, datum:date, acct_date:date, last_acctdate:date, to_date:date, close_year:date):
    msg_str = ""
    lvcarea:string = "gl-linkar-check-date"

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea
        nonlocal pvilanguage, datum, acct_date, last_acctdate, to_date, close_year

        return {"msg_str": msg_str}


    if acct_date == None or last_acctdate == None or to_date == None or close_year == None:
        msg_str = translateExtended ("Accounting Date(s) not defined", lvcarea, "") + chr_unicode(13) +\
                chr_unicode(10) + translateExtended ("(ParamNo 372, 558, 597, 1014)", lvcarea, "")


    else:

        if datum <= last_acctdate:
            msg_str = translateExtended ("Wrong Posting Date", lvcarea, "") + chr_unicode(13) +\
                    chr_unicode(10) + translateExtended ("Last A/R Journal Transfer Date :", lvcarea, "") + " " + to_string(last_acctdate) +\
                    chr_unicode(13) + chr_unicode(10) + translateExtended ("Current G/L Closing Date :", lvcarea, "") + " " + to_string(acct_date)

    return generate_output()