from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Telephone

def delete_telephonebl(case_type:int, int1:int, char1:str, char2:str):
    success_flag = False
    telephone = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, telephone
        return {"success_flag": success_flag}

    if case_type == 1:
        telephone = db_session.query(Telephone).filter(
                # (func.lower(Telephone.telephone) == (char1).lower()) &
                (func.lower(Telephone.name) == (char2).lower())
            ).first()

        if telephone:
            db_session.delete(telephone)

            success_flag = True

    return generate_output()