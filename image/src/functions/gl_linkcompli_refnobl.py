from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_jouhdr

def gl_linkcompli_refnobl(refno:str):
    avail_gl_jouhdr = False
    gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_gl_jouhdr, gl_jouhdr


        return {"avail_gl_jouhdr": avail_gl_jouhdr}


    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (func.lower(Gl_jouhdr.(refno).lower()) == (refno).lower())).first()

    if gl_jouhdr:
        avail_gl_jouhdr = True

    return generate_output()