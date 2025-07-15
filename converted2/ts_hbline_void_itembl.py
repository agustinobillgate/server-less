#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def ts_hbline_void_itembl(menu_list_artnr:int, dept:int):

    prepare_cache ([H_artikel])

    betriebsnr = 0
    h_artikel = None

    h_art = None

    H_art = create_buffer("H_art",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal betriebsnr, h_artikel
        nonlocal menu_list_artnr, dept
        nonlocal h_art


        nonlocal h_art

        return {"betriebsnr": betriebsnr}


    h_art = get_cache (H_artikel, {"artnr": [(eq, menu_list_artnr)],"departement": [(eq, dept)]})
    betriebsnr = h_art.betriebsnr

    return generate_output()