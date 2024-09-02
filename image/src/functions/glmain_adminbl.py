from functions.additional_functions import *
import decimal
from models import Gl_acct, Gl_main

def glmain_adminbl(pvilanguage:int, nr:int):
    msg_str = ""
    success_flag = False
    lvcarea:str = "glmain_admin"
    gl_acct = gl_main = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, gl_acct, gl_main


        return {"msg_str": msg_str, "success_flag": success_flag}


    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.main_nr == nr)).first()

    if gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("Chart_of_account under this main code exists, deleting not possible.", lvcarea, "")
    else:

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.nr == nr)).first()

        if gl_main:
            db_session.delete(gl_main)

            success_flag = True

    return generate_output()