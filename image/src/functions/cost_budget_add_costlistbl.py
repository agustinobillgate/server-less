from functions.additional_functions import *
import decimal
from models import Parameters

def cost_budget_add_costlistbl(num1:int, name1:str):
    cost_list_list = []
    parameters = None

    cost_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "num":int, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, parameters


        nonlocal cost_list
        nonlocal cost_list_list
        return {"cost-list": cost_list_list}

    def add_costlist():

        nonlocal cost_list_list, parameters


        nonlocal cost_list
        nonlocal cost_list_list

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
        cost_list_list.append(cost_list)

        cost_list.rec_id = parameters._recid
        cost_list.num = to_int(parameters.varname)
        cost_list.name = parameters.vstring


    add_costlist()

    return generate_output()