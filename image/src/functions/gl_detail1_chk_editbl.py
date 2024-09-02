from functions.additional_functions import *
import decimal
from models import Gl_jouhdr, Htparam

def gl_detail1_chk_editbl(pvilanguage:int, jnr:int):
    msg_str = ""
    err_nr = 0
    lvcarea:str = "gl_detail1_chk_edit"
    gl_jouhdr = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_nr, lvcarea, gl_jouhdr, htparam


        return {"msg_str": msg_str, "err_nr": err_nr}


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jnr == jnr)).first()

    if gl_jouhdr:

        if gl_jouhdr.activeflag == 1:
            msg_str = msg_str + chr(2) + translateExtended ("Closed journals can not be edited", lvcarea, "")

            return generate_output()
        else:
            pass
    else:
        msg_str = msg_str + chr(2) + translateExtended ("Archived journals can not be edited", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 983)).first()

    if htparam.flogical:
        msg_str = msg_str + chr(2) + translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")

    return generate_output()