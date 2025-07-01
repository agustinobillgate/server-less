#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_budget

tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
sbudget_list, Sbudget = create_model_like(Tbudget)

def eg_received_btn_ok1bl(sbudget_list:[Sbudget]):

    prepare_cache ([Eg_budget])

    tbudget_list = []
    eg_budget = None

    tbudget = sbudget = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_list, eg_budget


        nonlocal tbudget, sbudget
        nonlocal tbudget_list

        return {}


    for sbudget in query(sbudget_list):
        eg_budget = Eg_budget()
        db_session.add(eg_budget)

        eg_budget.nr = sbudget.res_nr
        eg_budget.year = sbudget.year
        eg_budget.month = sbudget.month
        eg_budget.score =  to_decimal(sbudget.amount)

    return generate_output()