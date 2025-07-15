#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Gl_acct

def prepare_cost_budgetbl():

    prepare_cache ([Parameters, Gl_acct])

    alloc_list_data = []
    cost_list_data = []
    parameters = gl_acct = None

    alloc_list = cost_list = None

    alloc_list_data, Alloc_list = create_model("Alloc_list", {"rec_id":int, "name":string, "bezeich":string, "fibu":string})
    cost_list_data, Cost_list = create_model("Cost_list", {"rec_id":int, "num":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal alloc_list_data, cost_list_data, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_data, cost_list_data

        return {"alloc-list": alloc_list_data, "cost-list": cost_list_data}

    def create_costlist():

        nonlocal alloc_list_data, cost_list_data, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_data, cost_list_data

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.rec_id = parameters._recid
            cost_list.num = to_int(parameters.varname)
            cost_list.name = parameters.vstring


    def create_alloclist():

        nonlocal alloc_list_data, cost_list_data, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_data, cost_list_data

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Alloc").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, parameters.vstring)]})

            if gl_acct:
                alloc_list = Alloc_list()
                alloc_list_data.append(alloc_list)

                alloc_list.rec_id = parameters._recid
                alloc_list.name = parameters.varname
                alloc_list.fibu = parameters.vstring
                alloc_list.bezeich = gl_acct.bezeich


    create_costlist()
    create_alloclist()

    return generate_output()