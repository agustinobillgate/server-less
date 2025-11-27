#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def vhp_rms_config_logsbl(case_type:int, log_recid:int, month_val:int):

    prepare_cache ([Queasy])

    log_list_data = []
    queasy = None

    log_list = None

    log_list_data, Log_list = create_model("Log_list", {"log_recid":int, "send_date":date, "report_name":string, "send_status":bool, "send_result":string, "report_no":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal log_list_data, queasy
        nonlocal case_type, log_recid, month_val


        nonlocal log_list
        nonlocal log_list_data

        return {"log-list": log_list_data}

    if case_type == 1:

        # queasy = get_cache (Queasy, {"_recid": [(eq, log_recid)]})
        queasy = db_session.query(Queasy).filter(Queasy._recid == log_recid).with_for_update().first()

        if queasy:
            pass
            queasy.logi1 = False


            pass
            pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 347) & (Queasy.betriebsnr == 2) & (Queasy.number1 == month_val) & (Queasy.number2 == get_year(get_current_date()))).order_by(Queasy._recid).all():
        log_list = Log_list()
        log_list_data.append(log_list)

        log_list.log_recid = queasy._recid
        log_list.send_date = queasy.date1
        log_list.report_name = queasy.char1
        log_list.send_status = queasy.logi1
        log_list.send_result = queasy.char2
        log_list.report_no = queasy.number3

    return generate_output()