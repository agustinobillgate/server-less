#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam

def chg_gcf_btn_searchbl(case_type:int, master_gastnr:int):

    prepare_cache ([Guest, Htparam])

    progname = ""
    mastername = ""
    gbuff_gastnr = 0
    ext_char:string = ""
    guest = htparam = None

    gbuff = None

    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal progname, mastername, gbuff_gastnr, ext_char, guest, htparam
        nonlocal case_type, master_gastnr
        nonlocal gbuff


        nonlocal gbuff

        return {"progname": progname, "mastername": mastername, "gbuff_gastnr": gbuff_gastnr}


    if case_type == 0:

        gbuff = get_cache (Guest, {"gastnr": [(eq, master_gastnr)]})
        mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    ext_char = htparam.fchar

    gbuff = get_cache (Guest, {"gastnr": [(eq, master_gastnr)]})

    if gbuff:
        gbuff_gastnr = gbuff.gastnr
        progname = "chg-gcf" + ext_char + to_string(gbuff.karteityp) + "UI.p"
        mastername = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma + " " + gbuff.anrede1

    return generate_output()