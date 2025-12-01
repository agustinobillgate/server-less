#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def tada_resend_databl(case_type:int, send_date:date, rec_id:int):

    prepare_cache ([Queasy])

    log_list_data = []
    nr:int = 0
    queasy = None

    log_list = None

    log_list_data, Log_list = create_model("Log_list", {"nr":int, "send_date":date, "data_date":date, "deptnr":int, "filenames":string, "send_status":bool, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal log_list_data, nr, queasy
        nonlocal case_type, send_date, rec_id


        nonlocal log_list
        nonlocal log_list_data

        return {"log-list": log_list_data}

    if case_type == 1:

        # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        queasy = db_session.query(Queasy).filter(
            Queasy._recid == rec_id
        ).with_for_update().first()

        if queasy:
            pass
            queasy.logi1 = False
            pass
            pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 99)).order_by(Queasy._recid).all():
        nr = nr + 1
        log_list = Log_list()
        log_list_data.append(log_list)

        log_list.nr = nr
        log_list.send_date = queasy.date1
        log_list.data_date = queasy.date2
        log_list.deptnr = queasy.betriebsnr
        log_list.filenames = queasy.char1
        log_list.send_status = queasy.logi1
        log_list.rec_id = queasy._recid

    return generate_output()