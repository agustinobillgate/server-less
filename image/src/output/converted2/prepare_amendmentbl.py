#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def prepare_amendmentbl(blockid:string):
    amendmentstr = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amendmentstr
        nonlocal blockid

        return {"amendmentstr": amendmentstr}


    bk_amendment = db_session.query(Bk_amendment).filter(
             (Bk_amendment.blockid == blockid)).first()

    if bk_amendment:
        amendmentstr = bk_amendment.strAmendment

    return generate_output()