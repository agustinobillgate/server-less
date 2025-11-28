#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

maingrp_list_data, Maingrp_list = create_model_like(Queasy)

def write_selforder_maingrup_adminbl(case_type:int, maingrp_list_data:[Maingrp_list]):

    prepare_cache ([Queasy])

    success_flag = False
    queasy = None

    maingrp_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy
        nonlocal case_type


        nonlocal maingrp_list

        return {"success_flag": success_flag}

    maingrp_list = query(maingrp_list_data, first=True)

    if not maingrp_list:

        return generate_output()

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(maingrp_list, queasy)
        pass
        success_flag = True
    elif case_type == 2:

        # queasy = get_cache (Queasy, {"key": [(eq, 228)],"number1": [(eq, maingrp_list.number1)]})
        queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 228) &
                        (Queasy.number1 == maingrp_list.number1)
                    ).with_for_update().first()

        if queasy:
            pass
            queasy.char1 = maingrp_list.char1
            queasy.char2 = maingrp_list.char2
            queasy.number2 = maingrp_list.number2
            pass
            pass
            success_flag = True

    return generate_output()