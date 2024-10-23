from functions.additional_functions import *
import decimal
from models import Nebenst

def delete_nebenstbl(case_type:int, int1:int):
    successflag = False
    nebenst = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, nebenst
        nonlocal case_type, int1


        return {"successflag": successflag}


    if case_type == 1:

        nebenst = db_session.query(Nebenst).filter(
                 (Nebenst._recid == int1)).first()

        if nebenst:
            db_session.delete(nebenst)
            pass
            successflag = True

    return generate_output()