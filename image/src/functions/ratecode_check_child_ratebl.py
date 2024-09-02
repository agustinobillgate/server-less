from functions.additional_functions import *
import decimal
from models import Queasy

def ratecode_check_child_ratebl(case_type:int, inpchar1:str):
    child_rate = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal child_rate, queasy


        return {"child_rate": child_rate}


    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2)).first()
        while None != queasy:

            if queasy.char3 != "":

                if entry(1, queasy.char3, ";") == inpchar1:
                    child_rate = True


                    break

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2)).first()

    return generate_output()