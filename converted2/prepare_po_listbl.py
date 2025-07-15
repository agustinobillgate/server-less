#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Parameters

def prepare_po_listbl():

    prepare_cache ([Htparam, Bediener, Parameters])

    enforce_rflag = False
    billdate = None
    t_bediener_data = []
    cost_list_data = []
    htparam = bediener = parameters = None

    cost_list = t_bediener = None

    cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    t_bediener_data, T_bediener = create_model("T_bediener", {"userinit":string, "username":string, "nr":int, "permissions":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, billdate, t_bediener_data, cost_list_data, htparam, bediener, parameters


        nonlocal cost_list, t_bediener
        nonlocal cost_list_data, t_bediener_data

        return {"enforce_rflag": enforce_rflag, "billdate": billdate, "t-bediener": t_bediener_data, "cost-list": cost_list_data}

    def create_costlist():

        nonlocal enforce_rflag, billdate, t_bediener_data, cost_list_data, htparam, bediener, parameters


        nonlocal cost_list, t_bediener
        nonlocal cost_list_data, t_bediener_data

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    create_costlist()

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        t_bediener = T_bediener()
        t_bediener_data.append(t_bediener)

        t_bediener.userinit = bediener.userinit
        t_bediener.username = bediener.username
        t_bediener.nr = bediener.nr
        t_bediener.permissions = bediener.permissions

    return generate_output()