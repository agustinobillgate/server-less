#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Queasy

def prepare_eg_rephistorymoveallbl():
    ci_date = None
    t_queasy133_list = []
    queasy = None

    t_queasy133 = None

    t_queasy133_list, T_queasy133 = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, t_queasy133_list, queasy


        nonlocal t_queasy133
        nonlocal t_queasy133_list

        return {"ci_date": ci_date, "t-queasy133": t_queasy133_list}


    ci_date = get_output(htpdate(87))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        t_queasy133 = T_queasy133()
        t_queasy133_list.append(t_queasy133)

        buffer_copy(queasy, t_queasy133)

    return generate_output()