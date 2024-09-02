from functions.additional_functions import *
import decimal
from models import Queasy, Gl_acct

def load_queasybl(case_type:int, qno:int):
    t_queasy_list = []
    queasy = gl_acct = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy, gl_acct


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    if case_type == 1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == qno)).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 2:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == qno) &  (Queasy.logi2)).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 3:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == qno) &  (not Queasy.logi2)).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 4:

        queasy_obj_list = []
        for queasy, gl_acct in db_session.query(Queasy, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Queasy.char3)).filter(
                (Queasy.key == qno)).all():
            if queasy._recid in queasy_obj_list:
                continue
            else:
                queasy_obj_list.append(queasy._recid)


            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 11:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == qno)).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            t_queasy.number3 = to_int(queasy._recid)

    return generate_output()