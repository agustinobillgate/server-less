#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Queasy

def update_global_allotment_preparebl():

    prepare_cache ([Queasy])

    ci_date = None
    q_list_list = []
    queasy = None

    q_list = None

    q_list_list, Q_list = create_model("Q_list", {"char1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, q_list_list, queasy


        nonlocal q_list
        nonlocal q_list_list

        return {"ci_date": ci_date, "q-list": q_list_list}


    ci_date = get_output(htpdate(87))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 147)).order_by(Queasy.char1).all():
        q_list = Q_list()
        q_list_list.append(q_list)

        q_list.char1 = queasy.char1

    return generate_output()