from functions.additional_functions import *
import decimal
from models import Akt_kont

def mk_aktion_btn_help2bl(guest_gastnr:int, kontnr:int):
    namekontakt = ""
    akt_kont = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal namekontakt, akt_kont
        nonlocal guest_gastnr, kontnr


        return {"namekontakt": namekontakt}


    akt_kont = db_session.query(Akt_kont).filter(
             (Akt_kont.gastnr == guest_gastnr) & (Akt_kont.kontakt_nr == kontnr)).first()
    namekontakt = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede + " - " + akt_kont.funktion + " / " + akt_kont.abteilung

    return generate_output()