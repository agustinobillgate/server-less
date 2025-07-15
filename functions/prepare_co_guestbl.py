#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint

def prepare_co_guestbl():
    fr_date = None
    price_decimal = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fr_date, price_decimal

        return {"fr_date": fr_date, "price_decimal": price_decimal}

    fr_date = get_output(htpdate(110))
    price_decimal = get_output(htpint(491))

    return generate_output()