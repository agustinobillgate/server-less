#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def pchase_book_sartnrbl(pvilanguage:int, s_artnr:int):

    prepare_cache ([L_artikel])

    s_bezeich = ""
    lvcarea:string = "pchase-book"
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_bezeich, lvcarea, l_artikel
        nonlocal pvilanguage, s_artnr

        return {"s_bezeich": s_bezeich}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if l_artikel:
        s_bezeich = l_artikel.bezeich
    else:
        s_bezeich = translateExtended ("Article Description", lvcarea, "")

    return generate_output()