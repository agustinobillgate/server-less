#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def cost_budget_btn_del1bl(cost_list_rec_id:int):
    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal cost_list_rec_id

        return {}


    parameters = get_cache (Parameters, {"_recid": [(eq, cost_list_rec_id)]})
    db_session.delete(parameters)

    return generate_output()