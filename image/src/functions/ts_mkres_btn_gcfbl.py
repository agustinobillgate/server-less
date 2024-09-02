from functions.additional_functions import *
import decimal
from models import Guest

def ts_mkres_btn_gcfbl(gastno:int):
    gname = ""
    telefon = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, guest


        return {"gname": gname, "telefon": telefon}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()

    if guest:
        gname = guest.name + "," + guest.vorname1
        telefon = guest.telefon

    return generate_output()