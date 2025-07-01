#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, L_hauptgrp

def prepare_fb_reconsile1bl():

    prepare_cache ([Htparam, Waehrung, L_hauptgrp])

    food = 0
    bev = 0
    ldry = 0
    dstore = 0
    to_date = None
    from_date = None
    bill_date = None
    foreign_nr = 0
    double_currency = False
    exchg_rate = 1
    t_l_hauptgrp_list = []
    htparam = waehrung = l_hauptgrp = None

    t_l_hauptgrp = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, ldry, dstore, to_date, from_date, bill_date, foreign_nr, double_currency, exchg_rate, t_l_hauptgrp_list, htparam, waehrung, l_hauptgrp


        nonlocal t_l_hauptgrp
        nonlocal t_l_hauptgrp_list

        return {"food": food, "bev": bev, "ldry": ldry, "dstore": dstore, "to_date": to_date, "from_date": from_date, "bill_date": bill_date, "foreign_nr": foreign_nr, "double_currency": double_currency, "exchg_rate": exchg_rate, "t-l-hauptgrp": t_l_hauptgrp_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    food = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    bev = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    ldry = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
    dstore = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam.flogical:
        double_currency = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    return generate_output()