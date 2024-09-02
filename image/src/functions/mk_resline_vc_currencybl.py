from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.htpdec import htpdec
from models import Waehrung

def mk_resline_vc_currencybl(pvilanguage:int, currency:str, zipreis:decimal):
    msg_str = ""
    curr_number = 0
    curr_amount = 0
    max_rate:decimal = 0
    lvcarea:str = "mk_resline"
    waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, curr_number, curr_amount, max_rate, lvcarea, waehrung


        return {"msg_str": msg_str, "curr_number": curr_number, "curr_amount": curr_amount}


    waehrung = db_session.query(Waehrung).filter(
            (func.lower(Waehrung.wabkurz) == (currency).lower())).first()
    curr_number = waehrungsnr
    curr_amount = waehrung.ankauf / waehrung.einheit


    max_rate = get_output(htpdec(1108))

    if max_rate != 0 and zipreis > 0 and (zipreis * curr_amount) > max_rate:
        msg_str = translateExtended ("Room Rate too large, currency NOT changed.", lvcarea, "")

    return generate_output()