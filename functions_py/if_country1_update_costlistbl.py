#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country1_update_costlistbl(cost_list_rec_id:int, zone1:string, grace1:int, wday1:int, ftime1:int, ttime1:int, tdura1:int, dura1:int, cost1:Decimal):

    prepare_cache ([Parameters])

    parameters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal parameters
        nonlocal cost_list_rec_id, zone1, grace1, wday1, ftime1, ttime1, tdura1, dura1, cost1

        return {}

    def update_costlist():

        nonlocal parameters
        nonlocal cost_list_rec_id, zone1, grace1, wday1, ftime1, ttime1, tdura1, dura1, cost1

        s:string = ""

        parameters = get_cache (Parameters, {"_recid": [(eq, cost_list_rec_id)]})
        if parameters:
            parameters.vstring = to_string(grace1) + ";" + to_string(wday1) + ";" + to_string(ftime1, "9999") + ";" + to_string(ttime1, "9999") + ";" + to_string(tdura1) + ";" + to_string(dura1) + ";" + to_string(cost1, ">>>>>>9.99") + ";" + s
        pass


    update_costlist()

    return generate_output()