#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def fa_artlist_fibukontobl(fibukonto:string):
    do_it = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, gl_acct
        nonlocal fibukonto

        return {"do_it": do_it}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

    if not gl_acct and to_int(fibukonto) != 0:
        do_it = True

    return generate_output()