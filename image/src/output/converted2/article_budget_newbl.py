#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Budget

def article_budget_newbl(from_date:date, to_date:date, fdate:date, tdate:date, artnr:int, departement:int, betrag:Decimal):
    t_budget_list = []
    datum:date = None
    budget = None

    t_budget = None

    t_budget_list, T_budget = create_model_like(Budget)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_budget_list, datum, budget
        nonlocal from_date, to_date, fdate, tdate, artnr, departement, betrag


        nonlocal t_budget
        nonlocal t_budget_list

        return {"t-budget": t_budget_list}


    for datum in date_range(fdate,tdate) :

        budget = get_cache (Budget, {"datum": [(eq, datum)],"artnr": [(eq, artnr)],"departement": [(eq, departement)]})

        if not budget:
            budget = Budget()
            db_session.add(budget)

            budget.datum = datum
            budget.artnr = artnr
            budget.departement = departement
        pass
        budget.betrag =  to_decimal(betrag)
        pass

    for budget in db_session.query(Budget).filter(
             (Budget.datum >= from_date) & (Budget.datum <= to_date)).order_by(Budget.datum).all():
        t_budget = T_budget()
        t_budget_list.append(t_budget)

        buffer_copy(budget, t_budget)

    return generate_output()