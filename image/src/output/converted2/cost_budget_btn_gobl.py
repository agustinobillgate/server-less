from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Parameters

def cost_budget_btn_gobl(fibu1:str, curr_select:str, cost_list_num:int):
    flag = 0
    alloc_list_list = []
    bezeich1:str = ""
    gl_acct = parameters = None

    alloc_list = None

    alloc_list_list, Alloc_list = create_model("Alloc_list", {"rec_id":int, "name":str, "bezeich":str, "fibu":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, alloc_list_list, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_list
        return {"flag": flag, "alloc-list": alloc_list_list}

    def add_alloclist():

        nonlocal flag, alloc_list_list, bezeich1, gl_acct, parameters
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

        nonlocal flag, alloc_list_list, bezeich1, gl_acct, parameters
        nonlocal fibu1, curr_select, cost_list_num


        nonlocal alloc_list
        nonlocal alloc_list_list

        parameters = db_session.query(Parameters).filter(
                 (Parameters._recid == alloc_list.rec_id)).first()
        parameters.vstring = fibu1


    gl_acct = db_session.query(Gl_acct).filter(
             (func.lower(Gl_acct.fibukonto) == (fibu1).lower())).first()

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