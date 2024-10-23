from functions.additional_functions import *
import decimal
from models import Fixleist

def delete_fixleistbl(case_type:int, int1:int):
    succesflag = False
    fixleist = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal succesflag, fixleist
        nonlocal case_type, int1


        return {"succesflag": succesflag}


    if case_type == 1:

        fixleist = db_session.query(Fixleist).filter(
                 (Fixleist._recid == int1)).first()

        if fixleist:
            db_session.delete(fixleist)
            pass
            succesflag = True

    return generate_output()