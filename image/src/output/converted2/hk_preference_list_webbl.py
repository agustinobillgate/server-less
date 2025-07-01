#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Res_line

def hk_preference_list_webbl(qno:int):

    prepare_cache ([Res_line])

    t_queasy_list = []
    guest_name:string = ""
    queasy = res_line = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"guestname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, guest_name, queasy, res_line
        nonlocal qno


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == qno)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.number3 = to_int(queasy._recid)

        res_line = get_cache (Res_line, {"zinr": [(eq, queasy.char1)],"active_flag": [(eq, 1)],"resnr": [(ne, 0)]})

        if res_line:
            guest_name = res_line.name

    return generate_output()