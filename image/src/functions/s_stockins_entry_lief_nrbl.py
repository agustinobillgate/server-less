from functions.additional_functions import *
import decimal
from models import L_lieferant

def s_stockins_entry_lief_nrbl(lief_nr:int):
    err_code = 0
    l_lieferant_firma = ""
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_lieferant_firma, l_lieferant


        return {"err_code": err_code, "l_lieferant_firma": l_lieferant_firma}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if not l_lieferant:
        err_code = 1

        return generate_output()

    elif l_lieferant:
        l_lieferant_firma = l_lieferant.firma
        err_code = 2

        return generate_output()