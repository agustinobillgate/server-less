from functions.additional_functions import *
import decimal
from models import Interface, Nebenst, Zimmer, Res_history

t_interface1_list, T_interface1 = create_model_like(Interface)
t_interface2_list, T_interface2 = create_model_like(Interface)

def write_interfacebl(case_type:int, t_interface1_list:[T_interface1], t_interface2_list:[T_interface2]):
    successflag = False
    user_init:str = ""
    interface = nebenst = zimmer = res_history = None

    t_interface1 = t_interface2 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, user_init, interface, nebenst, zimmer, res_history

        nonlocal t_interface1, t_interface2
        global t_interface1_list, t_interface2_list
        db_session.commit()
        return {"successflag": successflag}

    if case_type == 1:
        local_storage.debugging = local_storage.debugging + ",1:30"
        t_interface1 = query(t_interface1_list, first=True)

        if t_interface1:
            interface = Interface()
            db_session.add(interface)

            buffer_copy(t_interface1, interface)

            successflag = True
    elif case_type == 2:
        local_storage.debugging = local_storage.debugging + ",2:41"
        t_interface2 = query(t_interface2_list, first=True)

        interface = db_session.query(Interface).filter(
                (Interface.key == t_interface2.key) &  (Interface.zinr == t_interface2.zinr) &  (Interface.nebenstelle == t_interface2.nebenstelle) &  (Interface.action == t_interface2.action) &  (Interface.parameters == t_interface2.parameters) &  (Interface.intfield == t_interface2.intfield) &  (Interface.decfield == t_interface2.decfield) &  (Interface.intdate == t_interface2.intdate) &  (Interface.int_time == t_interface2.int_time) &  (Interface.betriebsnr == t_interface2.betriebsnr) &  (Interface.resnr == t_interface2.resnr) &  (Interface.reslinnr == t_interface2.reslinnr) &  (Interface.zinr_old == t_interface2.zinr_old)).first()

        if interface:
            buffer_copy(t_interface1, interface)

            interface = db_session.query(Interface).first()

            successflag = True
    elif case_type == 3:
        local_storage.debugging = local_storage.debugging + ",3:54"
        interface = db_session.query(Interface).filter(
                (Interface.key == 17)).first()

        if interface:

            return generate_output()
        interface = Interface()
        db_session.add(interface)

        interface.key = 17
        interface.intdate = get_current_date()
        interface.int_time = get_current_time_in_seconds()

        interface = db_session.query(Interface).first()

    elif case_type == 4:
        local_storage.debugging = local_storage.debugging + ",71"

        for t_interface1 in query(t_interface1_list):
            print("69", t_interface1)
            interface = Interface()
            db_session.add(interface)

            buffer_copy(t_interface1, interface)
            user_init = entry(1, interface.parameters, ";")
            interface.parameters = entry(0, interface.parameters, ";")
            local_storage.debugging = local_storage.debugging + "."+ interface.parameters
            if interface.nebenstelle.strip() == "":
                nebenst = db_session.query(Nebenst).filter(
                        (Nebenst.zinr == interface.zinr) &  (Nebenst.nebst_type == 0)).first()

                if nebenst:
                    interface.nebenstelle = nebenst.nebenstelle
                else:
                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == interface.zinr)).first()

                    if zimmer:
                        interface.nebenstelle = zimmer.nebenstelle
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = to_int(user_init)
                res_history.resnr = interface.resnr
                res_history.reslinnr = interface.reslinnr
                # tgl 4 digit : 2024/07/10
                res_history.datum = get_date_input(interface.intdate)
                res_history.zeit = interface.int_time
                res_history.action = "Wake Up Call"

                if interface.parameters.lower()  == "Wakeup Calls OFF".lower():
                    res_history.aenderung = "Cancel Wake Up Call;"
                else:
                    res_history.aenderung = "Set Wake Up Call;"
                res_history.aenderung = res_history.aenderung + " RmNo: " + interface.zinr + ";" + " TIME: " + to_string(interface.intfield, "HH:MM") + ";"

                if user_init != "":
                    res_history.aenderung = res_history.aenderung + "UID :" + user_init + ";"

    return generate_output()