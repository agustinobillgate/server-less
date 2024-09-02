from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def unlink_ratecodebl(child_code:str, tb1_char3:str):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (child_code).lower())).first()
    queasy.char3 = tb1_char3

    queasy = db_session.query(Queasy).first()

    return generate_output()