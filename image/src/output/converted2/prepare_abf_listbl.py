#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from functions.get_vipnrbl import get_vipnrbl

def prepare_abf_listbl():
    ci_date = None
    vipnr1 = 0
    vipnr2 = 0
    vipnr3 = 0
    vipnr4 = 0
    vipnr5 = 0
    vipnr6 = 0
    vipnr7 = 0
    vipnr8 = 0
    vipnr9 = 0
    bfast_artnr = 0
    bfast_dept = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, bfast_artnr, bfast_dept

        return {"ci_date": ci_date, "vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9, "bfast_artnr": bfast_artnr, "bfast_dept": bfast_dept}

    ci_date = get_output(htpdate(87))
    bfast_artnr = get_output(htpint(125))
    bfast_dept = get_output(htpint(126))
    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    return generate_output()