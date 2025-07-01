#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_hcost_analbl():

    prepare_cache ([Htparam])

    long_digit = False
    price_decimal = 0
    to_date = None
    from_date = None
    bill_date = None
    f_eknr = 0
    b_eknr = 0
    fl_eknr = 0
    bl_eknr = 0
    bev_food = ""
    food_bev = ""
    price_type = 0
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, price_decimal, to_date, from_date, bill_date, f_eknr, b_eknr, fl_eknr, bl_eknr, bev_food, food_bev, price_type, htparam

        return {"long_digit": long_digit, "price_decimal": price_decimal, "to_date": to_date, "from_date": from_date, "bill_date": bill_date, "f_eknr": f_eknr, "b_eknr": b_eknr, "fl_eknr": fl_eknr, "bl_eknr": bl_eknr, "bev_food": bev_food, "food_bev": food_bev, "price_type": price_type}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    f_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
    b_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    fl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bl_eknr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 272)]})
    bev_food = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 275)]})
    food_bev = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger

    return generate_output()