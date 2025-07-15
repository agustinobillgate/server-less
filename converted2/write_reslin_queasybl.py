#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Reslin_queasy

old_rqbuff_data, Old_rqbuff = create_model_like(Reslin_queasy)
new_rqbuff_data, New_rqbuff = create_model_like(Reslin_queasy)

def write_reslin_queasybl(case_type:int, old_rqbuff_data:[Old_rqbuff], new_rqbuff_data:[New_rqbuff]):
    success_flag = False
    i_pos:int = 0
    ct:string = ""
    reslin_queasy = None

    old_rqbuff = new_rqbuff = rqbuff = None

    Rqbuff = create_buffer("Rqbuff",Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, i_pos, ct, reslin_queasy
        nonlocal case_type
        nonlocal rqbuff


        nonlocal old_rqbuff, new_rqbuff, rqbuff

        return {"success_flag": success_flag}


    if case_type == 1:

        new_rqbuff = query(new_rqbuff_data, first=True)

        if not new_rqBuff:

            return generate_output()
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        buffer_copy(new_rQbuff, reslin_queasy)
        pass
        pass
        success_flag = True
    elif case_type == 2:

        old_rqbuff = query(old_rqbuff_data, first=True)

        new_rqbuff = query(new_rqbuff_data, first=True)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, old_rqbuff.key)],"resnr": [(eq, old_rqbuff.resnr)],"reslinnr": [(eq, old_rqbuff.reslinnr)],"number1": [(eq, old_rqbuff.number1)],"number2": [(eq, old_rqbuff.number2)],"number3": [(eq, old_rqbuff.number3)],"date1": [(eq, old_rqbuff.date1)],"date2": [(eq, old_rqbuff.date2)],"date3": [(eq, old_rqbuff.date3)],"char1": [(eq, old_rqbuff.char1)],"char2": [(eq, old_rqbuff.char2)],"char3": [(eq, old_rqbuff.char3)],"deci1": [(eq, old_rqbuff.deci1)],"deci2": [(eq, old_rqbuff.deci2)],"deci3": [(eq, old_rqbuff.deci3)],"logi1": [(eq, old_rqbuff.logi1)],"logi2": [(eq, old_rqbuff.logi2)],"logi3": [(eq, old_rqbuff.logi3)]})

        if reslin_queasy:
            buffer_copy(new_rqBuff, reslin_queasy)
            pass
            pass
            success_flag = True
    elif case_type == 3:

        old_rqbuff = query(old_rqbuff_data, first=True)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, old_rqbuff.key)],"resnr": [(eq, old_rqbuff.resnr)],"reslinnr": [(eq, old_rqbuff.reslinnr)],"number1": [(eq, old_rqbuff.number1)],"number2": [(eq, old_rqbuff.number2)],"number3": [(eq, old_rqbuff.number3)],"date1": [(eq, old_rqbuff.date1)],"date2": [(eq, old_rqbuff.date2)],"date3": [(eq, old_rqbuff.date3)],"char1": [(eq, old_rqbuff.char1)],"char2": [(eq, old_rqbuff.char2)],"char3": [(eq, old_rqbuff.char3)],"deci1": [(eq, old_rqbuff.deci1)],"deci2": [(eq, old_rqbuff.deci2)],"deci3": [(eq, old_rqbuff.deci3)],"logi1": [(eq, old_rqbuff.logi1)],"logi2": [(eq, old_rqbuff.logi2)],"logi3": [(eq, old_rqbuff.logi3)]})

        if reslin_queasy:
            db_session.delete(reslin_queasy)
            pass
            success_flag = True
    elif case_type == 4:

        new_rqbuff = query(new_rqbuff_data, first=True)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, new_rqbuff.key)],"resnr": [(eq, new_rqbuff.resnr)],"reslinnr": [(eq, new_rqbuff.reslinnr)]})

        if reslin_queasy:
            reslin_queasy.date2 = new_rqbuff.date1
            reslin_queasy.number2 = new_rqbuff.number1
            reslin_queasy.char2 = new_rqbuff.char1
            reslin_queasy.char3 = new_rqbuff.char3


            pass
        else:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            buffer_copy(new_rqbuff, reslin_queasy)
            pass

    return generate_output()