#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, L_op, L_ophis

def initial_stock_check_registerbl(s_artnr:int, curr_lager:int):

    prepare_cache ([L_bestand])

    error_code = 0
    fl_code = 0
    best_list_list = []
    l_bestand = l_op = l_ophis = None

    best_list = None

    best_list_list, Best_list = create_model_like(L_bestand, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, fl_code, best_list_list, l_bestand, l_op, l_ophis
        nonlocal s_artnr, curr_lager


        nonlocal best_list
        nonlocal best_list_list

        return {"error_code": error_code, "fl_code": fl_code, "best-list": best_list_list}

    l_bestand = get_cache (L_bestand, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, curr_lager)]})

    if l_bestand:

        l_op = get_cache (L_op, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, curr_lager)]})

        if l_op:
            fl_code = 1
            error_code = 2

            return generate_output()

        l_ophis = get_cache (L_ophis, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, curr_lager)]})

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
        best_list.anz_anf_best =  to_decimal(l_bestand.anz_anf_best)
        best_list.val_anf_best =  to_decimal(l_bestand.val_anf_best)
        best_list.betriebsnr = 1
        best_list.rec_id = l_bestand._recid

    return generate_output()