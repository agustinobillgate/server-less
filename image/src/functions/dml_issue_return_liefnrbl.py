from functions.additional_functions import *
import decimal
from models import L_lieferant

def dml_issue_return_liefnrbl(lief_nr:int):
    lief_bezeich = ""
    avail_lieferant = False
    l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lief_bezeich, avail_lieferant, l_lieferant


        return {"lief_bezeich": lief_bezeich, "avail_lieferant": avail_lieferant}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    if not l_lieferant:

        return generate_output()

    elif l_lieferant:
        lief_bezeich = l_lieferant.firma
        avail_lieferant = True

    return generate_output()