#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_main

def glmain_adminbl(pvilanguage:int, nr:int):
    msg_str = ""
    success_flag = False
    lvcarea:string = "glmain-admin"
    gl_acct = gl_main = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, gl_acct, gl_main
        nonlocal pvilanguage, nr

        return {"msg_str": msg_str, "success_flag": success_flag}


    gl_acct = get_cache (Gl_acct, {"main_nr": [(eq, nr)]})

    if gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Chart-of-account under this main code exists, deleting not possible.", lvcarea, "")
    else:

        gl_main = get_cache (Gl_main, {"nr": [(eq, nr)]})

        if gl_main:
            db_session.delete(gl_main)
            pass
            success_flag = True

    return generate_output()