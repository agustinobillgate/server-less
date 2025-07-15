#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def segmgroup_adminbl(pvilanguage:int, int1:int, char3:string):
    msg_str = ""
    lvcarea:string = "segmgroup-admin"
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, bediener
        nonlocal pvilanguage, int1, char3

        return {"msg_str": msg_str}


    bediener = get_cache (Bediener, {"user_group": [(eq, int1)],"flag": [(eq, 0)]})

    if bediener:
        pass
    else:
        msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("REMOVE the Department", lvcarea, "") + chr_unicode(10) + to_string(int1) + " - " + char3 + " ?"

    return generate_output()