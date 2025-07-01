#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_freeze_ratecodebl():

    prepare_cache ([Queasy])

    trate_code_list = []
    queasy = None

    trate_code = bqueasy = None

    trate_code_list, Trate_code = create_model_like(Queasy, {"active_flag":bool})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal trate_code_list, queasy
        nonlocal bqueasy


        nonlocal trate_code, bqueasy
        nonlocal trate_code_list

        return {"trate-code": trate_code_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.logi2 == False)).order_by(Queasy._recid).all():
        trate_code = Trate_code()
        trate_code_list.append(trate_code)

        buffer_copy(queasy, trate_code)

        bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, queasy.char1)]})

        if bqueasy:
            trate_code.active_flag = bqueasy.logi1

    return generate_output()