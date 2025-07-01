#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Interface, Nebenst, Zimmer, Bediener, Res_history

t_interface1_list, T_interface1 = create_model_like(Interface)
t_interface2_list, T_interface2 = create_model_like(Interface)

def write_interfacebl(case_type:int, t_interface1_list:[T_interface1], t_interface2_list:[T_interface2]):

    prepare_cache ([Interface, Nebenst, Zimmer, Bediener, Res_history])

    successflag = False
    bediener_nr:int = 0
    user_init:string = ""
    interface = nebenst = zimmer = bediener = res_history = None

    t_interface1 = t_interface2 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, bediener_nr, user_init, interface, nebenst, zimmer, bediener, res_history
        nonlocal case_type, t_interface1_list, t_interface2_list


        nonlocal t_interface1, t_interface2

        return {"successflag": successflag}


    if case_type == 1:

        t_interface1 = query(t_interface1_list, first=True)

        if t_interface1:
            interface = Interface()
            db_session.add(interface)

            buffer_copy(t_interface1, interface)
            pass
            successflag = True
    elif case_type == 2:

        t_interface2 = query(t_interface2_list, first=True)

        interface = get_cache (Interface, {"key": [(eq, t_interface2.key)],"zinr": [(eq, t_interface2.zinr)],"nebenstelle": [(eq, t_interface2.nebenstelle)],"action": [(eq, t_interface2.action)],"parameters": [(eq, t_interface2.parameters)],"intfield": [(eq, t_interface2.intfield)],"decfield": [(eq, t_interface2.decfield)],"intdate": [(eq, t_interface2.intdate)],"int_time": [(eq, t_interface2.int_time)],"betriebsnr": [(eq, t_interface2.betriebsnr)],"resnr": [(eq, t_interface2.resnr)],"reslinnr": [(eq, t_interface2.reslinnr)],"zinr_old": [(eq, t_interface2.zinr_old)]})

        if interface:
            buffer_copy(t_interface1, interface)
            pass
            pass
            successflag = True
    elif case_type == 3:

        interface = get_cache (Interface, {"key": [(eq, 17)]})

        if interface:

            return generate_output()
        interface = Interface()
        db_session.add(interface)

        interface.key = 17
        interface.intdate = get_current_date()
        interface.int_time = get_current_time_in_seconds()


        pass
        pass
    elif case_type == 4:

        for t_interface1 in query(t_interface1_list):
            interface = Interface()
            db_session.add(interface)

            buffer_copy(t_interface1, interface)
            user_init = entry(1, interface.parameters, ";")
            interface.parameters = entry(0, interface.parameters, ";")

            if interface.nebenstelle == "":

                nebenst = get_cache (Nebenst, {"zinr": [(eq, interface.zinr)],"nebst_type": [(eq, 0)]})

                if nebenst:
                    interface.nebenstelle = nebenst.nebenstelle
                else:

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, interface.zinr)]})

                    if zimmer:
                        interface.nebenstelle = zimmer.nebenstelle

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    bediener_nr = bediener.nr
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener_nr
                res_history.resnr = interface.resnr
                res_history.reslinnr = interface.reslinnr
                res_history.datum = interface.intdate
                res_history.zeit = interface.int_time
                res_history.action = "Wake Up Call"

                if interface.parameters.lower()  == ("Wakeup Calls OFF").lower() :
                    res_history.aenderung = "Cancel Wake Up Call;"
                else:
                    res_history.aenderung = "Set Wake Up Call;"
                res_history.aenderung = res_history.aenderung + " RmNo: " + interface.zinr + ";" + " TIME: " + to_string(interface.intfield, "HH:MM") + ";"

                if user_init != "":
                    res_history.aenderung = res_history.aenderung + "UID :" + user_init + ";"

    return generate_output()