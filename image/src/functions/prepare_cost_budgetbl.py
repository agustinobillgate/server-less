from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters, Gl_acct

def prepare_cost_budgetbl():
    alloc_list_list = []
    cost_list_list = []
    parameters = gl_acct = None

    alloc_list = cost_list = None

    alloc_list_list, Alloc_list = create_model("Alloc_list", {"rec_id":int, "name":str, "bezeich":str, "fibu":str})
    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "num":int, "name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal alloc_list_list, cost_list_list, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_list, cost_list_list
        return {"alloc-list": alloc_list_list, "cost-list": cost_list_list}

    def create_costlist():

        nonlocal alloc_list_list, cost_list_list, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_list, cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.rec_id = parameters._recid
            cost_list.num = to_int(parameters.varname)
            cost_list.name = parameters.vstring

    def create_alloclist():

        nonlocal alloc_list_list, cost_list_list, parameters, gl_acct


        nonlocal alloc_list, cost_list
        nonlocal alloc_list_list, cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Alloc") &  (Parameters.varname > "")).all():

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == parameters.vstring)).first()

            if gl_acct:
                alloc_list = Alloc_list()
                alloc_list_list.append(alloc_list)

                alloc_list.rec_id = parameters._recid
                alloc_list.name = parameters.varname
                alloc_list.fibu = parameters.vstring
                alloc_list.bezeich = gl_acct.bezeich

    create_costlist()
    create_alloclist()

    return generate_output()