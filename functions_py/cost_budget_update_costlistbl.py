#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def cost_budget_update_costlistbl(cost_list_rec_id:int, name1:string):

    prepare_cache ([Parameters])

    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal cost_list_rec_id, name1

        return {}

    def update_costlist():

        nonlocal parameters
        nonlocal cost_list_rec_id, name1

        # parameters = get_cache (Parameters, {"_recid": [(eq, cost_list_rec_id)]})
        parameters = db_session.query(Parameters).filter(
                 (Parameters._recid == cost_list_rec_id)).with_for_update().first()
        parameters.vstring = name1
        pass


    update_costlist()

    return generate_output()