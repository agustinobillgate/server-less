from functions.additional_functions import *
import decimal
from models import Queasy

def eg_action_maintaskbl(maintask:int):
    do_it = False
    char1 = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, char1, queasy


        return {"do_it": do_it, "char1": char1}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 133) &  (Queasy.number1 == maintask)).first()

    if not queasy:
        do_it = True
    else:
        char1 = queasy.char1

    return generate_output()