#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr

def fa_depn_refnobl(refno:string):
    err_no = 0
    gl_jouhdr = None

    gl_jouhdr1 = None

    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, gl_jouhdr
        nonlocal refno
        nonlocal gl_jouhdr1


        nonlocal gl_jouhdr1

        return {"err_no": err_no}


    gl_jouhdr1 = db_session.query(Gl_jouhdr1).filter(
             (Gl_jouhdr1.refno == (refno).lower()) & (Gl_jouhdr1.jtype == 7)).first()

    if gl_jouhdr1:
        err_no = 1

    return generate_output()