#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_keyaccount_configbl():

    prepare_cache ([Queasy])

    t_queasy_data = []
    temp_list_data = []
    queasy = None

    t_queasy = temp_list = b_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)
    temp_list_data, Temp_list = create_model("Temp_list", {"number1":int, "number2":int, "char1":string, "number3":int, "category":string})

    B_queasy = create_buffer("B_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, temp_list_data, queasy
        nonlocal b_queasy


        nonlocal t_queasy, temp_list, b_queasy
        nonlocal t_queasy_data, temp_list_data

        return {"t-queasy": t_queasy_data, "temp-list": temp_list_data}

    t_queasy_data.clear()
    temp_list_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 211)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

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

    return generate_output()