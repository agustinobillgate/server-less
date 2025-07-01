#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters

def prepare_if_country1bl(fl_run_proc:bool):
    cost_list_list = []
    zone_list_list = []
    t_parameters_list = []
    parameters = None

    t_parameters = cost_list = zone_list = None

    t_parameters_list, T_parameters = create_model_like(Parameters, {"rec_id":int})
    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "zone":string, "grace":int, "wday":int, "ftime":int, "ttime":int, "tdura":int, "dura":int, "cost":Decimal, "info":string})
    zone_list_list, Zone_list = create_model("Zone_list", {"rec_id":int, "zone":string, "city":string, "acode":string, "info":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, zone_list_list, t_parameters_list, parameters
        nonlocal fl_run_proc


        nonlocal t_parameters, cost_list, zone_list
        nonlocal t_parameters_list, cost_list_list, zone_list_list

        return {"cost-list": cost_list_list, "zone-list": zone_list_list, "t-parameters": t_parameters_list}

    def cleanup_zonelist():

        nonlocal cost_list_list, zone_list_list, t_parameters_list, parameters
        nonlocal fl_run_proc


        nonlocal t_parameters, cost_list, zone_list
        nonlocal t_parameters_list, cost_list_list, zone_list_list

        parameters = get_cache (Parameters, {"progname": [(eq, "if-internal")],"section": [(eq, "dcode")],"varname": [(gt, "")]})

        if parameters:

            for parameters in db_session.query(Parameters).filter(
                     (Parameters.progname == ("if-internal").lower()) & (Parameters.section == ("Dcode").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
                db_session.delete(parameters)

    def create_costlist():

        nonlocal cost_list_list, zone_list_list, t_parameters_list, parameters
        nonlocal fl_run_proc


        nonlocal t_parameters, cost_list, zone_list
        nonlocal t_parameters_list, cost_list_list, zone_list_list

        i:int = 0
        m:int = 1
        n:int = 0
        s:string = ""
        k:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("if-internal").lower()) & (Parameters.section == ("zone").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.rec_id = parameters._recid
            cost_list.zone = parameters.varname
            i = 1
            n = 0
            m = 1
            while i <= 8 and n < length(parameters.vstring) :
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

                        if substring(parameters.vstring, n - 3 - 1, 1) == (".").lower()  or substring(parameters.vstring, n - 3 - 1, 1) == (",").lower() :
                            cost_list.cost = to_decimal(substring(parameters.vstring, m - 1, n - m - 3))
                            cost_list.cost = cost_list.cost + to_decimal(substring(parameters.vstring, n - 2 - 1, 2)) / 100
                        else:
                            cost_list.cost = to_decimal(substring(parameters.vstring, m - 1, n - m - 2))
                            cost_list.cost = cost_list.cost + to_decimal(substring(parameters.vstring, n - 2 - 1, 2)) / 100

                    elif i == 8:
                        cost_list.info = substring(parameters.vstring, m - 1, n - m)
                    m = n + 1
                    i = i + 1


    def create_zonelist():

        nonlocal cost_list_list, zone_list_list, t_parameters_list, parameters
        nonlocal fl_run_proc


        nonlocal t_parameters, cost_list, zone_list
        nonlocal t_parameters_list, cost_list_list, zone_list_list

        i:int = 0
        m:int = 1
        n:int = 0
        ifname:string = "if-internal"

        if substring(proversion(), 0, 1) >= ("9").lower()  or substring(proversion(), 0, 1) == ("1").lower() :
            ifname = "interface"

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == (ifname).lower()) & (Parameters.section == ("Dcode").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            zone_list = Zone_list()
            zone_list_list.append(zone_list)

            zone_list.rec_id = parameters._recid
            zone_list.zone = parameters.varname
            i = 1
            n = 0
            m = 1
            while i <= 3 and n < length(parameters.vstring) :
                n = n + 1

                if substring(parameters.vstring, n - 1, 1) == (";").lower() :

                    if i == 1:
                        zone_list.city = substring(parameters.vstring, m - 1, n - m)

                    elif i == 2:
                        zone_list.acode = substring(parameters.vstring, m - 1, n - m)

                    elif i == 3:
                        zone_list.info = substring(parameters.vstring, m - 1, n - m)
                    m = n + 1
                    i = i + 1


    if fl_run_proc:
        cleanup_zonelist()
    create_costlist()
    create_zonelist()

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("interface").lower()) & (Parameters.section == ("zone").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        buffer_copy(parameters, t_parameters)
        t_parameters.rec_id = parameters._recid

    return generate_output()