from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Htparam

def prepare_chg_storerequestbl(user_init:str):
    show_price = False
    req_flag = False
    p_220 = 0
    bediener = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, p_220, bediener, htparam


        return {"show_price": show_price, "req_flag": req_flag, "p_220": p_220}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 475)).first()
    req_flag = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 220)).first()
    p_220 = htparam.finteger

    return generate_output()