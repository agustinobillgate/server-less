#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Queasy

def gl_postjourn_gl_acct2bl(pvilanguage:int, curr_mode:string, elim_journal:bool, fibukonto:string):

    prepare_cache ([Gl_acct, Queasy])

    acct_bez = ""
    flag_code = 0
    msg_str = ""
    lvcarea:string = "gl-postjourn"
    gl_acct = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal acct_bez, flag_code, msg_str, lvcarea, gl_acct, queasy
        nonlocal pvilanguage, curr_mode, elim_journal, fibukonto

        return {"acct_bez": acct_bez, "flag_code": flag_code, "msg_str": msg_str}


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)],"activeflag": [(eq, True)],"bezeich": [(ne, "")]})

    if not gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("No such account found.", lvcarea, "")

        return generate_output()

    if elim_journal:

        queasy = get_cache (Queasy, {"key": [(eq, 108)],"char1": [(eq, fibukonto)]})

        if queasy:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, queasy.char2)]})
        fibukonto = gl_acct.fibukonto
    acct_bez = gl_acct.bezeich

    if gl_acct.acc_type == 2 or gl_acct.acc_type == 3 or gl_acct.acc_type == 5:
        flag_code = 1

        return generate_output()

    elif gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
        flag_code = 2

        return generate_output()

    return generate_output()