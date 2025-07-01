#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def cal_commision(recid_ar:int, pay_date:date):
    lvcarea:string = "cal-commision"

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea
        nonlocal recid_ar, pay_date

        return {}

    pass

    return generate_output()