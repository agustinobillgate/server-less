from functions.additional_functions import *
import decimal
from models import Parameters

def if_country_add_costlistbl(zone1:str, grace1:int, wday1:int, ftime1:int, ttime1:int, tdura1:int, dura1:int, cost1:decimal):
    cost_list_list = []
    parameters = None

    cost_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "zone":str, "grace":int, "wday":int, "ftime":int, "ttime":int, "tdura":int, "dura":int, "cost":decimal, "info":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, parameters


        nonlocal cost_list
        nonlocal cost_list_list
        return {"cost-list": cost_list_list}

    def add_costlist():

        nonlocal cost_list_list, parameters


        nonlocal cost_list
        nonlocal cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0
        s:str = ""
        k:int = 0
        parameters = Parameters()
        db_session.add(parameters)

        parameters.progname = "interface"
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

            if substring(parameters.vstring, n - 1, 1) == ";":

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
                    s = ""
                    for k in range(m,(n - 3)  + 1) :

                        if substring(parameters.vstring, k - 1, 1) == "." or substring(parameters.vstring, k - 1, 1) == ",":
                            s = s + ","
                        else:
                            s = s + substring(parameters.vstring, k - 1, 1)
                    cost_list.cost = decimal.Decimal(s)
                    cost_list.cost = cost_list.cost + decimal.Decimal(substring(parameters.vstring, n - 2 - 1, 2)) / 100
                m = n + 1
                i = i + 1


    add_costlist()

    return generate_output()