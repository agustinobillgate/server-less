#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================
# Rd, 26/11/2025, with_for_update
#----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def if_ecsys_check_queasybl(fr_date:date, to_date:date, userinit:string, dept:string):

    prepare_cache ([Queasy])

    success_flag = False
    curr_date:date = None
    queasy = None

    db_session = local_storage.db_session
    dept = dept.strip()

    def generate_output():
        nonlocal success_flag, curr_date, queasy
        nonlocal fr_date, to_date, userinit, dept

        return {"success_flag": success_flag}

    success_flag = False


    for curr_date in date_range(fr_date,to_date) :

        # queasy = get_cache (Queasy, {"key": [(eq, 366)],"date1": [(eq, curr_date)]})
        queasy = db_session.query(Queasy).filter(
            (Queasy.key == 366) & (Queasy.date1 == curr_date)).with_for_update().first()

        if queasy:
            pass
            queasy.char1 = userinit
            queasy.char2 = dept
            queasy.logi1 = True
            queasy.logi2 = False


            pass
            pass
            success_flag = True


        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 366
            queasy.date1 = curr_date
            queasy.char1 = userinit
            queasy.char2 = dept
            queasy.logi1 = True
            queasy.logi2 = False


            success_flag = True

    return generate_output()