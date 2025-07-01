#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_sel_egcategbl():

    prepare_cache ([Queasy])

    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"number1":int, "char1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 132)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.number1 = queasy.number1
        t_queasy.char1 = queasy.char1

    return generate_output()