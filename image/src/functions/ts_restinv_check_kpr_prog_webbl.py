from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def ts_restinv_check_kpr_prog_webbl(kpr_time:int, kpr_recid:int, bill_date:date):
    fl_code = 0
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, queasy


        return {"fl_code": fl_code}


    if (kpr_time - get_current_time_in_seconds()) >= 300:
        kpr_time = get_current_time_in_seconds()

    if kpr_recid == 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 3) &  (Queasy.number1 != 0) &  ((Queasy.char1 != "") |  (Queasy.char3 != "")) &  ((Queasy.date1 == bill_date))).first()

        if queasy:
            kpr_recid = to_int(queasy._recid)


        kpr_time = get_current_time_in_seconds()

    elif kpr_recid != 0 and (get_current_time_in_seconds() > (kpr_time + 30)):

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == kpr_recid)).first()

        if queasy and queasy.number1 != 0:
            fl_code = 1
        kpr_recid = 0
        kpr_time = get_current_time_in_seconds()

    return generate_output()