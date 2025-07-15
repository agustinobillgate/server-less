#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Pricecod

def check_del_prtablebl(pvilanguage:int, nr:int, bezeich:string):

    prepare_cache ([Ratecode, Pricecod])

    msg_str = ""
    rcode:string = ""
    lvcarea:string = "check-del-prtable"
    ratecode = pricecod = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, rcode, lvcarea, ratecode, pricecod
        nonlocal pvilanguage, nr, bezeich

        return {"msg_str": msg_str}


    ratecode = get_cache (Ratecode, {"marknr": [(eq, nr)]})

    if ratecode:
        rcode = ratecode.code
    else:

        pricecod = get_cache (Pricecod, {"marknr": [(eq, nr)]})

        if pricecod:
            rcode = pricecod.code

    if rcode != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Rates exists, CODE = ", lvcarea, "") + rcode + "; " + translateExtended ("deleting not possibe", lvcarea, "")

        return generate_output()
    msg_str = msg_str + chr_unicode(2) + "&Q" + translateExtended ("Do you really want to REMOVE the Price Market Table", lvcarea, "") + chr_unicode(10) + to_string(nr) + " - " + bezeich + " ?"

    return generate_output()