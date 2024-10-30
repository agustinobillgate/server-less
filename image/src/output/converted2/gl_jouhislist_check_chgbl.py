from functions.additional_functions import *
import decimal
from models import Gl_jhdrhis, Htparam

def gl_jouhislist_check_chgbl(pvilanguage:int, jnr:int):
    msg_str = ""
    err_code = 0
    lvcarea:str = "gl-jouhislist"
    gl_jhdrhis = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, err_code, lvcarea, gl_jhdrhis, htparam
        nonlocal pvilanguage, jnr

        return {"msg_str": msg_str, "err_code": err_code}


    gl_jhdrhis = db_session.query(Gl_jhdrhis).filter(
             (Gl_jhdrhis.jnr == jnr)).first()

    if gl_jhdrhis.activeflag == 1:
        msg_str = msg_str + chr(2) + translateExtended ("Closed journals can not be edited", lvcarea, "")
        err_code = 1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 983)).first()

    if htparam.flogical:
        msg_str = msg_str + chr(2) + translateExtended ("G/L closing process is running, journal transaction not possible", lvcarea, "")

    return generate_output()