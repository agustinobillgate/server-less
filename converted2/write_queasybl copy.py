from functions.additional_functions import *
import decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy)
t_queasy1_list, T_queasy1 = create_model_like(Queasy)

def write_queasybl(case_type:int, t_queasy_list:[T_queasy], t_queasy1_list:[T_queasy1]):
    success_flag = False
    curr_count:int = 0
    queasy = None

    t_queasy = t_queasy1 = qbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_count, queasy
        nonlocal case_type, t_queasy1_list
        nonlocal qbuff


        nonlocal t_queasy, t_queasy1, qbuff
        nonlocal t_queasy_list, t_queasy1_list
        return {"success_flag": success_flag}


    if not t_queasy:
        t_queasy = query(t_queasy_list, first=True)

    if case_type == 1:

        if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1)).first()

        if queasy:
            buffer_copy(t_queasy, queasy)
            success_flag = True
    elif case_type == 2:

        if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1)).first()

        if not queasy:
            queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        success_flag = True
    elif case_type == 3:

        for t_queasy in query(t_queasy_list):
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
            pass
        success_flag = True
    elif case_type == 4:
        pass

        for t_queasy in query(t_queasy_list):

            if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1)).first()

            if queasy:
                buffer_copy(t_queasy, queasy)
                success_flag = True
    elif case_type == 5:

        if not t_queasy1:
            t_queasy1 = query(t_queasy1_list, first=True)

        if not queasy or not(queasy.key == t_queasy1.key and queasy.number1 == t_queasy1.number1 and queasy.char1 == t_queasy1.char1 and queasy.betriebsnr == t_queasy.betriebsnr and queasy.deci1 == t_queasy1.deci1 and queasy.date1 == t_queasy.date1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy1.key) &  (Queasy.number1 == t_queasy1.number1) &  (Queasy.char1 == t_queasy1.char1) &  (Queasy.betriebsnr == t_queasy.betriebsnr) &  (Queasy.deci1 == t_queasy1.deci1) &  (Queasy.date1 == t_queasy.date1)).first()

        if queasy:
            buffer_copy(t_queasy, queasy)
            success_flag = True
    elif case_type == 6:

        if not t_queasy1:
            t_queasy1 = query(t_queasy1_list, first=True)

        if not queasy or not(queasy.key == t_queasy1.key and queasy.char1 == t_queasy1.char1 and queasy.betriebsnr == t_queasy.betriebsnr and queasy.deci1 == t_queasy1.deci1 and queasy.date1 == t_queasy.date1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy1.key) &  (Queasy.char1 == t_queasy1.char1) &  (Queasy.betriebsnr == t_queasy.betriebsnr) &  (Queasy.deci1 == t_queasy1.deci1) &  (Queasy.date1 == t_queasy.date1)).first()

        if queasy:
            buffer_copy(t_queasy, queasy)
            success_flag = True
    elif case_type == 7:

        if not queasy or not(queasy.key == t_queasy.key and queasy.number3 == t_queasy.number3):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number3 == t_queasy.number3)).first()

        if queasy:
            buffer_copy(t_queasy, queasy)
            success_flag = True
    elif case_type == 11:

        if not queasy or not(queasy._recid == t_queasy.number3):
            queasy = db_session.query(Queasy).filter(
                (Queasy._recid == t_queasy.number3)).first()

        if queasy:
            buffer_copy(t_queasy, queasy,except_fields=["number3"])
            success_flag = True
    elif case_type == 12:

        if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1)).first()

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True
    elif case_type == 13:

        if not queasy or not(queasy.key == 157 and queasy.date1 == get_current_date()):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 157) &  (Queasy.date1 == get_current_date())).first()

        if queasy and queasy.number1 >= 1:
            queasy.number1 = queasy.number1 - 1


        success_flag = True
    elif case_type == 14:
        curr_count = t_queasy.number1

        if not queasy or not(queasy.key == t_queasy.key and queasy.number1 <= t_queasy.number1 and queasy.betriebsnr == 1):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == t_queasy.key) &  (Queasy.number1 <= t_queasy.number1) &  (Queasy.betriebsnr == 1)).first()
        while None != queasy:

            if not qbuff or not(qbuff._recid == queasy._recid):
                qbuff = db_session.query(Qbuff).filter(
                    (Qbuff._recid == queasy._recid)).first()

            if qbuff:
                db_session.delete(qbuff)
                pass
                success_flag = True

            if not queasy or not(queasy.key == t_queasy.key and queasy.number1 <= t_queasy.number1 and queasy.betriebsnr == 1):
                curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == t_queasy.key) &  (Queasy.number1 <= t_queasy.number1) &  (Queasy.betriebsnr == 1)).filter(Queasy._recid > curr_recid).first()
    elif case_type == 15:

        if not queasy or not(queasy.key == 37 and queasy.betriebsnr == 2):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 37) &  (Queasy.betriebsnr == 2)).first()
        while None != queasy:

            if not qbuff or not(qbuff._recid == queasy._recid):
                qbuff = db_session.query(Qbuff).filter(
                    (Qbuff._recid == queasy._recid)).first()

            if qbuff:
                db_session.delete(qbuff)
                pass
                success_flag = True

            if not queasy or not(queasy.key == 37 and queasy.betriebsnr == 2):
                curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 37) &  (Queasy.betriebsnr == 2)).filter(Queasy._recid > curr_recid).first()
    elif case_type == 16:

        for t_queasy in query(t_queasy_list):

            if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1 and queasy.number2 == t_queasy.number2 and queasy.char1 == t_queasy.char1):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1) &  (Queasy.number2 == t_queasy.number2) &  (Queasy.char1 == t_queasy.char1)).first()

            if queasy:
                db_session.delete(queasy)
                pass
                success_flag = True

    elif case_type == 17:

        for t_queasy in query(t_queasy_list):

            if not queasy or not(queasy.key == t_queasy.key and queasy.number1 == t_queasy.number1 and queasy.number2 == t_queasy.number2 and queasy.char1 == t_queasy.char1):
                queasy = db_session.query(Queasy).filter(
                    (Queasy.key == t_queasy.key) &  (Queasy.number1 == t_queasy.number1) &  (Queasy.number2 == t_queasy.number2) &  (Queasy.char1 == t_queasy.char1)).first()

            if queasy:
                buffer_copy(t_queasy, queasy)
                pass
                success_flag = True


    return generate_output()