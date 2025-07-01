#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

def write_queasy1bl(case_type:int, t_queasy_list:[T_queasy]):

    prepare_cache ([Queasy])

    success_flag = False
    queasy = None

    t_queasy = buf_queasy = None

    Buf_queasy = create_buffer("Buf_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type
        nonlocal buf_queasy


        nonlocal t_queasy, buf_queasy

        return {"success_flag": success_flag}

    t_queasy = query(t_queasy_list, first=True)

    if not t_queasy:

        return generate_output()

    if case_type == 1:

        queasy = get_cache (Queasy, {"_recid": [(eq, t_queasy.rec_id)]})

        if queasy:
            queasy.deci1 =  to_decimal(t_queasy.deci1)
            queasy.deci2 =  to_decimal(t_queasy.deci2)


            pass
            success_flag = True


    elif case_type == 2:

        for t_queasy in query(t_queasy_list):

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == t_queasy.key) & (Queasy.number1 == t_queasy.number1) & (Queasy.number2 == t_queasy.number2) & (Queasy.char1 == t_queasy.char1) & ((Queasy.deci1 != t_queasy.deci1) | (Queasy.deci2 != t_queasy.deci2))).first()

            if queasy:
                pass
                queasy.deci1 =  to_decimal(t_queasy.deci1)
                queasy.deci2 =  to_decimal(t_queasy.deci2)


                pass
                pass
                success_flag = True

    return generate_output()