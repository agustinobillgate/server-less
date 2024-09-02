from functions.additional_functions import *
import decimal
from models import L_lieferant

def supply_hinlist_lieferantbl(lief_nr:int):
    from_supp = ""
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_supp, l_lieferant


        return {"from_supp": from_supp}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    from_supp = l_lieferant.firma

    return generate_output()