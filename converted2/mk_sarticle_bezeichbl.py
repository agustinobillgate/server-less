#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def mk_sarticle_bezeichbl(pvilanguage:int, l_bezeich:string):

    prepare_cache ([L_artikel])

    str_msg = ""
    lvcarea:string = "mk-sarticle"
    l_artikel = None

    l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, lvcarea, l_artikel
        nonlocal pvilanguage, l_bezeich
        nonlocal l_art1


        nonlocal l_art1

        return {"str_msg": str_msg}


    l_art1 = get_cache (L_artikel, {"bezeich": [(eq, l_bezeich)]})

    if l_art1:
        str_msg = "&W" + translateExtended ("Same Description found with article number: ", lvcarea, "") + to_string(l_art1.artnr)

    return generate_output()