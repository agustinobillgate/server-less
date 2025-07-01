#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def arl_list_add_queue_roombl(roomno:string, user_init:string):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal roomno, user_init

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 162)],"char1": [(eq, roomno)]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 162
        queasy.char1 = roomno


    queasy.char2 = user_init
    queasy.number1 = 0
    queasy.number2 = get_current_time_in_seconds()
    queasy.date2 = get_current_date()


    pass

    return generate_output()