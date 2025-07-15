#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jhdrhis, Htparam

def gl_jouhislist_check_chgbl(pvilanguage:int, jnr:int):

    prepare_cache ([Gl_jhdrhis])

    msg_str = ""
    err_code = 0
    lvcarea:string = "gl-jouhislist"
    gl_jhdrhis = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_code, lvcarea, gl_jhdrhis, htparam
        nonlocal pvilanguage, jnr

        return {"msg_str": msg_str, "err_code": err_code}


    gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, jnr)]})

    if gl_jhdrhis.activeflag == 1:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Closed journals can not be edited", lvcarea, "")
        err_code = 1

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})

    if htparam.flogical:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")

    return generate_output()