#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_budget, Eg_cost

def eg_costclose_btn_okbl(styear:int, stmonth:int, intres:int, user_init:string):

    prepare_cache ([Eg_budget, Eg_cost])

    eg_budget = eg_cost = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_budget, eg_cost
        nonlocal styear, stmonth, intres, user_init

        return {}


    eg_budget = get_cache (Eg_budget, {"year": [(eq, styear)],"month": [(eq, stmonth)],"nr": [(eq, intres)]})

    if eg_budget:
        eg_budget.closeflag = True
        eg_budget.close_date = get_current_date()
        eg_budget.close_time = get_current_time_in_seconds()
        eg_budget.close_by = user_init


    else:
        pass

    eg_cost = get_cache (Eg_cost, {"year": [(eq, styear)],"month": [(eq, stmonth)],"resource_nr": [(eq, intres)]})

    if eg_cost:
        eg_cost.closeflag = True
        eg_cost.close_date = get_current_date()
        eg_cost.close_time = get_current_time_in_seconds()
        eg_cost.close_by = user_init


    else:
        pass

    return generate_output()