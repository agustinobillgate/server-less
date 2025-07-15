from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_kont

def mk_aktion_return_namekontaktbl(namekontakt:str, g_gastnr:int):
    t_kontakt_nr = 0
    avail_akt_kont = False
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = create_buffer("Akt_kont1",Akt_kont)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontakt_nr, avail_akt_kont, akt_kont
        nonlocal namekontakt, g_gastnr
        nonlocal akt_kont1


        nonlocal akt_kont1
        return {"namekontakt": namekontakt, "t_kontakt_nr": t_kontakt_nr, "avail_akt_kont": avail_akt_kont}


    akt_kont1 = db_session.query(Akt_kont1).filter(
             (Akt_kont1.gastnr == g_gastnr) & (func.lower(Akt_kont1.name) == (namekontakt).lower())).first()

    if not akt_kont1:

        return generate_output()
    else:
        avail_akt_kont = True
        t_kontakt_nr = akt_kont1.kontakt_nr
        namekontakt = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede

    return generate_output()