from functions.additional_functions import *
import decimal
from models import Queasy

trate_code_list, Trate_code = create_model_like(Queasy, {"active_flag":bool})

def freeze_ratecodebl(trate_code_list:[Trate_code]):
    queasy = None

    trate_code = bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal bqueasy


        nonlocal trate_code, bqueasy
        nonlocal trate_code_list
        return {}

    for trate_code in query(trate_code_list):

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy.key == 264) & (Bqueasy.char1 == trate_code.char1)).first()

        if not bqueasy and trate_code.active_flag :
            bqueasy = Bqueasy()
            db_session.add(bqueasy)

            bqueasy.key = 264
            bqueasy.char1 = trate_code.char1
            bqueasy.logi1 = trate_code.active_flag

        elif bqueasy:
            bqueasy.logi1 = trate_code.active_flag


            pass

    return generate_output()