from functions.additional_functions import *
import decimal
from models import Queasy

def write_selforder_maingrup_adminbl(case_type:int, maingrp_list:[Maingrp_list]):
    success_flag = False
    queasy = None

    maingrp_list = None

    maingrp_list_list, Maingrp_list = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        nonlocal maingrp_list
        nonlocal maingrp_list_list
        return {"success_flag": success_flag}

    maingrp_list = query(maingrp_list_list, first=True)

    if not maingrp_list:

        return generate_output()

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(maingrp_list, queasy)

        success_flag = True
    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 228) &  (Queasy.number1 == maingrp_list.number1)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.char1 = maingrp_list.char1
            queasy.char2 = maingrp_list.char2
            queasy.number2 = maingrp_list.number2

            queasy = db_session.query(Queasy).first()

            success_flag = True

    return generate_output()