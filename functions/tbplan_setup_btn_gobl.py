#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def tbplan_setup_btn_gobl(curr_mode:string, location:int, from_table:int):
    t_queasy_data = []
    queasy = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, queasy
        nonlocal curr_mode, location, from_table


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    if curr_mode.lower()  == ("add").lower() :
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 31
        queasy.number1 = location
        queasy.number2 = from_table


        pass
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    elif curr_mode.lower()  == ("move").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, location)],"number2": [(eq, from_table)],"betriebsnr": [(eq, 0)]})
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()