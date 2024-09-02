from functions.additional_functions import *
import decimal
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from models import Htparam, Artikel

def prepare_ar_agebl(from_art:int, to_art:int):
    long_digit = False
    day1 = 0
    day2 = 0
    day3 = 0
    price_decimal = 0
    default_fcurr = ""
    htparam = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, day1, day2, day3, price_decimal, default_fcurr, htparam, artikel


        return {"long_digit": long_digit, "day1": day1, "day2": day2, "day3": day3, "price_decimal": price_decimal, "default_fcurr": default_fcurr}


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
            (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 7)) &  (Artikel.activeflag)).all():

        if from_art > artikel.artnr:
            from_art = artikel.artnr

        if to_art < artikel.artnr:
            to_art = artikel.artnr

    return generate_output()