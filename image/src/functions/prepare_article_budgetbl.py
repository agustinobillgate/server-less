from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, Artikel, Budget, Htparam

def prepare_article_budgetbl(dept:int):
    price_decimal = 0
    bill_date = None
    from_date = None
    to_date = None
    t_hoteldpt_list = []
    t_artikel_list = []
    t_budget_list = []
    hoteldpt = artikel = budget = htparam = None

    t_hoteldpt = t_artikel = t_budget = None

    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_budget_list, T_budget = create_model_like(Budget)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, bill_date, from_date, to_date, t_hoteldpt_list, t_artikel_list, t_budget_list, hoteldpt, artikel, budget, htparam


        nonlocal t_hoteldpt, t_artikel, t_budget
        nonlocal t_hoteldpt_list, t_artikel_list, t_budget_list
        return {"price_decimal": price_decimal, "bill_date": bill_date, "from_date": from_date, "to_date": to_date, "t-hoteldpt": t_hoteldpt_list, "t-artikel": t_artikel_list, "t-budget": t_budget_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    from_date = bill_date
    to_date = from_date

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    for artikel in db_session.query(Artikel).filter(
            (Artikel.departement == dept) &  ((Artikel.artart == 0) |  (Artikel.artart == 8))).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    for budget in db_session.query(Budget).filter(
            (Budget.departement == dept) &  (Budget.datum >= from_date) &  (Budget.datum <= to_date)).all():
        t_budget = T_budget()
        t_budget_list.append(t_budget)

        buffer_copy(budget, t_budget)

    return generate_output()