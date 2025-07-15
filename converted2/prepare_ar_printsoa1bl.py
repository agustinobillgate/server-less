#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Htparam, Waehrung

def prepare_ar_printsoa1bl():

    prepare_cache ([Htparam, Waehrung])

    curr_date = None
    foreign_rate = False
    price_decimal = 0
    local_curr = ""
    p_417 = ""
    foreign_curr = ""
    dollar_rate = to_decimal("0.0")
    curr_day = None
    htparam = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, foreign_rate, price_decimal, local_curr, p_417, foreign_curr, dollar_rate, curr_day, htparam, waehrung

        return {"curr_date": curr_date, "foreign_rate": foreign_rate, "price_decimal": price_decimal, "local_curr": local_curr, "p_417": p_417, "foreign_curr": foreign_curr, "dollar_rate": dollar_rate, "curr_day": curr_day}

    curr_date = get_output(htpdate(110))
    foreign_rate = get_output(htplogic(143))
    price_decimal = get_output(htpint(491))
    local_curr = get_output(htpchar(152))
    p_417 = get_output(htpchar(417))
    curr_day = get_output(htpdate(110))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
    foreign_curr = waehrung.wabkurz

    if waehrung:
        dollar_rate =  to_decimal(waehrung.ankauf)

    return generate_output()