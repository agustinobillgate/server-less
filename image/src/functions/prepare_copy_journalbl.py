from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_copy_journalbl():
    last_acctdate = None
    datum = None
    fl_temp = False
    finteger = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_acctdate, datum, fl_temp, finteger, htparam


        return {"last_acctdate": last_acctdate, "datum": datum, "fl_temp": fl_temp, "finteger": finteger}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    last_acctdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 372)).first()
    datum = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        fl_temp = True
        finteger = htparam.finteger

    return generate_output()