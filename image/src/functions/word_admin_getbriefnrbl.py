from functions.additional_functions import *
import decimal
from models import Brief

def word_admin_getbriefnrbl():
    briefnr = 0
    brief = None

    brief1 = None

    Brief1 = Brief

    db_session = local_storage.db_session

    def generate_output():
        nonlocal briefnr, brief
        nonlocal brief1


        nonlocal brief1
        return {"briefnr": briefnr}


    for brief1 in db_session.query(Brief1).all():
        briefnr = briefnr + brief1.briefnr
        break
    briefnr = briefnr + 1

    return generate_output()