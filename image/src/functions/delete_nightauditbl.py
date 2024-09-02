from functions.additional_functions import *
import decimal
from models import Nightaudit

def delete_nightauditbl(case_type:int, int1:int):
    successflag = False
    nightaudit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, nightaudit


        return {"successflag": successflag}


    if case_type == 1:

        nightaudit = db_session.query(Nightaudit).filter(
                (Nightaudit._recid == int1)).first()

        if nightaudit:
            db_session.delete(nightaudit)

            successflag = True

    return generate_output()