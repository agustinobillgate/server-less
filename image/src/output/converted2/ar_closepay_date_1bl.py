#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint

def ar_closepay_date_1bl():
    bill_date = None
    last_transfer = None
    rundung = 0
    p121 = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, last_transfer, rundung, p121

        return {"bill_date": bill_date, "last_transfer": last_transfer, "rundung": rundung, "p121": p121}

    bill_date = get_output(htpdate(110))
    last_transfer = get_output(htpdate(1014))
    rundung = get_output(htpint(491))
    p121 = get_output(htpint(121))

    return generate_output()