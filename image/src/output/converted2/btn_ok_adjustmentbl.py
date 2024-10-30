from functions.additional_functions import *
import decimal
from models import Queasy

def btn_ok_adjustmentbl(user_init:str, passwd:str, id_str:str):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal user_init, passwd, id_str

        return {}

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 8
    queasy.date1 = get_current_date()
    queasy.number1 = get_current_time_in_seconds()
    queasy.char1 = user_init

    if passwd.lower()  != (id_str).lower() :
        queasy.char2 = id_str
    pass

    return generate_output()