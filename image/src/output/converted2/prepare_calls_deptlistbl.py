#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Parameters

def prepare_calls_deptlistbl():

    prepare_cache ([Htparam, Parameters])

    double_currency = False
    price_decimal = 0
    cost1 = 0
    cost2 = 0
    cost_list_list = []
    htparam = parameters = None

    cost_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"num":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, price_decimal, cost1, cost2, cost_list_list, htparam, parameters


        nonlocal cost_list
        nonlocal cost_list_list

        return {"double_currency": double_currency, "price_decimal": price_decimal, "cost1": cost1, "cost2": cost2, "cost-list": cost_list_list}

    def create_costlist():

        nonlocal double_currency, price_decimal, cost1, cost2, cost_list_list, htparam, parameters


        nonlocal cost_list
        nonlocal cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0
        cost_list_list.clear()

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.num = to_int(parameters.varname)
            cost_list.name = parameters.vstring

            if cost1 > cost_list.num:
                cost1 = cost_list.num

            if cost2 < cost_list.num:
                cost2 = cost_list.num


    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    create_costlist()

    return generate_output()