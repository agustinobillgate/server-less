#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

updq_data, Updq = create_model("Updq", {"ratecode":string, "vhprates":Decimal, "berates":Decimal, "datum":date, "user_init":string, "sysdate":date, "systime":int})

def bookengine_pushrate_storebl(booken_selected:int, updq_data:[Updq], mode:int):
    prevrates:Decimal = to_decimal("0.0")
    queasy = None

    updq = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal prevrates, queasy
        nonlocal booken_selected, mode


        nonlocal updq

        return {}

    if mode == 1:

        for updq in query(updq_data):

            queasy = get_cache (Queasy, {"key": [(eq, 201)],"number1": [(eq, 5)],"date1": [(eq, updq.datum)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 201
                queasy.number1 = 5
                queasy.number2 = booken_selected
                queasy.number3 = updq.systime
                queasy.char1 = updq.ratecode
                queasy.char2 = updq.user_init
                queasy.deci1 =  to_decimal(updq.vhprates)
                queasy.date1 = updq.datum
                queasy.date2 = updq.sysdate
                queasy.deci2 =  to_decimal("0")
                queasy.deci3 =  to_decimal(updq.vhprates)


            else:
                prevrates =  to_decimal(queasy.deci3)
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 201
                queasy.number1 = 5
                queasy.number2 = booken_selected
                queasy.number3 = updq.systime
                queasy.char1 = updq.ratecode
                queasy.char2 = updq.user_init
                queasy.deci1 =  to_decimal(updq.vhprates)
                queasy.date1 = updq.datum
                queasy.date2 = updq.sysdate
                queasy.deci2 =  to_decimal(prevrates)
                queasy.deci3 =  to_decimal(updq.berates)

        for updq in query(updq_data):

            # queasy = get_cache (Queasy, {"key": [(eq, 201)],"number1": [(eq, 6)],"date1": [(eq, updq.datum)],"char1": [(eq, updq.ratecode)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 201) &
                     (Queasy.number1 == 6) &
                     (Queasy.number2 == booken_selected) &
                     (Queasy.date1 == updq.datum) &
                     (Queasy.char1 == updq.ratecode)).with_for_update().first()

            if queasy:
                db_session.delete(queasy)
                pass

        for updq in query(updq_data):
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 201
            queasy.number1 = 6
            queasy.number2 = booken_selected
            queasy.number3 = updq.systime
            queasy.char1 = updq.ratecode
            queasy.char2 = updq.user_init
            queasy.deci1 =  to_decimal(updq.vhprates)
            queasy.date1 = updq.datum
            queasy.date2 = updq.sysdate
            queasy.deci2 =  to_decimal("0")
            queasy.deci3 =  to_decimal(updq.berates)

    elif mode == 2:

        for updq in query(updq_data):

            # queasy = get_cache (Queasy, {"key": [(eq, 201)],"number1": [(eq, 6)],"number2": [(eq, booken_selected)],"date1": [(eq, updq.datum)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 201) &
                     (Queasy.number1 == 6) &
                     (Queasy.number2 == booken_selected) &
                     (Queasy.date1 == updq.datum)).with_for_update().first()

            if queasy:
                db_session.delete(queasy)
                pass

    return generate_output()