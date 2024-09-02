from functions.additional_functions import *
import decimal
from models import L_lieferant

def s_stockiss_l_lieferantbl(lief_nr:int):
    a_firma = ""
    avail_l_lieferant = False
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_firma, avail_l_lieferant, l_lieferant


        return {"a_firma": a_firma, "avail_l_lieferant": avail_l_lieferant}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if l_lieferant:
        avail_l_lieferant = True
        a_firma = l_lieferant.firma

    return generate_output()