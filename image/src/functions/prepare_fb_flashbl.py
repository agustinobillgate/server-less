from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_fb_flashbl():
    food = 0
    bev = 0
    date2 = None
    date1 = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal food, bev, date2, date1, htparam


        return {"food": food, "bev": bev, "date2": date2, "date1": date1}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    food = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    bev = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    date2 = fdate
    date1 = date_mdy(get_month(date2) , 1, get_year(date2))

    return generate_output()