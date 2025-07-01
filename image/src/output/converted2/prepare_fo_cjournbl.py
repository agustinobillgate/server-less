#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt

def prepare_fo_cjournbl(from_dept:int):

    prepare_cache ([Htparam, Hoteldpt])

    fdate = None
    long_digit = False
    depname1 = ""
    depname2 = ""
    htparam = hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, long_digit, depname1, depname2, htparam, hoteldpt
        nonlocal from_dept

        return {"fdate": fdate, "long_digit": long_digit, "depname1": depname1, "depname2": depname2}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    fdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})

    if hoteldpt:
        depname1 = hoteldpt.depart
        depname2 = hoteldpt.depart

    return generate_output()