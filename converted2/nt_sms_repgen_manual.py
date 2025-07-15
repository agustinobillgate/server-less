from functions.additional_functions import *
import decimal
from datetime import date
from functions.sms_repgen import sms_repgen
from models import Queasy

def nt_sms_repgen_manual():
    billdate:date = None
    s_recid:int = 0
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, s_recid, queasy

        return {}

    billdate

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 34)).order_by(Queasy._recid).all():
        s_recid = to_int(queasy._recid)


        get_output(sms_repgen(billdate, s_recid))

    return generate_output()