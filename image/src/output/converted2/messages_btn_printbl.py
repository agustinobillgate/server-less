from functions.additional_functions import *
import decimal
from models import Htparam, Brief

def messages_btn_printbl():
    brief_briefnr = 0
    avail_brief = False
    htparam = brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal brief_briefnr, avail_brief, htparam, brief


        return {"brief_briefnr": brief_briefnr, "avail_brief": avail_brief}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 434)).first()

    brief = db_session.query(Brief).filter(
             (Brief.briefnr == htparam.finteger)).first()

    if brief:
        avail_brief = True
        brief_briefnr = brief.briefnr

    return generate_output()