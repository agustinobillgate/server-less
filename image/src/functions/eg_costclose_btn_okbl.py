from functions.additional_functions import *
import decimal
from models import Eg_budget, Eg_cost

def eg_costclose_btn_okbl(styear:int, stmonth:int, intres:int, user_init:str):
    eg_budget = eg_cost = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_budget, eg_cost


        return {}


    eg_budget = db_session.query(Eg_budget).filter(
            (Eg_budget.YEAR == styear) &  (Eg_budget.MONTH == stmonth) &  (Eg_budget.nr == intres)).first()

    if eg_budget:
        eg_budget.closeflag = True
        eg_budget.close_date = get_current_date()
        eg_budget.close_time = get_current_time_in_seconds()
        eg_budget.close_by = user_init


    else:
        pass

    eg_cost = db_session.query(Eg_cost).filter(
            (Eg_cost.YEAR == styear) &  (Eg_cost.MONTH == stmonth) &  (Eg_cost.resource_nr == intres)).first()

    if eg_cost:
        eg_cost.closeflag = True
        eg_cost.close_date = get_current_date()
        eg_cost.close_time = get_current_time_in_seconds()
        eg_cost.close_by = user_init


    else:
        pass

    return generate_output()