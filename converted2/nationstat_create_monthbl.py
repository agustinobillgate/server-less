#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def nationstat_create_monthbl(diff_one:int, from_month:string):
    mm:int = 0
    yy:int = 0
    curr_date:date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mm, yy, curr_date
        nonlocal diff_one, from_month

        return {"from_month": from_month}

    mm = to_int(substring(from_month, 0, 2)) + diff_one
    yy = to_int(substring(from_month, 2, 4))

    if diff_one == 1 and mm == 13:
        mm = 1
        yy = yy + 1

    elif diff_one == -1 and mm == 0:
        mm = 12
        yy = yy - 1
    curr_date = date_mdy(mm, 1, yy)
    from_month = to_string(get_month(curr_date) , "99") + to_string(get_year(curr_date) , "9999")

    return generate_output()