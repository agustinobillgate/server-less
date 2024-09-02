from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Reslin_queasy

def read_reslin_queasybl(case_type:int, rkey:str, inpchar:str, resno:int, reslinno:int, inpnum1:int, inpnum2:int, inpnum3:int, datum1:date, datum2:date):
    t_reslin_queasy_list = []
    curr_datum:date = None
    reslin_queasy = None

    t_reslin_queasy = None

    t_reslin_queasy_list, T_reslin_queasy = create_model_like(Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_reslin_queasy_list, curr_datum, reslin_queasy


        nonlocal t_reslin_queasy
        nonlocal t_reslin_queasy_list
        return {"t-reslin-queasy": t_reslin_queasy_list}

    if case_type == 1:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (Reslin_queasy.key == rkey) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 2:

        if inpchar == "" and inpnum2 == 0:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno)).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_list.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

        else:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.char1 == inpchar) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.number2 == inpnum2)).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_list.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

    elif case_type == 3:
        for curr_datum in range(datum1,datum2 + 1) :

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.date1 <= curr_datum) &  (Reslin_queasy.date2 >= curr_datum)).first()

            if reslin_queasy:

                t_reslin_queasy = query(t_reslin_queasy_list, first=True)

                if not t_reslin_queasy:
                    t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_list.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)
            else:
                t_reslin_queasy_list.remove(t_reslin_queasy)

                return generate_output()
    elif case_type == 4:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.char1 == inpchar) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.number1 == inpnum1) &  (Reslin_queasy.number2 == inpnum2)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 5:

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.char1 == inpchar) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.number1 == inpnum1) &  (Reslin_queasy.number2 == inpnum2)).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 6:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.char1 == inpchar) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.number1 == inpnum1) &  (Reslin_queasy.number2 == inpnum2) &  (Reslin_queasy.number3 == inpnum3) &  (Reslin_queasy.datum1 >= Reslin_queasy.date1) &  (Reslin_queasy.datum1 <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 7:

        for reslin_queasy in db_session.query(Reslin_queasy).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 8:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.betriebsnr == 0)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 9:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.datum1 >= Reslin_queasy.date1) &  (Reslin_queasy.datum1 <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 10:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.char1 == inpchar) &  (Reslin_queasy.number1 == inpnum1) &  (Reslin_queasy.number2 == inpnum2) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.deci1 != 0)).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 11:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == (rkey).lower()) &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.betriebsnr == inpnum1) &  ((Reslin_queasy.logi1) |  (Reslin_queasy.logi2) |  (Reslin_queasy.logi3 ))).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_list.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)

    return generate_output()