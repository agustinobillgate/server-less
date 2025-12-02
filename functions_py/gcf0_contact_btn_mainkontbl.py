#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

def gcf0_contact_btn_mainkontbl(rec_id:int, gastnr:int):

    prepare_cache ([Akt_kont])

    main_kont = ""
    akt_kont = None

    akt_kont1 = None

    Akt_kont1 = create_buffer("Akt_kont1",Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_kont, akt_kont
        nonlocal rec_id, gastnr
        nonlocal akt_kont1


        nonlocal akt_kont1

        return {"main_kont": main_kont}


    akt_kont1 = db_session.query(Akt_kont).filter((Akt_kont.gastnr == gastnr) & (Akt_kont.hauptkontakt == True)).with_for_update().first()

    if akt_kont1:
        akt_kont1.hauptkontakt = False
        pass

    akt_kont = db_session.query(Akt_kont).filter(Akt_kont._recid == rec_id).with_for_update().first()
    pass
    akt_kont.hauptkontakt = True
    pass
    main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    return generate_output()
