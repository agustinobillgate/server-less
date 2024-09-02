from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, Bediener

def prepare_sales_performbl(user_init:str):
    price_decimal = 0
    from_date = ""
    to_date = ""
    usr_init = ""
    htparam = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, from_date, to_date, usr_init, htparam, bediener


        return {"price_decimal": price_decimal, "from_date": from_date, "to_date": to_date, "usr_init": usr_init}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = to_string(get_month(fdate) , "99") + to_string(get_year(fdate) , "9999")
    to_date = from_date
    usr_init = user_init

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    return generate_output()