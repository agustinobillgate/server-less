#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def if_country1_add_costlistbl(zone1:string, grace1:int, wday1:int, ftime1:int, ttime1:int, tdura1:int, dura1:int, cost1:Decimal):

    prepare_cache ([Parameters])

    cost_list_list = []
    parameters = None

    cost_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "zone":string, "grace":int, "wday":int, "ftime":int, "ttime":int, "tdura":int, "dura":int, "cost":Decimal, "info":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, parameters
        nonlocal zone1, grace1, wday1, ftime1, ttime1, tdura1, dura1, cost1


        nonlocal cost_list
        nonlocal cost_list_list

        return {"cost-list": cost_list_list}

    def add_costlist():

        nonlocal cost_list_list, parameters
        nonlocal zone1, grace1, wday1, ftime1, ttime1, tdura1, dura1, cost1


        nonlocal cost_list
        nonlocal cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0
        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = "if-internal"
        parameters.section = "zone"
        parameters.varname = zone1
        parameters.vtype = 1
        parameters.vstring = to_string(grace1) + ";" + to_string(wday1) + ";" + to_string(ftime1, "9999") + ";" + to_string(ttime1, "9999") + ";" + to_string(tdura1) + ";" + to_string(dura1) + ";" + to_string(cost1, ">>>>>>9.99") + ";"
        cost_list = Cost_list()
        cost_list_list.append(cost_list)

        cost_list.rec_id = parameters._recid
        cost_list.zone = parameters.varname
        i = 1
        n = 0
        m = 1
        while i <= 7:
            n = n + 1

            if substring(parameters.vstring, n - 1, 1) == (";").lower() :

                if i == 1:
                    cost_list.grace = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 2:
                    cost_list.wday = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 3:
                    cost_list.ftime = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 4:
                    cost_list.ttime = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 5:
                    cost_list.tdura = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 6:
                    cost_list.dura = to_int(substring(parameters.vstring, m - 1, n - m))

                elif i == 7:
                    cost_list.cost = to_decimal(substring(parameters.vstring, m - 1, n - m - 3))
                    cost_list.cost = cost_list.cost + to_decimal(substring(parameters.vstring, n - 2 - 1, 2)) / 100
                m = n + 1
                i = i + 1

    add_costlist()

    return generate_output()