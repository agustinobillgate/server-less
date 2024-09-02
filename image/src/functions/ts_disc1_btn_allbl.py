from functions.additional_functions import *
import decimal
from models import H_artikel, Artikel

def ts_disc1_btn_allbl(menu_artnr:int, menu_departement:int, food_flag:bool, bev_flag:bool, other_flag:bool):
    menu_prtflag = 0
    menu_bcol = 0
    h_artikel = artikel = None

    h_art = f_art = None

    H_art = H_artikel
    F_art = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal menu_prtflag, menu_bcol, h_artikel, artikel
        nonlocal h_art, f_art


        nonlocal h_art, f_art
        return {"menu_prtflag": menu_prtflag, "menu_bcol": menu_bcol}


    h_art = db_session.query(H_art).filter(
            (H_art.artnr == menu_artnr) &  (H_art.departement == menu_departement)).first()

    if h_art:

        f_art = db_session.query(F_art).filter(
                (F_art.departement == h_art.departement) &  (F_art.artnr == h_art.artnrfront)).first()

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