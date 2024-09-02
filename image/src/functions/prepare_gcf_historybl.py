from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Htparam

def prepare_gcf_historybl(gastnr:int):
    fdate = None
    t_tittle = ""
    guest = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, t_tittle, guest, htparam


        return {"fdate": fdate, "t_tittle": t_tittle}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    if guest:
        t_tittle = t_tittle + " - " + (guest.name + ", " + guest.vorname1 + guest.anredefirma)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    fdate = htparam.fdate

    return generate_output()