#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Parameters

def cost_budget_btn_gobl(fibu1:string, curr_select:string, cost_list_num:int):

    prepare_cache ([Gl_acct, Parameters])

    flag = 0
    alloc_list_data = []
    bezeich1:string = ""
    gl_acct = parameters = None

    alloc_list = None

    alloc_list_data, Alloc_list = create_model("Alloc_list", {"rec_id":int, "name":string, "bezeich":string, "fibu":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, alloc_list_data, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_data

        return {"flag": flag, "alloc-list": alloc_list_data}

    def add_alloclist():

        nonlocal flag, alloc_list_data, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_data


        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = "CostCenter"
        parameters.section = "Alloc"
        parameters.varname = to_string(cost_list_num)
        parameters.vtype = 1
        parameters.vstring = fibu1
        alloc_list = Alloc_list()
        alloc_list_data.append(alloc_list)

        alloc_list.rec_id = parameters._recid
        alloc_list.name = to_string(cost_list_num)
        alloc_list.bezeich = bezeich1
        alloc_list.fibu = fibu1


    def update_alloclist():

        nonlocal flag, alloc_list_data, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_data

        parameters = get_cache (Parameters, {"_recid": [(eq, alloc_list.rec_id)]})
        parameters.vstring = fibu1
        pass


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu1)]})

    if not gl_acct:
        flag = 1

        return generate_output()

    if curr_select.lower()  == ("add-alloc").lower() :
        bezeich1 = gl_acct.bezeich
        add_alloclist()
        flag = 2

        return generate_output()

    if curr_select.lower()  == ("chg-alloc").lower() :
        update_alloclist()
        flag = 3

    return generate_output()