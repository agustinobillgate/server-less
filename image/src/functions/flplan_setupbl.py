from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def flplan_setupbl(curr_mode:str, location:int, floor:int, from_room:str):
    t_queasy1_list = []
    queasy = None

    t_queasy1 = None

    t_queasy1_list, T_queasy1 = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy1_list, queasy


        nonlocal t_queasy1
        nonlocal t_queasy1_list
        return {"t-queasy1": t_queasy1_list}

    if curr_mode.lower()  == "add":
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 25
        queasy.number1 = location
        queasy.number2 = floor
        queasy.char1 = from_room

        queasy = db_session.query(Queasy).first()
        t_queasy1 = T_queasy1()
        t_queasy1_list.append(t_queasy1)

        buffer_copy(queasy, t_queasy1)
        t_queasy1.rec_id = queasy._recid

    elif curr_mode.lower()  == "move":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 25) &  (Queasy.number1 == location) &  (Queasy.number2 == floor) &  (func.lower(Queasy.char1) == (from_room).lower())).first()

        queasy = db_session.query(Queasy).first()
        t_queasy1 = T_queasy1()
        t_queasy1_list.append(t_queasy1)

        buffer_copy(queasy, t_queasy1)
        t_queasy1.rec_id = queasy._recid

    return generate_output()