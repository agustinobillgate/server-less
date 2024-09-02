from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def mn_chg_sysdatesbl():
    htparam = None

    htp = None

    Htp = Htparam

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam
        nonlocal htp


        nonlocal htp
        return {}

    def chg_sysdates():

        nonlocal htparam
        nonlocal htp


        nonlocal htp

        curr_date:date = None
        new_date:date = None
        Htp = Htparam

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 474)).first()

        if (htparam.fdate + timedelta(days=1)) <= get_current_date():

            htparam = db_session.query(Htparam).first()
            htparam.fdate = htparam.fdate + timedelta(days=1)

            htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 372)).first()
        curr_date = htparam.fdate
        new_date = curr_date + 1

        htp = db_session.query(Htp).filter(
                (Htp.paramnr == 597)).first()

        if curr_date > htp.fdate:
            curr_date = htp.fdate
        htparam.fdate = new_date

        htparam = db_session.query(Htparam).first()

    chg_sysdates()

    return generate_output()