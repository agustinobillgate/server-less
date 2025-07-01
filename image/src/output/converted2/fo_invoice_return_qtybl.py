#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Artikel

def fo_invoice_return_qtybl(t_artnr:int, balance:Decimal):

    prepare_cache ([Waehrung, Artikel])

    exrate = to_decimal("0.0")
    price = to_decimal("0.0")
    msg = 0
    waehrung = artikel = None

    w1 = None

    W1 = create_buffer("W1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate, price, msg, waehrung, artikel
        nonlocal t_artnr, balance
        nonlocal w1


        nonlocal w1

        return {"exrate": exrate, "price": price, "msg": msg}


    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)]})

    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

    if w1:
        exrate =  to_decimal(w1.ankauf) / to_decimal(w1.einheit)
    else:
        msg = 1
    price =  - to_decimal(balance) / to_decimal(exrate)

    return generate_output()