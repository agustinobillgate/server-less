from functions.additional_functions import *
import decimal
from models import Artikel, Htparam

def prepare_ar_remainlistbl():
    from_art = 0
    to_art = 0
    from_bez = ""
    to_bez = ""
    day1 = 0
    day2 = 0
    day3 = 0
    letter1 = 0
    letter2 = 0
    letter3 = 0
    price_decimal = 0
    artikel = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_art, to_art, from_bez, to_bez, day1, day2, day3, letter1, letter2, letter3, price_decimal, artikel, htparam


        return {"from_art": from_art, "to_art": to_art, "from_bez": from_bez, "to_bez": to_bez, "day1": day1, "day2": day2, "day3": day3, "letter1": letter1, "letter2": letter2, "letter3": letter3, "price_decimal": price_decimal}


    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  (Artikel.artart == 2) &  (Artikel.activeflag)).all():

        if from_art > artikel.artnr:
            from_art = artikel.artnr
            from_bez = artikel.bezeich

        if to_art < artikel.artnr:
            to_art = artikel.artnr
            to_bez = artikel.bezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 330)).first()
    day1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 331)).first()
    day2 = htparam.finteger + day1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 332)).first()
    day3 = htparam.finteger + day2

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 670)).first()
    letter1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 671)).first()
    letter2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 388)).first()
    letter3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    return generate_output()