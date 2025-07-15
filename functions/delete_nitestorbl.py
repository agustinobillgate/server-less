#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nitestor

def delete_nitestorbl(case_type:int, int1:int, int2:int):
    success_flag = False
    nitestor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nitestor
        nonlocal case_type, int1, int2

        return {"success_flag": success_flag}


    if case_type == 1:

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == int1) & (Nitestor.reihenfolge == int2)).order_by(Nitestor._recid).all():
            db_session.delete(nitestor)
            pass
            success_flag = True

    return generate_output()