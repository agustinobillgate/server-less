#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief

def word_admin_getbriefnrbl():

    prepare_cache ([Brief])

    briefnr = 0
    brief = None

    brief1 = None

    Brief1 = create_buffer("Brief1",Brief)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal briefnr, brief
        nonlocal brief1


        nonlocal brief1

        return {"briefnr": briefnr}


    for brief1 in db_session.query(Brief1).order_by(Brief1.briefnr.desc()).yield_per(100):
        briefnr = briefnr + brief1.briefnr
        break
    briefnr = briefnr + 1

    return generate_output()