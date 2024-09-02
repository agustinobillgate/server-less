from functions.additional_functions import *
import decimal
from models import Htparam, L_artikel

def prepare_stock_movelistbl(s_bezeich:str, inp_artnr:int):
    price_decimal = 0
    show_price = False
    avail_l_artikel = False
    htparam = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, show_price, avail_l_artikel, htparam, l_artikel


        return {"price_decimal": price_decimal, "show_price": show_price, "avail_l_artikel": avail_l_artikel}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if inp_artnr != 0:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == inp_artnr)).first()

        if l_artikel:
            s_bezeich = l_artikel.bezeich
            avail_l_artikel = True

    return generate_output()