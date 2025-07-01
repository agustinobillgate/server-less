#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Parameters

def cost_center_btn_go2bl(fibu1:string, curr_select:string, cost_list_num:int):

    prepare_cache ([Gl_acct, Parameters])

    err_code = 0
    alloc_list_list = []
    bezeich1:string = ""
    gl_acct = parameters = None

    alloc_list = None

    alloc_list_list, Alloc_list = create_model("Alloc_list", {"rec_id":int, "name":string, "bezeich":string, "fibu":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, alloc_list_list, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_list

        return {"err_code": err_code, "alloc-list": alloc_list_list}

    def add_alloclist():

        nonlocal err_code, alloc_list_list, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_list


        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = "CostCenter"
        parameters.section = "Alloc"
        parameters.varname = to_string(cost_list_num)
        parameters.vtype = 1
        parameters.vstring = fibu1
        alloc_list = Alloc_list()
        alloc_list_list.append(alloc_list)

        alloc_list.rec_id = parameters._recid
        alloc_list.name = to_string(cost_list_num)
        alloc_list.bezeich = bezeich1
        alloc_list.fibu = fibu1


    def update_alloclist():

        nonlocal err_code, alloc_list_list, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_list

        parameters = get_cache (Parameters, {"_recid": [(eq, alloc_list.rec_id)]})
        parameters.vstring = fibu1
        pass


    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu1)]})

    if not gl_acct:
        err_code = 1

        return generate_output()

    if curr_select.lower()  == ("add-alloc").lower() :
        bezeich1 = gl_acct.bezeich
        add_alloclist()

    if curr_select.lower()  == ("chg-alloc").lower() :
        update_alloclist()

    return generate_output()