from functions.additional_functions import *
import decimal
from models import Akt_kont

def mk_aktline_btn_help2bl(akt_line1_gastnr:int, kontnr:int):
    t_kontakt = ""
    akt_kont = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontakt, akt_kont


        return {"t_kontakt": t_kontakt}


    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == akt_line1_gastnr) &  (Akt_kont.kontakt_nr == kontnr)).first()
    t_kontakt = akt_kont.name + ", " + akt_kont.anrede

    return generate_output()