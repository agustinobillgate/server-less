from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_jouhdr

def gl_adjustment_btn_delbl(jnr:int):
    success_flag = False
    gl_journal = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_journal, gl_jouhdr
        nonlocal jnr


        return {"success_flag": success_flag}


    gl_journal = db_session.query(Gl_journal).filter(
             (Gl_journal.jnr == jnr)).first()

    if gl_journal:

        return generate_output()
    else:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.jnr == jnr)).first()

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            success_flag = True

    return generate_output()