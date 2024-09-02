from functions.additional_functions import *
import decimal
from datetime import date
from models import Budget

def article_budget_disp_itbl(departement:int, artnr:int, from_date:date, to_date:date):
    t_budget_list = []
    budget = None

    t_budget = None

    t_budget_list, T_budget = create_model_like(Budget)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_budget_list, budget


        nonlocal t_budget
        nonlocal t_budget_list
        return {"t-budget": t_budget_list}

    for budget in db_session.query(Budget).filter(
            (Budget.departement == departement) &  (Budget.datum >= from_date) &  (Budget.datum <= to_date)).all():
        t_budget = T_budget()
        t_budget_list.append(t_budget)

        buffer_copy(budget, t_budget)

    return generate_output()