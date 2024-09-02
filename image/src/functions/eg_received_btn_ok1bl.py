from functions.additional_functions import *
import decimal
from models import Eg_budget

def eg_received_btn_ok1bl(sbudget:[Sbudget]):
    eg_budget = None

    tbudget = sbudget = None

    tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})
    sbudget_list, Sbudget = create_model_like(Tbudget)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_budget


        nonlocal tbudget, sbudget
        nonlocal tbudget_list, sbudget_list
        return {}


    for sbudget in query(sbudget_list):
        eg_budget = Eg_budget()
        db_session.add(eg_budget)

        eg_budget.nr = sbudget.res_nr
        eg_budget.YEAR = sbudget.YEAR
        eg_budget.MONTH = sbudget.MONTH
        eg_budget.score = sbudget.amount

    return generate_output()