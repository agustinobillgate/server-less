from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Reservation

def prepare_auto_checkoutbl(resnr:int):
    ci_date = None
    res_name = ""
    htparam = reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, res_name, htparam, reservation


        return {"ci_date": ci_date, "res_name": res_name}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()
    res_name = reservation.name

    return generate_output()