from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Queasy, L_lieferant

def prepare_gl_postjournbl(adjust_flag:bool):
    f_int = 0
    datum = None
    last_acctdate = None
    acct_date = None
    close_year = None
    avail_queasy = False
    gst_flag = False
    htparam = queasy = l_lieferant = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, datum, last_acctdate, acct_date, close_year, avail_queasy, gst_flag, htparam, queasy, l_lieferant
        nonlocal adjust_flag

        return {"f_int": f_int, "datum": datum, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "avail_queasy": avail_queasy, "gst_flag": gst_flag}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    if not adjust_flag:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 372)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 795)).first()
    datum = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 558)).first()
    last_acctdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    acct_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 108)).first()

    if not queasy:
        avail_queasy = False
    else:
        avail_queasy = True

    l_lieferant = db_session.query(L_lieferant).filter(
             (func.lower(L_lieferant.firma) == ("GST").lower())).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()