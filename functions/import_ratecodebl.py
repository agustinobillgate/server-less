#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

tb1_data, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":string, "freeze":bool})

def import_ratecodebl(tb1_data:[Tb1]):

    prepare_cache ([Queasy])

    queasy = None

    tb1 = bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal tb1_data
        nonlocal bqueasy


        nonlocal tb1, bqueasy

        return {}

    for tb1 in query(tb1_data):

        queasy = get_cache (Queasy, {"key": [(eq, tb1.key)],"char1": [(eq, tb1.char1)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(tb1, queasy)
        else:
            queasy.char3 = tb1.char3

        bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, tb1.char1)]})

        if not bqueasy and tb1.freeze :
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 264
            bqueasy.char1 = tb1.char1
            bqueasy.logi1 = tb1.freeze

        elif bqueasy:
            pass
            bqueasy.logi1 = tb1.freeze


            pass
            pass

    return generate_output()