#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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

        # queasy = get_cache (Queasy, {"key": [(eq, tb1.key)],"char1": [(eq, tb1.char1)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == tb1.key) &
                 (Queasy.char1 == tb1.char1)).with_for_update().first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(tb1, queasy)
        else:
            queasy.char3 = tb1.char3

        # bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, tb1.char1)]})
        bqueasy = db_session.query(Queasy).filter(
                 (Queasy.key == 264) &
                 (Queasy.char1 == tb1.char1)).with_for_update().first()

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