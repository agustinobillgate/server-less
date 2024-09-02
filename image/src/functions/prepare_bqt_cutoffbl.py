from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_bqt_cutoffbl():
    ci_date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, htparam


        return {"ci_date": ci_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    return generate_output()