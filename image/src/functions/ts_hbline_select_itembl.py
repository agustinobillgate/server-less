from functions.additional_functions import *
import decimal
from models import H_artikel

def ts_hbline_select_itembl(pvilanguage:int, dept:int, help_flag:bool, art_list_artnr:int):
    info_str = ""
    price:decimal = 0
    price2:decimal = 0
    lvcarea:str = "TS_hbline"
    h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal info_str, price, price2, lvcarea, h_artikel


        return {"info_str": info_str}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == art_list_artnr) &  (H_artikel.departement == dept)).first()

    if help_flag:
        price = h_artikel.epreis1
        price2 = h_artikel.epreis2

        if price2 == 0:
            info_str = to_string(h_artikel.artnr) + " - " + to_string(h_artikel.bezeich) + ": " + translateExtended ("price", lvcarea, "") + " " + trim(to_string(price, ">,>>>,>>>,>>9.99"))
        else:
            info_str = to_string(h_artikel.artnr) + " - " + to_string(h_artikel.bezeich) + ": " + translateExtended ("price", lvcarea, "") + " " + trim(to_string(price, ">,>>>,>>>,>>9.99")) + " [" + trim(to_string(price2, ">,>>>,>>>,>>9.99")) + "]"

        return generate_output()