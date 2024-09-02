from functions.additional_functions import *
import decimal
from datetime import date
from models import Budget

def article_budget_newbl(from_date:date, to_date:date, fdate:date, tdate:date, artnr:int, departement:int, betrag:decimal):
    t_budget_list = []
    datum:date = None
    budget = None

    t_budget = None

    t_budget_list, T_budget = create_model_like(Budget)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_budget_list, datum, budget


        nonlocal t_budget
        nonlocal t_budget_list
        return {"t-budget": t_budget_list}


    for datum in range(fdate,tdate + 1) :

        budget = db_session.query(Budget).filter(
                (Budget.datum == datum) &  (Budget.artnr == artnr) &  (Budget.departement == departement)).first()

        if not budget:
            budget = Budget()
            db_session.add(budget)

            budget.datum = datum
            budget.artnr = artnr
            budget.departement = departement

        budget = db_session.query(Budget).first()
        budget.betrag = betrag

        budget = db_session.query(Budget).first()

    for budget in db_session.query(Budget).filter(
            (Budget.datum >= from_date) &  (Budget.datum <= to_date)).all():
        t_budget = T_budget()
        t_budget_list.append(t_budget)

        buffer_copy(budget, t_budget)

    return generate_output()