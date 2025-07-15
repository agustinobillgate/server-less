from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_kont

def mk_aktion_of_namekontaktbl(namekontakt:str, guest_gastnr:int):
    a_kontakt_nr = 0
    avail_aktkont1 = True
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = create_buffer("Akt_kont1",Akt_kont)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_kontakt_nr, avail_aktkont1, akt_kont
        nonlocal namekontakt, guest_gastnr
        nonlocal akt_kont1


        nonlocal akt_kont1
        return {"namekontakt": namekontakt, "a_kontakt_nr": a_kontakt_nr, "avail_aktkont1": avail_aktkont1}


    akt_kont1 = db_session.query(Akt_kont1).filter(
             (Akt_kont1.gastnr == guest_gastnr) & (func.lower(Akt_kont1.name) == (namekontakt).lower())).first()

    if not akt_kont1:
        avail_aktkont1 = False
    else:
        a_kontakt_nr = akt_kont1.kontakt_nr
        namekontakt = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede

    return generate_output()