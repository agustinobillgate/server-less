#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def mk_sarticle_fibukontobl(pvilanguage:int, fibukonto:string):
    str_msg = ""
    lvcarea:string = "mk-sarticle"
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, lvcarea, gl_acct
        nonlocal pvilanguage, fibukonto

        return {"str_msg": str_msg}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

    if not gl_acct and to_int(fibukonto) != 0:
        str_msg = translateExtended ("No such account number", lvcarea, "")

    return generate_output()