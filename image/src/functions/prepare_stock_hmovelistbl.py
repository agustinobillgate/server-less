from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_artikel

def prepare_stock_hmovelistbl(s_bezeich:str, user_init:str, inp_artnr:int):
    price_decimal = 0
    show_price = False
    close_date = None
    mm = 0
    yy = 0
    fl_code = 0
    htparam = bediener = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, show_price, close_date, mm, yy, fl_code, htparam, bediener, l_artikel


        return {"price_decimal": price_decimal, "show_price": show_price, "close_date": close_date, "mm": mm, "yy": yy, "fl_code": fl_code}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    if inp_artnr != 0:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == inp_artnr)).first()

        if l_artikel:
            s_bezeich = l_artikel.bezeich

            if l_artikel.endkum <= 2:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 224)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 221)).first()
            close_date = htparam.fdate
            mm = get_month(close_date) - 1
            yy = get_year(close_date)

            if mm == 0:
                mm = 12
                yy = yy - 1


            fl_code = 1

    return generate_output()