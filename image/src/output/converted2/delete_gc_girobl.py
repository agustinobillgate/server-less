from functions.additional_functions import *
import decimal
from models import Gc_giro

def delete_gc_girobl(case_type:int, int1:int):
    successflag = False
    gc_giro = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gc_giro
        nonlocal case_type, int1


        return {"successflag": successflag}


    if case_type == 1:

        gc_giro = db_session.query(Gc_giro).filter(
                 (Gc_giro._recid == int1)).first()

        if gc_giro:
            db_session.delete(gc_giro)
            successflag = True

    return generate_output()