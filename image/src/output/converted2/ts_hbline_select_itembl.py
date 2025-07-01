#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def ts_hbline_select_itembl(pvilanguage:int, dept:int, help_flag:bool, art_list_artnr:int):

    prepare_cache ([H_artikel])

    info_str = ""
    price:Decimal = to_decimal("0.0")
    price2:Decimal = to_decimal("0.0")
    lvcarea:string = "TS-hbline"
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal info_str, price, price2, lvcarea, h_artikel
        nonlocal pvilanguage, dept, help_flag, art_list_artnr

        return {"info_str": info_str}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, art_list_artnr)],"departement": [(eq, dept)]})

    if help_flag:
        price =  to_decimal(h_artikel.epreis1)
        price2 =  to_decimal(h_artikel.epreis2)

        if price2 == 0:
            info_str = to_string(h_artikel.artnr) + " - " + to_string(h_artikel.bezeich) + ": " + translateExtended ("price", lvcarea, "") + " " + trim(to_string(price, ">,>>>,>>>,>>9.99"))
        else:
            info_str = to_string(h_artikel.artnr) + " - " + to_string(h_artikel.bezeich) + ": " + translateExtended ("price", lvcarea, "") + " " + trim(to_string(price, ">,>>>,>>>,>>9.99")) + " [" + trim(to_string(price2, ">,>>>,>>>,>>9.99")) + "]"

        return generate_output()

    return generate_output()