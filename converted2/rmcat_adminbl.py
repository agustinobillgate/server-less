#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Zimkateg

def rmcat_adminbl(pvilanguage:int, zikatnr:int):
    msg_str = ""
    lvcarea:string = "rmcat-admin"
    zimmer = zimkateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, zimmer, zimkateg
        nonlocal pvilanguage, zikatnr

        return {"msg_str": msg_str}


    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zikatnr)]})

    if zimmer:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Room under this category exists, deleting not possible.", lvcarea, "")
    else:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatnr)]})

        if zimkateg:
            db_session.delete(zimkateg)

    return generate_output()