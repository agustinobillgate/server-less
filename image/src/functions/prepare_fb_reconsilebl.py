from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_fb_reconsilebl():
    food = 0
    bev = 0
    to_date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, to_date, htparam


        return {"food": food, "bev": bev, "to_date": to_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    food = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bev = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    to_date = fdate

    return generate_output()