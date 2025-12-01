#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Master, Mast_art

def delete_masterbl(case_type:int, int1:int):
    success_flag = False
    master = mast_art = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master, mast_art
        nonlocal case_type, int1

        return {"success_flag": success_flag}


    if case_type == 1:
        master = db_session.query(Master).filter(Master.resnr == int1).with_for_update().first()

        if master:
            db_session.delete(master)
    elif case_type == 2:
        master = db_session.query(Master).filter(Master.resnr == int1).with_for_update().first()

        if master:
            db_session.delete(master)

        for mast_art in db_session.query(Mast_art).filter(
            Mast_art.resnr == int1).with_for_update().order_by(Mast_art._recid).all():
            db_session.delete(mast_art)

    return generate_output()