#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def tbplan_setup_btn_go_webbl(curr_mode:string, location:int, from_table:int, location2:int):
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy
        nonlocal curr_mode, location, from_table, location2


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    if curr_mode.lower()  == ("add").lower() :
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 31
        queasy.number1 = location
        queasy.number2 = from_table
        queasy.deci3 =  to_decimal(location2)


        pass
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    elif curr_mode.lower()  == ("move").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, location)],"number2": [(eq, from_table)],"betriebsnr": [(eq, 0)],"deci3": [(eq, location2)]})
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()