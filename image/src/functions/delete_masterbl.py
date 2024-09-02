from functions.additional_functions import *
import decimal
from models import Master, Mast_art

def delete_masterbl(case_type:int, int1:int):
    success_flag = False
    master = mast_art = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master, mast_art


        return {"success_flag": success_flag}


    if case_type == 1:

        master = db_session.query(Master).filter(
                (Master.resnr == int1)).first()

        if master:
            db_session.delete(master)

    elif case_type == 2:

        master = db_session.query(Master).filter(
                (Master.resnr == int1)).first()

        if master:
            db_session.delete(master)


        for mast_art in db_session.query(Mast_art).filter(
                (Mast_art.resnr == int1)).all():
            db_session.delete(mast_art)


    return generate_output()