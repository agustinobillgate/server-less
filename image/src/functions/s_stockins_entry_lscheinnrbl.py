from functions.additional_functions import *
import decimal
from models import L_lieferant, L_lager

def s_stockins_entry_lscheinnrbl(lief_nr:int, curr_lager:int):
    err_code = 0
    err_code1 = 0
    lager_bezeich = ""
    a_firma = ""
    l_lieferant = l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, err_code1, lager_bezeich, a_firma, l_lieferant, l_lager


        return {"err_code": err_code, "err_code1": err_code1, "lager_bezeich": lager_bezeich, "a_firma": a_firma}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if not l_lieferant:
        err_code = 1

        return generate_output()

    elif l_lieferant:
        err_code = 2
        a_firma = l_lieferant.firma

    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()

    if not l_lager:
        err_code1 = 1

        return generate_output()
    else:
        err_code1 = 2
        lager_bezeich = l_lager.bezeich

    return generate_output()