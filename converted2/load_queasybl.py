#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Gl_acct

def load_queasybl(case_type:int, qno:int):
    t_queasy_data = []
    queasy = gl_acct = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, queasy, gl_acct
        nonlocal case_type, qno


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    if case_type == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == qno)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 2:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == qno) & (Queasy.logi2)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == qno) & not_ (Queasy.logi2)).order_by(Queasy.char1).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 4:

        queasy_obj_list = {}
        for queasy, gl_acct in db_session.query(Queasy, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Queasy.char3)).filter(
                 (Queasy.key == qno)).order_by(Queasy._recid).all():
            if queasy_obj_list.get(queasy._recid):
                continue
            else:
                queasy_obj_list[queasy._recid] = True


            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
    elif case_type == 11:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == qno)).order_by(Queasy._recid).all():
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            t_queasy.number3 = to_int(queasy._recid)

    return generate_output()