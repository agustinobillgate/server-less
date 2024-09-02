from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_gacct_balancebl():
    heute = None
    billdate = None
    long_digit = False
    price_decimal = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal heute, billdate, long_digit, price_decimal, htparam


        return {"heute": heute, "billdate": billdate, "long_digit": long_digit, "price_decimal": price_decimal}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    heute = htparam.fdate
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    return generate_output()