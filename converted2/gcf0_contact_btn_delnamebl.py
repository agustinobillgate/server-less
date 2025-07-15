#using conversion tools version: 1.0.0.117

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


    akt_kont = get_cache (Akt_kont, {"kontakt_nr": [(eq, kontnr)],"gastnr": [(eq, gastnr)]})

    if akt_kont.hauptkontakt :

        akt_kont1 = get_cache (Akt_kont, {"gastnr": [(eq, gastnr)],"hauptkontakt": [(eq, False)]})

        if akt_kont1:
            main_kont = akt_kont1.name + ", " + akt_kont1.vorname + " " + akt_kont1.anrede
            pass
            akt_kont.hauptkontakt = False
            pass
            pass
            akt_kont1.hauptkontakt = True
            pass
        else:
            main_kont = ""
        maincontact = main_kont
    pass
    db_session.delete(akt_kont)

    return generate_output()