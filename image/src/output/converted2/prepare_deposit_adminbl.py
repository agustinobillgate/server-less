#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import Htparam, Artikel, Waehrung

def prepare_deposit_adminbl():

    prepare_cache ([Htparam, Artikel, Waehrung])

    fdate = None
    bill_date = None
    long_digit = False
    price_decimal = 0
    depo_foreign = False
    depo_curr = 0
    foreign_curr = 0
    p_60 = 0
    htparam = artikel = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, bill_date, long_digit, price_decimal, depo_foreign, depo_curr, foreign_curr, p_60, htparam, artikel, waehrung

        return {"fdate": fdate, "bill_date": bill_date, "long_digit": long_digit, "price_decimal": price_decimal, "depo_foreign": depo_foreign, "depo_curr": depo_curr, "foreign_curr": foreign_curr, "p_60": p_60}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    fdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
    depo_foreign = artikel.pricetab
    depo_curr = artikel.betriebsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
    foreign_curr = waehrung.waehrungsnr
    p_60 = get_output(htpint(60))

    return generate_output()