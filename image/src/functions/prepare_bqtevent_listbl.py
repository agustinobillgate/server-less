from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_bqtevent_listbl():
    from_date = None
    to_date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, htparam


        return {"from_date": from_date, "to_date": to_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate
    to_date = htparam.fdate

    return generate_output()