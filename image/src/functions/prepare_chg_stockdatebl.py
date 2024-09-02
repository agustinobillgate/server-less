from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Htparam

def prepare_chg_stockdatebl():
    close_date = None
    billdate = None
    record_use = False
    init_time = 0
    init_date = None
    flag_ok:bool = False
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal close_date, billdate, record_use, init_time, init_date, flag_ok, htparam


        return {"close_date": close_date, "billdate": billdate, "record_use": record_use, "init_time": init_time, "init_date": init_date}

    flag_ok, init_time, init_date = get_output(check_timebl(1, 474, None, "htparam", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    close_date = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    return generate_output()