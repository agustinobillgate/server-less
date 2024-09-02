from functions.additional_functions import *
import decimal
from models import Queasy
t_cflow1_list, T_cflow1 = create_model_like(Queasy)
def update_status_cashflowbl(case_type:int, t_cflow1_list:[T_cflow1]):
    success_flag = False
    queasy = None

    t_cflow1 = t_queasy = None
    T_queasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal t_queasy

        nonlocal t_cflow1, t_queasy
        global t_cflow1_list
        return {"success_flag": success_flag}

    if case_type == 1:
        t_cflow1 = query(t_cflow1_list, first=True)
        if t_cflow1:
            queasy = db_session.query(Queasy).filter((Queasy.key == 177) and  (Queasy.deci1 == t_cflow1.deci1)).first()
            if queasy:
                t_queasy = db_session.query(T_queasy).filter((T_queasy._recid == queasy._recid)).first()
                db_session.delete(t_queasy)
                success_flag = True
    elif case_type == 2:
        t_cflow1 = query(t_cflow1_list, first=True)
        if t_cflow1:
            t_queasy = db_session.query(T_queasy).filter((T_queasy.key == 177) and  (T_queasy.deci1 == t_cflow1.deci1)).first()
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
            queasy = db_session.query(Queasy).filter((Queasy.key == 177) and  (t_cflow1.deci1 == Queasy.deci1)).first()
            if queasy:
                t_queasy = db_session.query(T_queasy).filter((T_queasy._recid == queasy._recid)).first()
                t_queasy.deci1 = t_cflow1.deci1
                t_queasy.char1 = t_cflow1.char1
                t_queasy.logi1 = t_cflow1.logi1
                t_queasy = db_session.query(T_queasy).first()
                success_flag = True

    return generate_output()