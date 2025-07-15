from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Hoteldpt

def mn_del_old_selforderbl():
    i = 0
    ci_date:date = None
    order_date:date = None
    dynamic_date:date = None
    st_duration:int = 0
    queasy = htparam = hoteldpt = None

    qbuff = del_queasy = None

    Qbuff = create_buffer("Qbuff",Queasy)
    Del_queasy = create_buffer("Del_queasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, order_date, dynamic_date, st_duration, queasy, htparam, hoteldpt
        nonlocal qbuff, del_queasy


        nonlocal qbuff, del_queasy
        return {"i": i}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt.num).all():
        st_duration = 0

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 30) & (Queasy.number3 == 1) & (Queasy.betriebsnr == hoteldpt.num)).first()

        if queasy:
            st_duration = to_int(queasy.char2)

        if st_duration > 0:

            if st_duration <= 60:
                st_duration = 366

            qbuff = db_session.query(Qbuff).filter(
                     (Qbuff.key == 225) & ((func.lower(Qbuff.char1) == ("orderbill").lower()) | (func.lower(Qbuff.char1) == ("orderbill-line").lower())) & (Qbuff.number1 == hoteldpt.num) & (Qbuff.date1 != None) & ((Qbuff.date1 + st_duration <= ci_date))).first()
            while None != qbuff:
                i = i + 1

                del_queasy = db_session.query(Del_queasy).filter(
                             (Del_queasy._recid == Del_queasy._recid)).first()
                del_queasy_list.remove(del_queasy)
                pass


                curr_recid = qbuff._recid
                qbuff = db_session.query(Qbuff).filter(
                         (Qbuff.key == 225) & ((func.lower(Qbuff.char1) == ("orderbill").lower()) | (func.lower(Qbuff.char1) == ("orderbill-line").lower())) & (Qbuff.number1 == hoteldpt.num) & (Qbuff.date1 != None) & ((Qbuff.date1 + st_duration <= ci_date))).filter(Qbuff._recid > curr_recid).first()

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.number2 == 14) & (Queasy.number3 == 4) & (Queasy.betriebsnr == hoteldpt.num) & (Queasy.logi1)).first()

            if queasy:

                qbuff = db_session.query(Qbuff).filter(
                         (Qbuff.key == 225) & (func.lower(Qbuff.char1) == ("taken-table").lower()) & (Qbuff.number1 == hoteldpt.num) & (Qbuff.logi2) & ((date_mdy(entry(1, entry(3, Qbuff.char2, "|Qbuff.") , "=Qbuff.")) + st_duration <= ci_date))).first()
                while None != qbuff:
                    i = i + 1

                    del_queasy = db_session.query(Del_queasy).filter(
                                 (Del_queasy._recid == Del_queasy._recid)).first()
                    del_queasy_list.remove(del_queasy)
                    pass


                    curr_recid = qbuff._recid
                    qbuff = db_session.query(Qbuff).filter(
                             (Qbuff.key == 225) & (func.lower(Qbuff.char1) == ("taken-table").lower()) & (Qbuff.number1 == hoteldpt.num) & (Qbuff.logi2) & ((date_mdy(entry(1, entry(3, Qbuff.char2, "|Qbuff.") , "=Qbuff.")) + st_duration <= ci_date))).filter(Qbuff._recid > curr_recid).first()

    return generate_output()