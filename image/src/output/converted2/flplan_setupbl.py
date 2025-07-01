#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def flplan_setupbl(curr_mode:string, location:int, floor:int, from_room:string):
    t_queasy1_list = []
    queasy = None

    t_queasy1 = None

    t_queasy1_list, T_queasy1 = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy1_list, queasy
        nonlocal curr_mode, location, floor, from_room


        nonlocal t_queasy1
        nonlocal t_queasy1_list

        return {"t-queasy1": t_queasy1_list}

    if curr_mode.lower()  == ("add").lower() :
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 25
        queasy.number1 = location
        queasy.number2 = floor
        queasy.char1 = from_room


        pass
        t_queasy1 = T_queasy1()
        t_queasy1_list.append(t_queasy1)

        buffer_copy(queasy, t_queasy1)
        t_queasy1.rec_id = queasy._recid

    elif curr_mode.lower()  == ("move").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 25)],"number1": [(eq, location)],"number2": [(eq, floor)],"char1": [(eq, from_room)]})
        pass
        t_queasy1 = T_queasy1()
        t_queasy1_list.append(t_queasy1)

        buffer_copy(queasy, t_queasy1)
        t_queasy1.rec_id = queasy._recid

    return generate_output()