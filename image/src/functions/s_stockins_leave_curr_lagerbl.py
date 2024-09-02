from functions.additional_functions import *
import decimal
from models import L_lager

def s_stockins_leave_curr_lagerbl(curr_lager:int):
    lager_bezeich = ""
    err_code = 0
    l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lager_bezeich, err_code, l_lager


        return {"lager_bezeich": lager_bezeich, "err_code": err_code}


    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()

    if l_lager:
        lager_bezeich = l_lager.bezeich
        err_code = 1

        return generate_output()