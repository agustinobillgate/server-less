from functions.additional_functions import *
import decimal
from models import H_artikel

def ts_hbline_void_itembl(menu_list_artnr:int, dept:int):
    betriebsnr = 0
    h_artikel = None

    h_art = None

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal betriebsnr, h_artikel
        nonlocal h_art


        nonlocal h_art
        return {"betriebsnr": betriebsnr}


    h_art = db_session.query(H_art).filter(
            (H_art.artnr == menu_list_artnr) &  (H_art.departement == dept)).first()
    betriebsnr = h_art.betriebsnr

    return generate_output()