#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.article_budget_disp_itbl import article_budget_disp_itbl
from models import Budget, Artikel

def article_budget_entry_deptbl(dept:int, from_date:date, to_date:date):
    t_artikel_data = []
    t_budget_data = []
    budget = artikel = None

    t_budget = t_artikel = None

    t_budget_data, T_budget = create_model_like(Budget)
    t_artikel_data, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_data, t_budget_data, budget, artikel
        nonlocal dept, from_date, to_date


        nonlocal t_budget, t_artikel
        nonlocal t_budget_data, t_artikel_data

        return {"t-artikel": t_artikel_data, "t-budget": t_budget_data}


    for artikel in db_session.query(Artikel).filter(
             (Artikel.departement == dept) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel.bezeich).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    t_artikel = query(t_artikel_data, first=True)

    if t_artikel:
        t_budget_data = get_output(article_budget_disp_itbl(t_artikel.departement, t_artikel.artnr, from_date, to_date))

    return generate_output()