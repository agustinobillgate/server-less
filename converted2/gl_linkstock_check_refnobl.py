#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr

def gl_linkstock_check_refnobl(refno:string, jtype:int):
    avail_gl_jouhdr = False
    gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_jouhdr, gl_jouhdr
        nonlocal refno, jtype

        return {"avail_gl_jouhdr": avail_gl_jouhdr}


    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)],"jtype": [(eq, jtype)]})

    if gl_jouhdr:
        avail_gl_jouhdr = True

    return generate_output()