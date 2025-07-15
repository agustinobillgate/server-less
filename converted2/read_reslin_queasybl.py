#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy

def read_reslin_queasybl(case_type:int, rkey:string, inpchar:string, resno:int, reslinno:int, inpnum1:int, inpnum2:int, inpnum3:int, datum1:date, datum2:date):
    t_reslin_queasy_data = []
    curr_datum:date = None
    reslin_queasy = None

    t_reslin_queasy = None

    t_reslin_queasy_data, T_reslin_queasy = create_model_like(Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_reslin_queasy_data, curr_datum, reslin_queasy
        nonlocal case_type, rkey, inpchar, resno, reslinno, inpnum1, inpnum2, inpnum3, datum1, datum2


        nonlocal t_reslin_queasy
        nonlocal t_reslin_queasy_data

        return {"t-reslin-queasy": t_reslin_queasy_data}

    if case_type == 1:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 2:

        if inpchar == "" and inpnum2 == 0:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno)).order_by(Reslin_queasy._recid).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

        else:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.char1 == inpchar) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.number2 == inpnum2)).order_by(Reslin_queasy._recid).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

    elif case_type == 3:
        for curr_datum in date_range(datum1,datum2) :

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(le, curr_datum)],"date2": [(ge, curr_datum)]})

            if reslin_queasy:

                t_reslin_queasy = query(t_reslin_queasy_data, first=True)

                if not t_reslin_queasy:
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)
            else:
                t_reslin_queasy_data.remove(t_reslin_queasy)

                return generate_output()
    elif case_type == 4:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"reslinnr": [(eq, reslinno)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 5:

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.char1 == inpchar) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.number1 == inpnum1) & (Reslin_queasy.number2 == inpnum2)).order_by(Reslin_queasy.resnr, Reslin_queasy.number3, Reslin_queasy.date1).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 6:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)],"number3": [(eq, inpnum3)],"date1": [(le, datum1)],"date2": [(ge, datum1)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 7:

        for reslin_queasy in db_session.query(Reslin_queasy).order_by(Reslin_queasy._recid).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 8:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"betriebsnr": [(eq, 0)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 9:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(le, datum1)],"date2": [(ge, datum1)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 10:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)],"reslinnr": [(eq, reslinno)],"deci1": [(ne, 0)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 11:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.betriebsnr == inpnum1) & ((Reslin_queasy.logi1) | (Reslin_queasy.logi2) | (Reslin_queasy.logi3))).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)

    return generate_output()