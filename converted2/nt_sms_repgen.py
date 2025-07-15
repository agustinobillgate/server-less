from functions.additional_functions import *
import decimal
from datetime import date
from functions.sms_repgen import sms_repgen
from models import Htparam, Queasy

def nt_sms_repgen():
    billdate:date = None
    s_recid:int = 0
    htparam = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, s_recid, htparam, queasy

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 34)).order_by(Queasy._recid).all():
        s_recid = to_int(queasy._recid)


        get_output(sms_repgen(billdate, s_recid))

    return generate_output()