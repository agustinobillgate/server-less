from functions.additional_functions import *
import decimal
from models import L_bestand, L_op, L_ophis

def initial_stock_check_registerbl(s_artnr:int, curr_lager:int):
    error_code = 0
    fl_code = 0
    best_list_list = []
    l_bestand = l_op = l_ophis = None

    best_list = None

    best_list_list, Best_list = create_model_like(L_bestand, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, fl_code, best_list_list, l_bestand, l_op, l_ophis


        nonlocal best_list
        nonlocal best_list_list
        return {"error_code": error_code, "fl_code": fl_code, "best-list": best_list_list}

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == s_artnr) &  (L_bestand.lager_nr == curr_lager)).first()

    if l_bestand:

        l_op = db_session.query(L_op).filter(
                (L_op.artnr == s_artnr) &  (L_op.lager_nr == curr_lager)).first()

        if l_op:
            fl_code = 1
            error_code = 2

            return generate_output()

        l_ophis = db_session.query(L_ophis).filter(
                (L_ophis.artnr == s_artnr) &  (L_ophis.lager_nr == curr_lager)).first()

        if l_ophis:
            fl_code = 2
            error_code = 2

            return generate_output()
        fl_code = 3
        best_list = Best_list()
        best_list_list.append(best_list)

        best_list.artnr = s_artnr
        best_list.anf_best_dat = l_bestand.anf_best_dat
        best_list.lager_nr = curr_lager
        best_list.anz_anf_best = l_bestand.anz_anf_best
        best_list.val_anf_best = l_bestand.val_anf_best
        best_list.betriebsnr = 1
        best_list.rec_id = l_bestand._recid

    return generate_output()