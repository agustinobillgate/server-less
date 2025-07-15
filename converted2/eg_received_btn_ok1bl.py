#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_budget

tbudget_data, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
sbudget_data, Sbudget = create_model_like(Tbudget)

def eg_received_btn_ok1bl(sbudget_data:[Sbudget]):

    prepare_cache ([Eg_budget])

    tbudget_data = []
    eg_budget = None

    tbudget = sbudget = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_data, eg_budget


        nonlocal tbudget, sbudget
        nonlocal tbudget_data

        return {}


    for sbudget in query(sbudget_data):
        eg_budget = Eg_budget()
        db_session.add(eg_budget)

        eg_budget.nr = sbudget.res_nr
        eg_budget.year = sbudget.year
        eg_budget.month = sbudget.month
        eg_budget.score =  to_decimal(sbudget.amount)

    return generate_output()