#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

guest_list_data, Guest_list = create_model("Guest_list", {"guestnumber":int, "guestrefno":string, "guestname":string, "guesttype":string, "address":string, "selected":bool})

def keyaccount_config_addbl(selected_category:int, user_init:string, guest_list_data:[Guest_list]):

    prepare_cache ([Queasy, Bediener, Res_history])

    str_msg = ""
    temp_list_data = []
    nr:int = 1
    category:string = ""
    gname:string = ""
    assigned:string = ""
    queasy = bediener = res_history = None

    guest_list = temp_list = b_queasy = None

    temp_list_data, Temp_list = create_model("Temp_list", {"number1":int, "number2":int, "char1":string, "number3":int, "category":string})

    B_queasy = create_buffer("B_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, temp_list_data, nr, category, gname, assigned, queasy, bediener, res_history
        nonlocal selected_category, user_init
        nonlocal b_queasy


        nonlocal guest_list, temp_list, b_queasy
        nonlocal temp_list_data

        return {"str_msg": str_msg, "temp-list": temp_list_data}

    def add_guest():

        nonlocal str_msg, temp_list_data, nr, category, gname, assigned, queasy, bediener, res_history
        nonlocal selected_category, user_init
        nonlocal b_queasy


        nonlocal guest_list, temp_list, b_queasy
        nonlocal temp_list_data

        b_queasy = get_cache (Queasy, {"key": [(eq, 211)],"number1": [(eq, selected_category)]})

        if b_queasy:
            category = b_queasy.char1

        for guest_list in query(guest_list_data):

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 212) & (Queasy.number1 == selected_category)).order_by(Queasy.number2.desc()).yield_per(100):
                nr = queasy.number2 + 1
                break

            queasy = get_cache (Queasy, {"key": [(eq, 212)],"number3": [(eq, guest_list.guestnumber)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 212
                queasy.number1 = selected_category
                queasy.number2 = nr
                queasy.char1 = guest_list.guestname
                queasy.number3 = guest_list.guestnumber


                gname = queasy.char1

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Assign Guest to KeyAccount, Name: " + gname + " KeyAccount: " + category
                    res_history.action = "Key Account"


                    pass
                    pass

            elif queasy:

                b_queasy = get_cache (Queasy, {"key": [(eq, 211)],"number1": [(eq, queasy.number1)]})

                if b_queasy:
                    str_msg = str_msg + '"' + queasy.char1 + '" has already been assigned to "' + b_queasy.char1 + '"' + chr_unicode(10)
        guest_list_data.clear()
        temp_list_data.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 212)).order_by(Queasy._recid).all():

            b_queasy = get_cache (Queasy, {"key": [(eq, 211)],"number1": [(eq, queasy.number1)]})

            if b_queasy:
                temp_list = Temp_list()
                temp_list_data.append(temp_list)

                temp_list.number1 = queasy.number1
                temp_list.number2 = queasy.number2
                temp_list.char1 = queasy.char1
                temp_list.number3 = queasy.number3

                if queasy.number1 == b_queasy.number1:
                    temp_list.category = b_queasy.char1


    add_guest()

    return generate_output()