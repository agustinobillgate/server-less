#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def pos_dashboard_sound_linkbl(sound_link:string):

    prepare_cache ([Queasy])

    v_success = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, queasy
        nonlocal sound_link

        return {"v_success": v_success}


    queasy = get_cache (Queasy, {"key": [(eq, 299)],"number1": [(eq, 1)],"char1": [(eq, "selforder-sound")]})

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 299
        queasy.number1 = 1
        queasy.char1 = "SelfOrder-Sound"
        queasy.char2 = sound_link


    else:
        queasy.char2 = sound_link
    pass
    pass
    v_success = True

    return generate_output()