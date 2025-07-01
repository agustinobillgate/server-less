#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_budget

def eg_received_btn_renartbl():
    t_eg_budget_list = []
    eg_budget = None

    t_eg_budget = None

    t_eg_budget_list, T_eg_budget = create_model_like(Eg_budget)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_budget_list, eg_budget


        nonlocal t_eg_budget
        nonlocal t_eg_budget_list

        return {"t-eg-budget": t_eg_budget_list}

    for eg_budget in db_session.query(Eg_budget).order_by(Eg_budget._recid).all():
        t_eg_budget = T_eg_budget()
        t_eg_budget_list.append(t_eg_budget)

        buffer_copy(eg_budget, t_eg_budget)

    return generate_output()