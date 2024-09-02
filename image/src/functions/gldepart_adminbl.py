from functions.additional_functions import *
import decimal
from models import Gl_acct, Gl_department

def gldepart_adminbl(pvilanguage:int, nr:int):
    msg_str = ""
    lvcarea:str = "gldepart_admin"
    gl_acct = gl_department = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_acct, gl_department


        return {"msg_str": msg_str}


    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.deptnr == nr)).first()

    if gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("Chart_of_account exists, deleting not possible.", lvcarea, "")

        return generate_output()
    else:

        gl_department = db_session.query(Gl_department).filter(
                (Gl_department.nr == nr)).first()

        if gl_department:
            db_session.delete(gl_department)


    return generate_output()