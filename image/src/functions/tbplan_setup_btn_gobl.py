from functions.additional_functions import *
import decimal
from models import Queasy

def tbplan_setup_btn_gobl(curr_mode:str, location:int, from_table:int):
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    if curr_mode.lower()  == "add":
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 31
        queasy.number1 = location
        queasy.number2 = from_table

        queasy = db_session.query(Queasy).first()
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    elif curr_mode.lower()  == "move":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 31) &  (Queasy.number1 == location) &  (Queasy.number2 == from_table) &  (Queasy.betriebsnr == 0)).first()
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()