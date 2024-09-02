from functions.additional_functions import *
import decimal
from models import Htparam, Brief

def sel_printminvbl(ind:int, briefnr:int):
    htparam = brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam, brief


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 688)).first()

    if htparam.finteger > 0:

        brief = db_session.query(Brief).filter(
                (briefnr == htparam.finteger)).first()

        if brief:
            briefnr = htparam.finteger

    if ind == 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 495)).first()

        if htparam.finteger > 0:

            brief = db_session.query(Brief).filter(
                    (briefnr == htparam.finteger)).first()

            if brief:
                briefnr = htparam.finteger

    return generate_output()