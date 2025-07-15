#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpdec import htpdec
from models import Waehrung

def mk_resline_vc_currencybl(pvilanguage:int, currency:string, zipreis:Decimal):

    prepare_cache ([Waehrung])

    msg_str = ""
    curr_number = 0
    curr_amount = 1
    max_rate:Decimal = to_decimal("0.0")
    lvcarea:string = "mk-resline"
    waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, curr_number, curr_amount, max_rate, lvcarea, waehrung
        nonlocal pvilanguage, currency, zipreis

        return {"msg_str": msg_str, "curr_number": curr_number, "curr_amount": curr_amount}


    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency)]})
    curr_number = waehrung.waehrungsnr
    curr_amount =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    max_rate = get_output(htpdec(1108))

    if max_rate != 0 and zipreis > 0 and (zipreis * curr_amount) > max_rate:
        msg_str = translateExtended ("Room Rate too large, currency NOT changed.", lvcarea, "")

    return generate_output()