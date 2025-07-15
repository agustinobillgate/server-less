#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_ap_journ1bl():
    to_date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date

        return {"to_date": to_date}

    to_date = get_output(htpdate(110))

    return generate_output()