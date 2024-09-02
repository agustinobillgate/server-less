from functions.additional_functions import *
import decimal
from functions.read_guestbl import read_guestbl
from sqlalchemy import func
from functions.write_guestbl import write_guestbl
from models import Guest, Bediener, Res_history

def change_guesttypebl(gastno:int, new_type:int, user_init:str):
    mess_str = ""
    success_flag:bool = False
    guest = bediener = res_history = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, success_flag, guest, bediener, res_history


        nonlocal t_guest
        nonlocal t_guest_list
        return {"mess_str": mess_str}


    t_guest_list = get_output(read_guestbl(1, gastno, "", ""))

    if new_type != t_guest.karteityp:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "CHG CardType"
        res_history.aenderung = "CHG CardType GuestNo " +\
                to_string(t_guest.gastnr) + " - " + t_guest.name +\
                " " + to_string(t_guest.karteityp) + "->" + to_string(new_type)


        success_flag = get_output(write_guestbl(1, t_guest))
        mess_str = "Cardtype change successfull!"
    else:
        mess_str = "Guest type can not be same type!"

        return generate_output()