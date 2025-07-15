#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Artikel

def ts_disc1_btn_allbl(menu_artnr:int, menu_departement:int, food_flag:bool, bev_flag:bool, other_flag:bool):

    prepare_cache ([H_artikel, Artikel])

    menu_prtflag = 0
    menu_bcol = 1
    h_artikel = artikel = None

    h_art = f_art = None

    H_art = create_buffer("H_art",H_artikel)
    F_art = create_buffer("F_art",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal menu_prtflag, menu_bcol, h_artikel, artikel
        nonlocal menu_artnr, menu_departement, food_flag, bev_flag, other_flag
        nonlocal h_art, f_art


        nonlocal h_art, f_art

        return {"menu_prtflag": menu_prtflag, "menu_bcol": menu_bcol}


    h_art = get_cache (H_artikel, {"artnr": [(eq, menu_artnr)],"departement": [(eq, menu_departement)]})

    if h_art:

        f_art = get_cache (Artikel, {"departement": [(eq, h_art.departement)],"artnr": [(eq, h_art.artnrfront)]})

        if food_flag and (f_art.umsatzart == 3 or f_art.umsatzart == 5):
            menu_prtflag = 1
            menu_bcol = 12

        if bev_flag and (f_art.umsatzart == 3 or f_art.umsatzart == 6):
            menu_prtflag = 1
            menu_bcol = 12

        if other_flag and f_art.umsatzart == 4:
            menu_prtflag = 1
            menu_bcol = 12

    return generate_output()