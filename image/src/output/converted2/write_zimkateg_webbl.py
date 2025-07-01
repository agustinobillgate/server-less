#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy

t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg, {"priority":int, "max_avail":int})

def write_zimkateg_webbl(case_type:int, t_zimkateg_list:[T_zimkateg]):

    prepare_cache ([Queasy])

    success_flag = False
    zimkateg = queasy = None

    t_zimkateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, zimkateg, queasy
        nonlocal case_type


        nonlocal t_zimkateg

        return {"success_flag": success_flag}

    t_zimkateg = query(t_zimkateg_list, first=True)

    if not t_zimkateg:

        return generate_output()

    if case_type == 1:
        zimkateg = Zimkateg()
        db_session.add(zimkateg)

        buffer_copy(t_zimkateg, zimkateg)
        pass

        queasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, t_zimkateg.zikatnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 325
            queasy.number1 = t_zimkateg.zikatnr
            queasy.number2 = t_zimkateg.priority
            queasy.number3 = t_zimkateg.max_avail


            pass
        else:
            pass
            queasy.number2 = t_zimkateg.priority
            queasy.number3 = t_zimkateg.max_avail


            pass
            pass
        success_flag = True


    elif case_type == 2:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, t_zimkateg.zikatnr)]})

        if zimkateg:
            buffer_copy(t_zimkateg, zimkateg)
            pass

            queasy = get_cache (Queasy, {"key": [(eq, 325)],"number1": [(eq, t_zimkateg.zikatnr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 325
                queasy.number1 = t_zimkateg.zikatnr
                queasy.number2 = t_zimkateg.priority
                queasy.number3 = t_zimkateg.max_avail


                pass
            else:
                pass
                queasy.number2 = t_zimkateg.priority
                queasy.number3 = t_zimkateg.max_avail


                pass
                pass
            success_flag = True

    return generate_output()