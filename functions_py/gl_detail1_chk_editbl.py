#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 25/11/2025, with_for_update added
# tidak ada EXCL-LOCK
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr, Htparam

def gl_detail1_chk_editbl(pvilanguage:int, jnr:int):

    prepare_cache ([Gl_jouhdr])

    msg_str = ""
    err_nr = 0
    lvcarea:string = "gl-detail1-chk-edit"
    gl_jouhdr = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_nr, lvcarea, gl_jouhdr, htparam
        nonlocal pvilanguage, jnr

        return {"msg_str": msg_str, "err_nr": err_nr}


    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 1:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Closed journals can not be edited", lvcarea, "")

            return generate_output()
        else:
            # break
            pass
    else:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Archived journals can not be edited", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})

    if htparam.flogical:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")

    return generate_output()