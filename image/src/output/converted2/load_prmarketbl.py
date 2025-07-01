#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Prmarket

def load_prmarketbl(case_type:int):
    t_prmarket_list = []
    prmarket = None

    t_prmarket = None

    t_prmarket_list, T_prmarket = create_model_like(Prmarket)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_prmarket_list, prmarket
        nonlocal case_type


        nonlocal t_prmarket
        nonlocal t_prmarket_list

        return {"t-prmarket": t_prmarket_list}

    if case_type == 1:

        for prmarket in db_session.query(Prmarket).order_by(Prmarket._recid).all():
            t_prmarket = T_prmarket()
            t_prmarket_list.append(t_prmarket)

            buffer_copy(prmarket, t_prmarket)

    return generate_output()