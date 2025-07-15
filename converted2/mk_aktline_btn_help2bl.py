#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont

def mk_aktline_btn_help2bl(akt_line1_gastnr:int, kontnr:int):

    prepare_cache ([Akt_kont])

    t_kontakt = ""
    akt_kont = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontakt, akt_kont
        nonlocal akt_line1_gastnr, kontnr

        return {"t_kontakt": t_kontakt}


    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, akt_line1_gastnr)],"kontakt_nr": [(eq, kontnr)]})
    t_kontakt = akt_kont.name + ", " + akt_kont.anrede

    return generate_output()