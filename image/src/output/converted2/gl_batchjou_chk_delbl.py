#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_jouhdr

def gl_batchjou_chk_delbl(pvilanguage:int, jnr:int, rec_id:int):
    msg_str = ""
    lvcarea:string = "gl-batchjou-chk-del"
    gl_journal = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_journal, gl_jouhdr
        nonlocal pvilanguage, jnr, rec_id

        return {"msg_str": msg_str}


    gl_journal = get_cache (Gl_journal, {"jnr": [(eq, jnr)]})

    if gl_journal:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Journal entries exist, deleting not possible", lvcarea, "")

        return generate_output()

    if not gl_journal:

        gl_jouhdr = get_cache (Gl_jouhdr, {"_recid": [(eq, rec_id)]})
        db_session.delete(gl_jouhdr)

    return generate_output()