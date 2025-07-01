#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr

def gl_xlsjourn_gljouhdrbl(journ_no:string):
    avail_gl_jouhdr = False
    gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_jouhdr, gl_jouhdr
        nonlocal journ_no

        return {"avail_gl_jouhdr": avail_gl_jouhdr}


    gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, journ_no)]})

    if gl_jouhdr:
        avail_gl_jouhdr = True

    return generate_output()