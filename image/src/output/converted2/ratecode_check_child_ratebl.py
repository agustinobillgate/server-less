#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ratecode_check_child_ratebl(case_type:int, inpchar1:string):
    child_rate = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal child_rate, queasy
        nonlocal case_type, inpchar1

        return {"child_rate": child_rate}


    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 2)]})
        while None != queasy:

            if queasy.char3 != "":

                if entry(1, queasy.char3, ";") == inpchar1:
                    child_rate = True


                    break

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy._recid > curr_recid)).first()

    return generate_output()