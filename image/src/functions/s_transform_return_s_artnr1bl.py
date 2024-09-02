from functions.additional_functions import *
import decimal
from models import L_artikel

def s_transform_return_s_artnr1bl(s_artnr1:int, avail_out_list:bool):
    l_artikel_artnr = 0
    descript1 = ""
    err_flag = 0
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel_artnr, descript1, err_flag, l_artikel


        return {"l_artikel_artnr": l_artikel_artnr, "descript1": descript1, "err_flag": err_flag}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr1)).first()

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