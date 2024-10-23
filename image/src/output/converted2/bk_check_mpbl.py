from functions.additional_functions import *
import decimal

def bk_check_mpbl(blockid:str):
    availflag = False


    db_session = local_storage.db_session

    def generate_output():
        nonlocal availflag
        nonlocal blockid


        return {"availflag": availflag}


    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.block_id == blockid)).first()

    if bk_master:
        availflag = True

    return generate_output()