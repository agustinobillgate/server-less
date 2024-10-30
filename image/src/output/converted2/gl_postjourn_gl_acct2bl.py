from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Queasy

def gl_postjourn_gl_acct2bl(pvilanguage:int, curr_mode:str, elim_journal:bool, fibukonto:str):
    acct_bez = ""
    flag_code = 0
    msg_str = ""
    lvcarea:str = "gl-postjourn"
    gl_acct = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal acct_bez, flag_code, msg_str, lvcarea, gl_acct, queasy
        nonlocal pvilanguage, curr_mode, elim_journal, fibukonto

        return {"acct_bez": acct_bez, "flag_code": flag_code, "msg_str": msg_str}


    gl_acct = db_session.query(Gl_acct).filter(
             (func.lower(Gl_acct.fibukonto) == (fibukonto).lower()) & (Gl_acct.activeflag) & (Gl_acct.bezeich != "")).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("No such account found.", lvcarea, "")

        return generate_output()

    if elim_journal:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 108) & (func.lower(Queasy.char1) == (fibukonto).lower())).first()

        if queasy:

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == queasy.char2)).first()
        fibukonto = gl_acct.fibukonto
    acct_bez = gl_acct.bezeich

    if gl_acct.acc_type == 2 or gl_acct.acc_type == 3 or gl_acct.acc_type == 5:
        flag_code = 1

        return generate_output()

    elif gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
        flag_code = 2

        return generate_output()

    return generate_output()