#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_fstype

def fstype_admin_delbl(pvilanguage:int, nr:int):
    msg_str = ""
    success_flag = False
    lvcarea:string = "fstype-admin"
    gl_acct = gl_fstype = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, gl_acct, gl_fstype
        nonlocal pvilanguage, nr

        return {"msg_str": msg_str, "success_flag": success_flag}


    gl_acct = get_cache (Gl_acct, {"fs_type": [(eq, nr)]})

    if gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Chart of account exists, deleting not possible.", lvcarea, "")
    else:

        # gl_fstype = get_cache (Gl_fstype, {"nr": [(eq, nr)]})
        gl_fstype = db_session.query(Gl_fstype).filter(Gl_fstype.nr == nr).with_for_update().first()
        db_session.delete(gl_fstype)
        success_flag = True

    return generate_output()