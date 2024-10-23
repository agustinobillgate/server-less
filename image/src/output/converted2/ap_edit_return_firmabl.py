from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant

def ap_edit_return_firmabl(firma:str):
    lief_nr = 0
    fl_temp = 0
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_nr, fl_temp, l_lieferant
        nonlocal firma


        return {"lief_nr": lief_nr, "fl_temp": fl_temp}


    l_lieferant = db_session.query(L_lieferant).filter(
             (func.lower(L_lieferant.firma) == (firma).lower())).first()

    if not l_lieferant:
        fl_temp = 1

        return generate_output()
    lief_nr = l_lieferant.lief_nr
    fl_temp = 0

    return generate_output()