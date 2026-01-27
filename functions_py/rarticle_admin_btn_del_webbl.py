#using conversion tools version: 1.0.0.119
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added

# Rulita, 19-01-2026
# Update fiture Sub Menu
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_umsatz, Queasy, H_menu

def rarticle_admin_btn_del_webbl(h_artnr:int, h_dept:int):
    flag = 0
    sub_menu_nr:int = 0
    h_artikel = h_umsatz = queasy = h_menu = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, sub_menu_nr, h_artikel, h_umsatz, queasy, h_menu
        nonlocal h_artnr, h_dept

        return {"flag": flag}


    # h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, h_dept)]})
    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == h_artnr) &
             (H_artikel.departement == h_dept)).with_for_update().first()

    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artnr)],"departement": [(eq, h_dept)]})

    if h_umsatz:
        flag = 1
    else:
        sub_menu_nr = h_artikel.betriebsnr
        flag = 2
        pass
        db_session.delete(h_artikel)

        # queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artnr)],"number3": [(eq, h_dept)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) &
                 (Queasy.number1 == 2) &
                 (Queasy.number2 == h_artnr) &
                 (Queasy.number3 == h_dept)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
        
        # Rulita, 19-01-2026
        # Update fiture Sub Menu
        for h_menu in db_session.query(H_menu).filter(
                 (H_menu.nr == sub_menu_nr)).order_by(H_menu._recid).all():
            db_session.delete(h_menu)

        # queasy = get_cache (Queasy, {"key": [(eq, 361)],"number2": [(eq, h_dept)],"char1": [(eq, "fixed-sub-menu")],"number1": [(eq, h_artnr)]})

        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 361) & (Queasy.number2 == h_dept) & 
                     (Queasy.char1 == ("fixed-sub-menu")) & 
                     (Queasy.number3 == h_artnr)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 361) & (Queasy.number2 == h_dept) & (Queasy.char1 == ("Qty-Sub-Menu").lower()) & (Queasy.number3 == sub_menu_nr)).order_by(Queasy._recid).all():
            db_session.delete(queasy)

    return generate_output()