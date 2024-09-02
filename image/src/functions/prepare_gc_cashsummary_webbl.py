from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_gc_cashsummary_webbl():
    from_date = None
    to_date = None
    curr_local = ""
    curr_foreign = ""
    double_curr = False
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, curr_local, curr_foreign, double_curr, htparam


        return {"from_date": from_date, "to_date": to_date, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_curr": double_curr}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam:
        from_date = htparam.fdate
        to_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    if htparam:
        curr_local = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam:
        curr_foreign = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        double_curr = htparam.flogi

    return generate_output()