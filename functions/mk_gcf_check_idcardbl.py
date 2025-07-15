from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest

def mk_gcf_check_idcardbl(gastnr:int, idcard:str):
    id_exist = False
    gastnr_exist = 0
    gname_exist = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal id_exist, gastnr_exist, gname_exist, guest
        nonlocal gastnr, idcard


        return {"id_exist": id_exist, "gastnr_exist": gastnr_exist, "gname_exist": gname_exist}


    guest = db_session.query(Guest).filter(
             (func.lower(Guest.ausweis_nr1) == (idcard).lower())).first()

    if guest:
        id_exist = True
        gastnr_exist = guest.gastnr
        gname_exist = guest.name + " " + guest.vorname1 + "," + guest.anrede1
        gname_exist = gname_exist.upper()
    else:
        id_exist = False
        gastnr_exist = 0
        gname_exist = ""

    return generate_output()