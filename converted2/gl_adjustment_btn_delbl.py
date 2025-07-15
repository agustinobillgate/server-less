#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_jouhdr

def gl_adjustment_btn_delbl(jnr:int):
    success_flag = False
    gl_journal = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_journal, gl_jouhdr
        nonlocal jnr

        return {"success_flag": success_flag}


    gl_journal = get_cache (Gl_journal, {"jnr": [(eq, jnr)]})

    if gl_journal:

        return generate_output()
    else:

        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})

        if gl_jouhdr:
            db_session.delete(gl_jouhdr)
            success_flag = True

    return generate_output()