from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def check_btn_new_gljour_listbl(pvilanguage:int):
    msg_str = ""
    fl_temp = False
    close_year:date = None
    curr_month:date = None
    lvcarea:str = "gljour-list"
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, fl_temp, close_year, curr_month, lvcarea, htparam
        nonlocal pvilanguage


        return {"msg_str": msg_str, "fl_temp": fl_temp}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 983)).first()

    if htparam.flogical:
        msg_str = translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")
        fl_temp = False
    else:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 795)).first()
        close_year = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 597)).first()
        curr_month = htparam.fdate

        if (get_year(close_year) + 1) != get_year(curr_month):
            msg_str = msg_str + chr(2) + "&W" + translateExtended ("Closing year has not been done.", lvcarea, "")
        fl_temp = True

    return generate_output()