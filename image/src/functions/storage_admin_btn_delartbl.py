from functions.additional_functions import *
import decimal
from models import L_lager, L_bestand

def storage_admin_btn_delartbl(lager_nr:int):
    err_code = 0
    l_lager = l_bestand = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_lager, l_bestand


        return {"err_code": err_code}


    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == lager_nr)).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.lager_nr == l_lager.lager_nr)).first()

    if l_bestand:
        err_code = 1
    else:

        l_lager = db_session.query(L_lager).first()
        db_session.delete(l_lager)

    return generate_output()