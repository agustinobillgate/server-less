from functions.additional_functions import *
import decimal
from models import Bediener

def delete_bedienerbl(case_type:int, int1:int, int2:int, char1:str):
    success_flag = False
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, bediener


        return {"success_flag": success_flag}


    if case_type == 1:

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == int1)).first()

        if bediener:
            db_session.delete(bediener)

            success_flag = True

    return generate_output()