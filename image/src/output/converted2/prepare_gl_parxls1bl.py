from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_gl_parxls1bl():
    price_decimal = 0
    close_date = None
    curr_close_year = 0
    p_418 = ""
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, close_date, curr_close_year, p_418, htparam

        return {"price_decimal": price_decimal, "close_date": close_date, "curr_close_year": curr_close_year, "p_418": p_418}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    close_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    curr_close_year = get_year(htparam.fdate) + 1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 418)).first()
    p_418 = htparam.fchar

    return generate_output()