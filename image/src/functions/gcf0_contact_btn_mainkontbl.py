from functions.additional_functions import *
import decimal
from models import Akt_kont

def gcf0_contact_btn_mainkontbl(rec_id:int, gastnr:int):
    main_kont = ""
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = Akt_kont

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_kont, akt_kont
        nonlocal akt_kont1


        nonlocal akt_kont1
        return {"main_kont": main_kont}


    akt_kont1 = db_session.query(Akt_kont1).filter(
            (Akt_kont1.gastnr == gastnr) &  (Akt_kont1.hauptkontakt)).first()

    if akt_kont1:
        akt_kont1.hauptkontakt = False

        akt_kont1 = db_session.query(Akt_kont1).first()

    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont._recid == rec_id)).first()

    akt_kont = db_session.query(Akt_kont).first()
    akt_kont.hauptkontakt = True

    akt_kont = db_session.query(Akt_kont).first()
    main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    return generate_output()