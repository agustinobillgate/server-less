from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def arl_list_add_queue_roombl(roomno:str, user_init:str):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 162) &  (func.lower(Queasy.char1) == (roomno).lower())).first()

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 162
        queasy.char1 = roomno


    queasy.char2 = user_init
    queasy.number1 = 0
    queasy.number2 = get_current_time_in_seconds()
    queasy.date2 = get_current_date()

    queasy = db_session.query(Queasy).first()

    return generate_output()