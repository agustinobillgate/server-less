#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Artikel

def fo_invoice_check_pricebl(l_price:Decimal, t_artnr:int, t_departement:int):

    prepare_cache ([Waehrung, Artikel])

    waehrung = artikel = None

    w1 = None

    W1 = create_buffer("W1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal waehrung, artikel
        nonlocal l_price, t_artnr, t_departement
        nonlocal w1


        nonlocal w1

        return {"l_price": l_price}


    artikel = get_cache (Artikel, {"artnr": [(eq, t_artnr)],"departement": [(eq, t_departement)]})

    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

    if w1:
        l_price =  to_decimal(l_price) * to_decimal(w1.ankauf) / to_decimal(w1.einheit)

    return generate_output()