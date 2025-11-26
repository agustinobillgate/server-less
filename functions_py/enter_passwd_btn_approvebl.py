#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def enter_passwd_btn_approvebl(q_recid:int, keystr:string, q_date1:date, q_number1:int):

    prepare_cache ([Queasy])

    reason = ""
    q_logi2 = None
    queasy = None

    qbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)

    db_session = local_storage.db_session
    keystr = keystr.strip()

    def generate_output():
        nonlocal reason, q_logi2, queasy
        nonlocal q_recid, keystr, q_date1, q_number1
        nonlocal qbuff


        nonlocal qbuff

        return {"reason": reason, "q_logi2": q_logi2}


    # qbuff = get_cache (Queasy, {"key": [(eq, 36)],"char1": [(eq, keystr)],"date1": [(eq, q_date1)],"number1": [(eq, q_number1)],"betriebsnr": [(eq, 1)]})
    qbuff = db_session.query(Queasy).filter(
             (Queasy.key == 36) &
             (Queasy.char1 == keystr) &
             (Queasy.date1 == q_date1) &
             (Queasy.number1 == q_number1) &
             (Queasy.betriebsnr == 1)).with_for_update().first()

    if not qbuff:

        return generate_output()

    if qbuff.logi1:
        reason = qbuff.char3
    pass
    qbuff.logi1 = True


    pass
    q_logi2 = qbuff.logi2

    return generate_output()