#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr

def gl_postjournbl(refno:string):

    prepare_cache ([Gl_jouhdr])

    fl_code = 0
    datum = None
    bezeich = ""
    gl_jouhdr = None

    gbuff = None

    Gbuff = create_buffer("Gbuff",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, datum, bezeich, gl_jouhdr
        nonlocal refno
        nonlocal gbuff


        nonlocal gbuff

        return {"fl_code": fl_code, "datum": datum, "bezeich": bezeich}


    gbuff = get_cache (Gl_jouhdr, {"refno": [(eq, refno)]})

    if gbuff:
        fl_code = 1
        datum = gbuff.datum
        bezeich = gbuff.bezeich

    return generate_output()