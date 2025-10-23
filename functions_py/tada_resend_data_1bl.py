#using conversion tools version: 1.0.0.117

# ===========================================
# Rulita, 15-10-2025
# Tiket ID : 523BB6 | New Compile program IF 
# ===========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def tada_resend_data_1bl(case_type:int, date_value:date, rec_id:int):

    prepare_cache ([Queasy])

    log_list_data = []
    nr:int = 0
    queasy = None

    log_list = None

    log_list_data, Log_list = create_model("Log_list", {"nr":int, "send_date":date, "data_date":date, "deptnr":int, "terminalid":int, "filenames":string, "send_status":bool, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal log_list_data, nr, queasy
        nonlocal case_type, date_value, rec_id


        nonlocal log_list
        nonlocal log_list_data

        return {"log-list": log_list_data}

    if case_type == 1:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        if queasy:
            pass
            queasy.logi1 = False
            pass
            pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 99) & (get_month(Queasy.date1) == get_month(date_value)) & (get_year(Queasy.date1) == get_year(date_value))).order_by(Queasy.betriebsnr, Queasy.date2).all():
        nr = nr + 1
        log_list = Log_list()
        log_list_data.append(log_list)

        log_list.nr = nr
        log_list.send_date = queasy.date1
        log_list.data_date = queasy.date2
        log_list.terminalid = queasy.betriebsnr
        log_list.deptnr = queasy.number2
        log_list.filenames = queasy.char1
        log_list.send_status = queasy.logi1
        log_list.rec_id = queasy._recid

    return generate_output()