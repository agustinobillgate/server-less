from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_jouhdr

def gl_batchjou_chk_delbl(pvilanguage:int, jnr:int, rec_id:int):
    msg_str = ""
    lvcarea:str = "gl-batchjou-chk-del"
    gl_journal = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_journal, gl_jouhdr
        nonlocal pvilanguage, jnr, rec_id

        return {"msg_str": msg_str}


    gl_journal = db_session.query(Gl_journal).filter(
             (Gl_journal.jnr == jnr)).first()

    if gl_journal:
        msg_str = msg_str + chr(2) + translateExtended ("Journal entries exist, deleting not possible", lvcarea, "")

        return generate_output()

    if not gl_journal:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr._recid == rec_id)).first()
        db_session.delete(gl_jouhdr)

    return generate_output()