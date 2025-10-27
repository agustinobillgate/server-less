#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 27/10/2025
#--------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.read_guestbl import read_guestbl
from functions.write_guestbl import write_guestbl
from models import Guest, Bediener, Res_history

def change_guesttypebl(gastno:int, new_type:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    mess_str = ""
    success_flag:bool = False
    guest = bediener = res_history = None

    t_guest = None

    t_guest_data, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, success_flag, guest, bediener, res_history
        nonlocal gastno, new_type, user_init


        nonlocal t_guest
        nonlocal t_guest_data

        return {"mess_str": mess_str}


    t_guest_data = get_output(read_guestbl(1, gastno, "", ""))

    # t_guest = query(t_guest_data, filters=(lambda t_guest: t_guest.gastnr == gastno), first=True)
    t_guest = db_session.query(Guest).filter(Guest.gastnr == gastno).first()

    if t_guest:

        if new_type != t_guest.karteityp:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "CHG CardType"
            res_history.aenderung = "CHG CardType GuestNo " +\
                    to_string(t_guest.gastnr) + " - " + t_guest.name +\
                    " " + to_string(t_guest.karteityp) + "->" + to_string(new_type)


            success_flag = get_output(write_guestbl(1, t_guest_data))
            mess_str = "Cardtype change successfull!"

            return generate_output()
        else:
            mess_str = "Guest type can not be same type!"

            return generate_output()
    else:
        mess_str = "Guest Does not exist"

        return generate_output()

    return generate_output()