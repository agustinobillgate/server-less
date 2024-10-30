from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr

def gl_postjournbl(refno:str):
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


    gbuff = db_session.query(Gbuff).filter(
             (func.lower(Gbuff.refno) == (refno).lower())).first()

    if gbuff:
        fl_code = 1
        datum = gbuff.datum
        bezeich = gbuff.bezeich

    return generate_output()