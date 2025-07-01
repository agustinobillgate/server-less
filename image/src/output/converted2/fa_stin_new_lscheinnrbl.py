#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_op

def fa_stin_new_lscheinnrbl(billdate:date):
    s = ""
    lscheinnr = ""
    i:int = 1
    fa_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s, lscheinnr, i, fa_op
        nonlocal billdate

        return {"s": s, "lscheinnr": lscheinnr}

    s = "FA" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")
    lscheinnr = s + to_string(i, "999")

    fa_op = db_session.query(Fa_op).filter(
             (Fa_op.datum == billdate) & (substring(Fa_op.lscheinnr, 0, 11) == (lscheinnr).lower())).first()
    while None != fa_op:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        fa_op = db_session.query(Fa_op).filter(
                 (Fa_op.datum == billdate) & (substring(Fa_op.lscheinnr, 0, 11) == (lscheinnr).lower())).first()

    return generate_output()