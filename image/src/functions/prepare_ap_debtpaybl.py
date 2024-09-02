from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam

def prepare_ap_debtpaybl():
    bill_date = None
    rundung = 0
    p_1118 = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, rundung, p_1118, htparam


        return {"bill_date": bill_date, "rundung": rundung, "p_1118": p_1118}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    rundung = htparam.finteger
    rundung = 2
    p_1118 = get_output(htpdate(1118))

    return generate_output()