from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_fa_depnbl():
    last_acctdate = None
    datum = None
    acct_date = None
    close_year = None
    err_no = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_acctdate, datum, acct_date, close_year, err_no, htparam


        return {"last_acctdate": last_acctdate, "datum": datum, "acct_date": acct_date, "close_year": close_year, "err_no": err_no}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 881)).first()
    last_acctdate = htparam.fdate
    datum = last_acctdate + 35
    datum = date_mdy(get_month(datum) , 1, get_year(datum)) - 1

    if datum > get_current_date():
        err_no = 1

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    return generate_output()