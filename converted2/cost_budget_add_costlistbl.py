#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def cost_budget_add_costlistbl(num1:int, name1:string):

    prepare_cache ([Parameters])

    cost_list_data = []
    parameters = None

    cost_list = None

    cost_list_data, Cost_list = create_model("Cost_list", {"rec_id":int, "num":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_data, parameters
        nonlocal num1, name1


        nonlocal cost_list
        nonlocal cost_list_data

        return {"cost-list": cost_list_data}

    def add_costlist():

        nonlocal cost_list_data, parameters
        nonlocal num1, name1


        nonlocal cost_list
        nonlocal cost_list_data

        i:int = 0
        m:int = 1
        n:int = 0
        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = "CostCenter"
        parameters.section = "Name"
        parameters.varname = to_string(num1)
        parameters.vtype = 1
        parameters.vstring = name1
        cost_list = Cost_list()
        cost_list_data.append(cost_list)

        cost_list.rec_id = parameters._recid
        cost_list.num = to_int(parameters.varname)
        cost_list.name = parameters.vstring

    add_costlist()

    return generate_output()