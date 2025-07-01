#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_cflow1_list, T_cflow1 = create_model_like(Queasy)

def update_status_cashflowbl(case_type:int, t_cflow1_list:[T_cflow1]):
    success_flag = False
    queasy = None

    t_cflow1 = t_queasy = None

    T_queasy = create_buffer("T_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type, t_cflow1_list
        nonlocal t_queasy


        nonlocal t_cflow1, t_queasy

        return {"success_flag": success_flag}

    if case_type == 1:

        t_cflow1 = query(t_cflow1_list, first=True)

        if t_cflow1:

            queasy = get_cache (Queasy, {"key": [(eq, 177)],"deci1": [(eq, t_cflow1.deci1)]})

            if queasy:

                t_queasy = db_session.query(T_queasy).filter(
                         (T_queasy._recid == queasy._recid)).first()
                db_session.delete(t_queasy)
                pass
                success_flag = True
    elif case_type == 2:

        t_cflow1 = query(t_cflow1_list, first=True)

        if t_cflow1:

            t_queasy = db_session.query(T_queasy).filter(
                     (T_queasy.key == 177) & (T_queasy.deci1 == t_cflow1.deci1)).first()

            if t_queasy:
                success_flag = False
            else:
                queasy = Queasy()
                db_session.add(queasy)

                buffer_copy(t_cflow1, queasy)
                success_flag = True
    elif case_type == 3:

        t_cflow1 = query(t_cflow1_list, first=True)

        if t_cflow1:

            queasy = get_cache (Queasy, {"key": [(eq, 177)],"deci1": [(eq, t_cflow1.deci1)]})

            if queasy:

                t_queasy = db_session.query(T_queasy).filter(
                         (T_queasy._recid == queasy._recid)).first()
                t_queasy.deci1 =  to_decimal(t_cflow1.deci1)
                t_queasy.char1 = t_cflow1.char1
                t_queasy.logi1 = t_cflow1.logi1


                pass
                pass
                success_flag = True

    return generate_output()