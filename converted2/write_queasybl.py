#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_data, T_queasy = create_model_like(Queasy)
t_queasy1_data, T_queasy1 = create_model_like(Queasy)

def write_queasybl(case_type:int, t_queasy_data:[T_queasy], t_queasy1_data:[T_queasy1]):
    success_flag = False
    curr_count:int = 0
    queasy = None

    t_queasy = t_queasy1 = qbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_count, queasy
        nonlocal case_type, t_queasy1_data
        nonlocal qbuff


        nonlocal t_queasy, t_queasy1, qbuff

        return {"success_flag": success_flag}


    t_queasy = query(t_queasy_data, first=True)

    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)]})

        if queasy:
            buffer_copy(t_queasy, queasy)
            pass
            success_flag = True
    elif case_type == 2:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        pass
        success_flag = True
    elif case_type == 3:

        for t_queasy in query(t_queasy_data):
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
            pass
            pass
        success_flag = True
    elif case_type == 4:
        pass

        for t_queasy in query(t_queasy_data):

            queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)]})

            if queasy:
                buffer_copy(t_queasy, queasy)
                pass
                success_flag = True
    elif case_type == 5:

        t_queasy1 = query(t_queasy1_data, first=True)

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy1.key)],"number1": [(eq, t_queasy1.number1)],"char1": [(eq, t_queasy1.char1)],"betriebsnr": [(eq, t_queasy.betriebsnr)],"deci1": [(eq, t_queasy1.deci1)],"date1": [(eq, t_queasy.date1)]})

        if queasy:
            buffer_copy(t_queasy, queasy)
            pass
            success_flag = True
    elif case_type == 6:

        t_queasy1 = query(t_queasy1_data, first=True)

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy1.key)],"char1": [(eq, t_queasy1.char1)],"betriebsnr": [(eq, t_queasy.betriebsnr)],"deci1": [(eq, t_queasy1.deci1)],"date1": [(eq, t_queasy.date1)]})

        if queasy:
            buffer_copy(t_queasy, queasy)
            pass
            success_flag = True
    elif case_type == 7:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number3": [(eq, t_queasy.number3)]})

        if queasy:
            buffer_copy(t_queasy, queasy)
            pass
            success_flag = True
    elif case_type == 11:

        queasy = get_cache (Queasy, {"_recid": [(eq, t_queasy.number3)]})

        if queasy:
            buffer_copy(t_queasy, queasy,except_fields=["number3"])
            pass
            success_flag = True
    elif case_type == 12:

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)]})

        if queasy:
            db_session.delete(queasy)
            pass
            success_flag = True
    elif case_type == 13:

        queasy = get_cache (Queasy, {"key": [(eq, 157)],"date1": [(eq, get_current_date())]})

        if queasy and queasy.number1 >= 1:
            pass
            queasy.number1 = queasy.number1 - 1


            pass
        success_flag = True
    elif case_type == 14:
        curr_count = t_queasy.number1

        queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(le, t_queasy.number1)],"betriebsnr": [(eq, 1)]})
        while None != queasy:

            qbuff = db_session.query(Qbuff).filter(
                     (Qbuff._recid == queasy._recid)).first()

            if qbuff:
                db_session.delete(qbuff)
                pass
                success_flag = True

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == t_queasy.key) & (Queasy.number1 <= t_queasy.number1) & (Queasy.betriebsnr == 1) & (Queasy._recid > curr_recid)).first()
    elif case_type == 15:

        queasy = get_cache (Queasy, {"key": [(eq, 37)],"betriebsnr": [(eq, 2)]})
        while None != queasy:

            qbuff = db_session.query(Qbuff).filter(
                     (Qbuff._recid == queasy._recid)).first()

            if qbuff:
                db_session.delete(qbuff)
                pass
                success_flag = True

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 37) & (Queasy.betriebsnr == 2) & (Queasy._recid > curr_recid)).first()
    elif case_type == 16:

        for t_queasy in query(t_queasy_data):

            queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)],"number2": [(eq, t_queasy.number2)],"char1": [(eq, t_queasy.char1)]})

            if queasy:
                db_session.delete(queasy)
                pass
                success_flag = True

    elif case_type == 17:

        for t_queasy in query(t_queasy_data):

            queasy = get_cache (Queasy, {"key": [(eq, t_queasy.key)],"number1": [(eq, t_queasy.number1)],"number2": [(eq, t_queasy.number2)],"char1": [(eq, t_queasy.char1)]})

            if queasy:
                buffer_copy(t_queasy, queasy)
                pass
                pass
                success_flag = True


    return generate_output()