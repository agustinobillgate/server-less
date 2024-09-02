from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nebenst, Parameters

def telext_adminbl(sorttype:int):
    t_nebenst_list = []
    cost_list_list = []
    nebenst = parameters = None

    cost_list = t_nebenst = None

    cost_list_list, Cost_list = create_model("Cost_list", {"num":int, "name":str})
    t_nebenst_list, T_nebenst = create_model_like(Nebenst, {"n_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nebenst_list, cost_list_list, nebenst, parameters


        nonlocal cost_list, t_nebenst
        nonlocal cost_list_list, t_nebenst_list
        return {"t-nebenst": t_nebenst_list, "cost-list": cost_list_list}

    def disp_it():

        nonlocal t_nebenst_list, cost_list_list, nebenst, parameters


        nonlocal cost_list, t_nebenst
        nonlocal cost_list_list, t_nebenst_list

        if sorttype == 1:

            for nebenst in db_session.query(Nebenst).all():
                assign_it()

        else:

            for nebenst in db_session.query(Nebenst).all():
                assign_it()


    def assign_it():

        nonlocal t_nebenst_list, cost_list_list, nebenst, parameters


        nonlocal cost_list, t_nebenst
        nonlocal cost_list_list, t_nebenst_list


        t_nebenst = T_nebenst()
        t_nebenst_list.append(t_nebenst)

        buffer_copy(nebenst, t_nebenst)
        t_nebenst.n_id = nebenst._recid

    def create_costlist():

        nonlocal t_nebenst_list, cost_list_list, nebenst, parameters


        nonlocal cost_list, t_nebenst
        nonlocal cost_list_list, t_nebenst_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.num = to_int(parameters.varname)
            cost_list.name = parameters.vstring

    disp_it()
    create_costlist()

    return generate_output()