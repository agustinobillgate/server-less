#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

def gcf0_contact_btn_delnamebl(gastnr:int, kontnr:int):

    prepare_cache ([Akt_kont])

    main_kont = ""
    maincontact = ""
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = create_buffer("Akt_kont1",Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_kont, maincontact, akt_kont
        nonlocal gastnr, kontnr
        nonlocal akt_kont1


        nonlocal akt_kont1

        return {"main_kont": main_kont, "maincontact": maincontact}

    akt_kont = db_session.query(Akt_kont).filter((Akt_kont.kontakt_nr == kontnr) & (Akt_kont.gastnr == gastnr)).with_for_update().first()

    if akt_kont.hauptkontakt :

        akt_kont1 = db_session.query(Akt_kont).filter((Akt_kont.gastnr == gastnr) & (Akt_kont.hauptkontakt == False)).with_for_update().first()

        if akt_kont1:
            main_kont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
            akt_kont.hauptkontakt = False
            akt_kont1.hauptkontakt = True
        else:
            main_kont = ""
        maincontact = main_kont
    pass
    db_session.delete(akt_kont)

    return generate_output()