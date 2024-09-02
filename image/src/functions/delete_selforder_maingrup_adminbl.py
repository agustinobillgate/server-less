from functions.additional_functions import *
import decimal
from models import Queasy

def delete_selforder_maingrup_adminbl(maingrp_number1:int):
    int_flag = 0
    success_flag = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal int_flag, success_flag, queasy


        return {"int_flag": int_flag, "success_flag": success_flag}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 228) &  (Queasy.number1 == maingrp_number1)).first()

    if queasy:
        db_session.delete(queasy)

        success_flag = True

    return generate_output()