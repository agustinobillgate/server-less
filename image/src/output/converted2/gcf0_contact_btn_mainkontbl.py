#using conversion tools version: 1.0.0.111

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


    akt_kont1 = get_cache (Akt_kont, {"gastnr": [(eq, gastnr)],"hauptkontakt": [(eq, True)]})

    if akt_kont1:
        akt_kont1.hauptkontakt = False
        pass

    akt_kont = get_cache (Akt_kont, {"_recid": [(eq, rec_id)]})
    pass
    akt_kont.hauptkontakt = True
    pass
    main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    return generate_output()