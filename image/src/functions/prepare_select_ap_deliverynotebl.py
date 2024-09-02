from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lieferant, Htparam

def prepare_select_ap_deliverynotebl(lief_nr:int):
    firma = ""
    fdate = None
    l_lieferant = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal firma, fdate, l_lieferant, htparam


        return {"firma": firma, "fdate": fdate}


    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    firma = l_lieferant.firma

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    fdate = htparam.fdate

    return generate_output()