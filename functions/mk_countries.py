from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters

def mk_countries():
    lvcarea:str = "mk-countries"
    curr_zone:str = ""
    write_all:bool = False
    city:str = ""
    curr_area:str = ""
    i:int = 0
    parameters = None

    cost_list = zone_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"rec_id":int, "zone":str, "grace":int, "wday":int, "ftime":int, "ttime":int, "tdura":int, "dura":int, "cost":decimal})
    zone_list_list, Zone_list = create_model("Zone_list", {"rec_id":int, "zone":str, "city":str, "acode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, curr_zone, write_all, city, curr_area, i, parameters


        nonlocal cost_list, zone_list
        nonlocal cost_list_list, zone_list_list

        return {}

    def create_costlist():

        nonlocal lvcarea, curr_zone, write_all, city, curr_area, parameters


        nonlocal cost_list, zone_list
        nonlocal cost_list_list, zone_list_list

        i:int = 0
        m:int = 1
        n:int = 0

                for parameters in db_session.query(Parameters).filter(
                         (func.lower(Parameters.progname) == ("Interface").lower()) & (func.lower(Parameters.section) == ("zone").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
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


    def create_zonelist():

        nonlocal lvcarea, curr_zone, write_all, city, curr_area, parameters


        nonlocal cost_list, zone_list
        nonlocal cost_list_list, zone_list_list

        i:int = 0
        m:int = 1
        n:int = 0

                for parameters in db_session.query(Parameters).filter(
                         (func.lower(Parameters.progname) == ("Interface").lower()) & (func.lower(Parameters.section) == ("Dcode").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
                    zone_list = Zone_list()
                    zone_list_list.append(zone_list)

                    zone_list.rec_id = parameters._recid
                    zone_list.zone = parameters.varname
                    i = 1
                    n = 0
                    m = 1
                    while i <= 2:
                        n = n + 1

                        if substring(parameters.vstring, n - 1, 1) == (";").lower() :

                            if i == 1:
                                zone_list.city = substring(parameters.vstring, m - 1, n - m)

                            elif i == 2:
                                zone_list.acode = substring(parameters.vstring, m - 1, n - m)
                            m = n + 1
                            i = i + 1


    create_costlist()
    create_zonelist()
    OUTPUT STREAM s1 TO "\\vhp\\countries.cfg"

    for zone_list in query(zone_list_list, sort_by=[("zone",False)]):

        if curr_zone != zone_list.zone:
            curr_zone = zone_list.zone
            write_all = True

        for cost_list in query(cost_list_list, filters=(lambda cost_list: cost_list.zone == zone_list.zone)):
            city = ""
            for i in range(1,len(zone_list.city)  + 1) :

                if substring(zone_list.city, i - 1, 1) == ("'").lower() :
                    pass

                elif substring(zone_list.city, i - 1, 1) == " " or substring(zone_list.city, i - 1, 1) == (".").lower()  or substring(zone_list.city, i - 1, 1) == (",").lower() :
                    city = city + "-"
                else:
                    city = city + substring(zone_list.city, i - 1, 1)

            if curr_area != zone_list.acode or write_all:

                if write_all:

                    elif curr_area != zone_list.acode:
                        curr_area = zone_list.acode
                write_all = False
            OUTPUT STREAM s1 CLOSE

    return generate_output()