#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_department

def gldepart_adminbl(pvilanguage:int, nr:int):
    msg_str = ""
    lvcarea:string = "gldepart-admin"
    gl_acct = gl_department = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_acct, gl_department
        nonlocal pvilanguage, nr

        return {"msg_str": msg_str}


    gl_acct = get_cache (Gl_acct, {"deptnr": [(eq, nr)]})

    if gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Chart-of-account exists, deleting not possible.", lvcarea, "")

        return generate_output()
    else:

        gl_department = get_cache (Gl_department, {"nr": [(eq, nr)]})

        if gl_department:
            db_session.delete(gl_department)
        pass

    return generate_output()