from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Htparam

def prepare_delv_stockbl(user_init:str):
    show_price = False
    long_digit = False
    bediener = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, long_digit, bediener, htparam


        return {"show_price": show_price, "long_digit": long_digit}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    return generate_output()