from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, Parameters

def prepare_po_listbl():
    enforce_rflag = False
    billdate = None
    t_bediener_list = []
    cost_list_list = []
    htparam = bediener = parameters = None

    cost_list = t_bediener = None

    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":str})
    t_bediener_list, T_bediener = create_model("T_bediener", {"userinit":str, "username":str, "nr":int, "permissions":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, billdate, t_bediener_list, cost_list_list, htparam, bediener, parameters


        nonlocal cost_list, t_bediener
        nonlocal cost_list_list, t_bediener_list
        return {"enforce_rflag": enforce_rflag, "billdate": billdate, "t-bediener": t_bediener_list, "cost-list": cost_list_list}

    def create_costlist():

        nonlocal enforce_rflag, billdate, t_bediener_list, cost_list_list, htparam, bediener, parameters


        nonlocal cost_list, t_bediener
        nonlocal cost_list_list, t_bediener_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate
    create_costlist()

    for bediener in db_session.query(Bediener).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        t_bediener.userinit = bediener.userinit
        t_bediener.username = bediener.username
        t_bediener.nr = bediener.nr
        t_bediener.permissions = bediener.permissions

    return generate_output()