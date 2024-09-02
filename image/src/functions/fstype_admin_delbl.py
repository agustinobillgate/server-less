from functions.additional_functions import *
import decimal
from models import Gl_acct, Gl_fstype

def fstype_admin_delbl(pvilanguage:int, nr:int):
    msg_str = ""
    success_flag = False
    lvcarea:str = "fstype_admin"
    gl_acct = gl_fstype = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, gl_acct, gl_fstype


        return {"msg_str": msg_str, "success_flag": success_flag}


    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fs_type == nr)).first()

    if gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("Chart of account exists, deleting not possible.", lvcarea, "")
    else:

        gl_fstype = db_session.query(Gl_fstype).filter(
                (Gl_fstype.nr == nr)).first()
        db_session.delete(gl_fstype)
        success_flag = True

    return generate_output()