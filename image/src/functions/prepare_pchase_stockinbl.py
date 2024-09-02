from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_pchase_stockinbl():
    order_date = None
    billdate = None
    enforce_rflag = False
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_date, billdate, enforce_rflag, htparam


        return {"order_date": order_date, "billdate": billdate, "enforce_rflag": enforce_rflag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    order_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    return generate_output()