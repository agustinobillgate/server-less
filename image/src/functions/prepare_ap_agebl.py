from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_ap_agebl():
    day1 = 0
    day2 = 0
    day3 = 0
    to_date = None
    price_decimal = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal day1, day2, day3, to_date, price_decimal, htparam


        return {"day1": day1, "day2": day2, "day3": day3, "to_date": to_date, "price_decimal": price_decimal}


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
    to_date = get_current_date()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    return generate_output()