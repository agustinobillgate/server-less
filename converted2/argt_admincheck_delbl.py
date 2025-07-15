#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Reslin_queasy, Res_line, Prtable

def argt_admincheck_delbl(pvilanguage:int, argtnr:int, arrangement:string):

    prepare_cache ([Reslin_queasy])

    msg_str = ""
    lvcarea:string = "argt-admin-check-del"
    found:bool = False
    i:int = 0
    reslin_queasy = res_line = prtable = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, found, i, reslin_queasy, res_line, prtable
        nonlocal pvilanguage, argtnr, arrangement

        return {"msg_str": msg_str}


    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"number2": [(eq, argtnr)]})

    if reslin_queasy:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Deleting no possible, arrangement defined in price code : ", lvcarea, "") + reslin_queasy.char1

        return generate_output()

    res_line = get_cache (Res_line, {"arrangement": [(eq, arrangement)]})

    if res_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")

        return generate_output()

    prtable = db_session.query(Prtable).first()
    while None != prtable and not found:
        for i in range(1,99 + 1) :

            if prtable.argtnr[i - 1] == argtnr:
                found = True

        curr_recid = prtable._recid
        prtable = db_session.query(Prtable).filter(Prtable._recid > curr_recid).first()

    if found:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Price Market Table exists, deleting not possible.", lvcarea, "")

        return generate_output()

    return generate_output()