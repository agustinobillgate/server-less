#using conversion tools version: 1.0.0.117

# ========================
# Rulita, 31-10-2025
# - Recompile program
# ========================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Paramtext

def ts_hbline_get_pricebl(art_list_artnr:int, dept:int):

    prepare_cache ([H_artikel, Paramtext])

    err = False
    err1 = False
    price = to_decimal("0.0")
    fract = 1
    h_artikel = paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, err1, price, fract, h_artikel, paramtext
        nonlocal art_list_artnr, dept

        return {"err": err, "err1": err1, "price": price, "fract": fract}

    def get_price():

        nonlocal err, err1, price, fract, h_artikel, paramtext
        nonlocal art_list_artnr, dept

        i:int = 0
        n:int = 0
        j:int = 0
        tolerance:int = 0
        curr_min:int = 0

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, art_list_artnr)],"departement": [(eq, dept)]})
        price =  to_decimal(h_artikel.epreis1)

        if price == 0:
            err = True

            return

        if h_artikel.epreis2 != 0:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (10000 + dept))]})

            if paramtext:
                tolerance = paramtext.sprachcode
                curr_min = to_int(substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 3, 2))
                i = round((get_current_time_in_seconds() / 3600 - 0.5) , 0)

                if i <= 0:
                    i = 24
                n = to_int(substring(paramtext.ptexte, i - 1, 1))

                if n == 2:
                    price =  to_decimal(h_artikel.epreis2)

                elif tolerance > 0:

                    if i == 1:
                        j = 24
                    else:
                        j = i - 1

                    if to_int(substring(paramtext.ptexte, j - 1, 1)) == 2 and curr_min <= tolerance:
                        price =  to_decimal(h_artikel.epreis2)

        if price != 0 and h_artikel.gang == 1:
            err1 = True

            return


    get_price()

    return generate_output()