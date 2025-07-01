#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Htparam, Artikel, Waehrung

def prepare_ar_age_1bl(from_art:int, to_art:int):

    prepare_cache ([Htparam, Artikel, Waehrung])

    long_digit = False
    day1 = 30
    day2 = 30
    day3 = 30
    price_decimal = 0
    default_fcurr = ""
    dollar_rate = to_decimal("0.0")
    htparam = artikel = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, day1, day2, day3, price_decimal, default_fcurr, dollar_rate, htparam, artikel, waehrung
        nonlocal from_art, to_art

        return {"from_art": from_art, "to_art": to_art, "long_digit": long_digit, "day1": day1, "day2": day2, "day3": day3, "price_decimal": price_decimal, "default_fcurr": default_fcurr, "dollar_rate": dollar_rate}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 330)]})

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 331)]})

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 332)]})

    if htparam.finteger != 0:
        day3 = htparam.finteger
    day2 = day2 + day1
    day3 = day3 + day2


    long_digit = get_output(htplogic(246))
    price_decimal = get_output(htpint(491))
    default_fcurr = get_output(htpchar(144))

    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7)) & (Artikel.activeflag)).order_by(Artikel._recid).all():

        if from_art > artikel.artnr:
            from_art = artikel.artnr

        if to_art < artikel.artnr:
            to_art = artikel.artnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        dollar_rate =  to_decimal(waehrung.ankauf)

    return generate_output()