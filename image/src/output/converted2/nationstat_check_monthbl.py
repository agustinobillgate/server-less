#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def nationstat_check_monthbl(from_month:string, ci_date:date, diff_one:int):
    msglogi = True
    mm1:int = 0
    yy1:int = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msglogi, mm1, yy1
        nonlocal from_month, ci_date, diff_one

        return {"msglogi": msglogi}

    mm1 = to_int(substring(from_month, 0, 2)) + diff_one
    yy1 = to_int(substring(from_month, 2, 4))

    if mm1 == 0:
        mm1 = 12
        yy1 = yy1 - 1

    if (yy1 > get_year(ci_date)) or ((get_year(ci_date) == yy1) and (mm1 > get_month(ci_date))):
        msglogi = False

    return generate_output()