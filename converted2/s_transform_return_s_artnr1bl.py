#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def s_transform_return_s_artnr1bl(s_artnr1:int, avail_out_list:bool):

    prepare_cache ([L_artikel])

    l_artikel_artnr = 0
    descript1 = ""
    err_flag = 0
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel_artnr, descript1, err_flag, l_artikel
        nonlocal s_artnr1, avail_out_list

        return {"l_artikel_artnr": l_artikel_artnr, "descript1": descript1, "err_flag": err_flag}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr1)]})

    if not l_artikel:
        err_flag = 1

        return generate_output()
    l_artikel_artnr = l_artikel.artnr

    if l_artikel.betriebsnr == 0:

        if avail_out_list:
            err_flag = 2

            return generate_output()
        descript1 = l_artikel.bezeich + " - " + l_artikel.masseinheit
        err_flag = 3

        return generate_output()

    return generate_output()