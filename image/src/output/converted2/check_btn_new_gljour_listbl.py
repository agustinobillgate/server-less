#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def check_btn_new_gljour_listbl(pvilanguage:int):

    prepare_cache ([Htparam])

    msg_str = ""
    fl_temp = False
    close_year:date = None
    curr_month:date = None
    lvcarea:string = "gljour-list"
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, fl_temp, close_year, curr_month, lvcarea, htparam
        nonlocal pvilanguage

        return {"msg_str": msg_str, "fl_temp": fl_temp}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})

    if htparam.flogical:
        msg_str = translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")
        fl_temp = False
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
        close_year = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        curr_month = htparam.fdate

        if (get_year(close_year) + 1) != get_year(curr_month):
            msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Closing year has not been done.", lvcarea, "")
        fl_temp = True

    return generate_output()