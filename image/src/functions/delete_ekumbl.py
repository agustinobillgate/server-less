from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Ekum

def delete_ekumbl(case_type:int, int1:int, char1:str):
    success_flag = False
    ekum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, ekum


        return {"success_flag": success_flag}


    if case_type == 1:

        ekum = db_session.query(Ekum).filter(
                (Ekum.eknr == int1) &  (func.lower(Ekum.bezeich) == (char1).lower())).first()

        if ekum:
            db_session.delete(ekum)

            success_flag = True

    return generate_output()