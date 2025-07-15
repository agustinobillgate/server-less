from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Htparam, Artikel, Waehrung

def prepare_ar_age_1bl (1)(from_art:int, to_art:int):
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


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 330)).first()

    if htparam.finteger != 0:
        day1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 331)).first()

    if htparam.finteger != 0:
        day2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 332)).first()

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
             (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        dollar_rate =  to_decimal(waehrung.ankauf)

    return generate_output()