#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_kont

def mk_aktline_of_kontakt1bl(gastnr:int, gname:string, akt_line1_gastnr:int, akt_line1_kontakt_nr:int):

    prepare_cache ([Guest, Akt_kont])

    t_kontakt = ""
    t_gastnr = 0
    t_kontakt_nr = 0
    avail_guest = False
    avail_akt_kont = False
    avail_akt_kont1 = False
    guest = akt_kont = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_kontakt, t_gastnr, t_kontakt_nr, avail_guest, avail_akt_kont, avail_akt_kont1, guest, akt_kont
        nonlocal gastnr, gname, akt_line1_gastnr, akt_line1_kontakt_nr

        return {"t_kontakt": t_kontakt, "t_gastnr": t_gastnr, "t_kontakt_nr": t_kontakt_nr, "avail_guest": avail_guest, "avail_akt_kont": avail_akt_kont, "avail_akt_kont1": avail_akt_kont1}


    guest = get_cache (Guest, {"gastnr": [(eq, akt_line1_gastnr)]})

    if not guest:

        return generate_output()
    else:
        avail_guest = True

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == gastnr) & (Akt_kont.name == (gname).lower()) | ((Akt_kont.name + ", " + Akt_kont.anrede) == (gname).lower())).first()

        if not akt_kont:

            return generate_output()
        else:
            avail_akt_kont = True
            t_kontakt_nr = akt_kont.kontakt_nr

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastnr)]})

            if akt_kont and akt_kont.name != "":
                avail_akt_kont1 = True
                t_kontakt = akt_kont.name + ", " + akt_kont.anrede
                t_gastnr = guest.gastnr

    return generate_output()