from functions.additional_functions import *
import decimal
from models import Queasy

def update_bookengine_configbl(task:int, becode:int, flag:bool, inp_str:str):
    i:int = 0
    str:str = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, str, queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 160) &  (Queasy.number1 == becode)).first()

    if queasy:
        str = entry(6, char1, ";")

        if num_entries(str, " == ") >= 9:
            str = entry(task - 1, str, "=", to_string(flag))
            char1 = entry(6, char1, ";", str)

        queasy = db_session.query(Queasy).first()

    return generate_output()