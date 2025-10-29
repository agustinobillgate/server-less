#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Artikel

def ts_selsubmenu_check_exitbl(v_mode:int, artno:int, curr_dept:int, str1:string, str2:string):

    prepare_cache ([H_artikel, Artikel])

    error_code = 0
    success_flag = False
    h_artikel = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, success_flag, h_artikel, artikel
        nonlocal v_mode, artno, curr_dept, str1, str2

        return {"error_code": error_code, "success_flag": success_flag}


    if v_mode == 1:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, artno)],"departement": [(eq, curr_dept)],"artart": [(eq, 0)]})

        if h_artikel:

            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

            if artikel:

                if artikel.artart == 9 and artikel.artgrp != 0:
                    error_code = 1

                return generate_output()
    success_flag = True

    return generate_output()