#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def cost_center_btn_gobl(case_type:int, num1:int, name1:string):

    prepare_cache ([Parameters])

    cost_list_data = []
    parameters = None

    cost_list = None

    cost_list_data, Cost_list = create_model("Cost_list", {"rec_id":int, "num":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_data, parameters
        nonlocal case_type, num1, name1


        nonlocal cost_list
        nonlocal cost_list_data

        return {"cost-list": cost_list_data}

    def add_costlist():

        nonlocal cost_list_data, parameters
        nonlocal case_type, num1, name1


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


    def update_costlist():

        nonlocal cost_list_data, parameters
        nonlocal case_type, num1, name1


        nonlocal cost_list
        nonlocal cost_list_data

        # parameters = get_cache (Parameters, {"_recid": [(eq, num1)]})
        parameters = db_session.query(Parameters).filter(
                 (Parameters._recid == num1)).with_for_update().first()

        if parameters:
            pass
            parameters.vstring = name1
            pass
            pass


    if case_type == 1:
        add_costlist()

    elif case_type == 2:
        update_costlist()

    return generate_output()