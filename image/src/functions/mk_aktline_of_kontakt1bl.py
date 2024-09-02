from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Akt_kont

def mk_aktline_of_kontakt1bl(gastnr:int, gname:str, akt_line1_gastnr:int, akt_line1_kontakt_nr:int):
    t_kontakt = ""
    t_gastnr = 0
    t_kontakt_nr = 0
    avail_guest = False
    avail_akt_kont = False
    avail_akt_kont1 = False
    guest = akt_kont = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontakt, t_gastnr, t_kontakt_nr, avail_guest, avail_akt_kont, avail_akt_kont1, guest, akt_kont


        return {"t_kontakt": t_kontakt, "t_gastnr": t_gastnr, "t_kontakt_nr": t_kontakt_nr, "avail_guest": avail_guest, "avail_akt_kont": avail_akt_kont, "avail_akt_kont1": avail_akt_kont1}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == akt_line1_gastnr)).first()

    if not guest:

        return generate_output()
    else:
        avail_guest = True

        akt_kont = db_session.query(Akt_kont).filter(
                (Akt_kont.gastnr == gastnr) &  (func.lower(Akt_kont.name) == (gname).lower()) |  ((func.lower(Akt_kont.name) + ", " + Akt_kont.anrede) == (gname).lower())).first()

        if not akt_kont:

            return generate_output()
        else:
            avail_akt_kont = True
            t_kontakt_nr = akt_kont.kontakt_nr

            akt_kont = db_session.query(Akt_kont).filter(
                    (Akt_kont.gastnr == gastnr)).first()

            if akt_kont and akt_kont.name != "":
                avail_akt_kont1 = True
                t_kontakt = akt_kont.name + ", " + akt_kont.anrede
                t_gastnr = guest.gastnr

    return generate_output()