from functions.additional_functions import *
import decimal
from models import L_lieferant

def dml_stockin_lieferantbl(lief_nr:int):
    err_flag = 0
    lief_bezeich = ""
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, lief_bezeich, l_lieferant


        return {"err_flag": err_flag, "lief_bezeich": lief_bezeich}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if not l_lieferant:
        err_flag = 1

        return generate_output()

    elif l_lieferant:
        err_flag = 2
        lief_bezeich = l_lieferant.firma

    return generate_output()