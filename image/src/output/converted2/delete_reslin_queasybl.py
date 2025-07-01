#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reslin_queasy

t_reslin_queasy_list, T_reslin_queasy = create_model_like(Reslin_queasy)

def delete_reslin_queasybl(t_reslin_queasy_list:[T_reslin_queasy]):
    success_flag = False
    reslin_queasy = None

    t_reslin_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, reslin_queasy


        nonlocal t_reslin_queasy

        return {"success_flag": success_flag}

    t_reslin_queasy = query(t_reslin_queasy_list, first=True)

    if t_reslin_queasy:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, t_reslin_queasy.key)],"resnr": [(eq, t_reslin_queasy.resnr)],"reslinnr": [(eq, t_reslin_queasy.reslinnr)],"number1": [(eq, t_reslin_queasy.number1)],"number2": [(eq, t_reslin_queasy.number2)],"number3": [(eq, t_reslin_queasy.number3)],"date1": [(eq, t_reslin_queasy.date1)],"date2": [(eq, t_reslin_queasy.date2)],"date3": [(eq, t_reslin_queasy.date3)],"char1": [(eq, t_reslin_queasy.char1)],"char2": [(eq, t_reslin_queasy.char2)],"char3": [(eq, t_reslin_queasy.char3)],"deci1": [(eq, t_reslin_queasy.deci1)],"deci2": [(eq, t_reslin_queasy.deci2)],"deci3": [(eq, t_reslin_queasy.deci3)],"logi1": [(eq, t_reslin_queasy.logi1)],"logi2": [(eq, t_reslin_queasy.logi2)],"logi3": [(eq, t_reslin_queasy.logi3)]})

    if reslin_queasy:
        db_session.delete(reslin_queasy)
        pass
        success_flag = True

    return generate_output()