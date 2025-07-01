#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def main_fs_display_page3bl():

    prepare_cache ([Queasy])

    t_q_list = []
    queasy = None

    t_q = None

    t_q_list, T_q = create_model("T_q", {"number1":int, "char3":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_q_list, queasy


        nonlocal t_q
        nonlocal t_q_list

        return {"t-q": t_q_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 148) & (Queasy.char3 != "") & (Queasy.number1 != 0)).order_by(Queasy._recid).all():
        t_q = T_q()
        t_q_list.append(t_q)

        t_q.number1 = queasy.number1
        t_q.char3 = queasy.char3

    return generate_output()