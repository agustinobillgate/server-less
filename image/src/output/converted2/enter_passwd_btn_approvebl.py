from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy

def enter_passwd_btn_approvebl(q_recid:int, keystr:str, q_date1:date, q_number1:int):
    reason = ""
    q_logi2 = None
    queasy = None

    qbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal reason, q_logi2, queasy
        nonlocal q_recid, keystr, q_date1, q_number1
        nonlocal qbuff


        nonlocal qbuff
        return {"reason": reason, "q_logi2": q_logi2}


    qbuff = db_session.query(Qbuff).filter(
             (Qbuff.key == 36) & (func.lower(Qbuff.char1) == (keystr).lower()) & (Qbuff.date1 == q_date1) & (Qbuff.number1 == q_number1) & (Qbuff.betriebsnr == 1)).first()

    if not qbuff:

        return generate_output()

    if qbuff.logi1:
        reason = qbuff.char3
    qbuff.logi1 = True


    q_logi2 = qbuff.logi2

    return generate_output()