#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

trate_code_list, Trate_code = create_model_like(Queasy, {"active_flag":bool})

def freeze_ratecodebl(trate_code_list:[Trate_code]):

    prepare_cache ([Queasy])

    queasy = None

    trate_code = bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal bqueasy


        nonlocal trate_code, bqueasy

        return {}

    for trate_code in query(trate_code_list):

        bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, trate_code.char1)]})

        if not bqueasy and trate_code.active_flag :
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 264
            bqueasy.char1 = trate_code.char1
            bqueasy.logi1 = trate_code.active_flag

        elif bqueasy:
            pass
            bqueasy.logi1 = trate_code.active_flag


            pass
            pass

    return generate_output()