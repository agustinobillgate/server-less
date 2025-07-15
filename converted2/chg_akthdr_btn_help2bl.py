#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

def chg_akthdr_btn_help2bl(guest_gastnr:int, kontnr:int):

    prepare_cache ([Akt_kont])

    namekontakt = ""
    akt_kont = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal namekontakt, akt_kont
        nonlocal guest_gastnr, kontnr

        return {"namekontakt": namekontakt}


    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest_gastnr)],"kontakt_nr": [(eq, kontnr)]})
    namekontakt = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    return generate_output()