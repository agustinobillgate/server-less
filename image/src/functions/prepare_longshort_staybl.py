from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_longshort_staybl():
    long_stay = 0
    curr_date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_stay, curr_date, htparam


        return {"long_stay": long_stay, "curr_date": curr_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 139)).first()
    long_stay = htparam.finteger

    if long_stay == 0:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    curr_date = fdate

    return generate_output()