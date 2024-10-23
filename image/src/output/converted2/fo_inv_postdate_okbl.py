from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate

def fo_inv_postdate_okbl(billdate:date, curr_date:date):
    transdate = None
    msgstr = ""
    its_ok:bool = True
    pdate:date = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal transdate, msgstr, its_ok, pdate
        nonlocal billdate, curr_date


        return {"transdate": transdate, "msgstr": msgstr}


    if billdate > curr_date:
        its_ok = False
    else:
        pdate = get_output(htpdate(1003))

        if billdate <= pdate:
            its_ok = False
            msgstr = "Wrong posting date;" + chr(10) + "Last transferred date F/O -> G/L = " + to_string(pdate)
            billdate = curr_date
            transdate = billdate

            return generate_output()

    if not its_ok:
        msgstr = "Wrong posting date"
        billdate = curr_date
    transdate = billdate

    return generate_output()