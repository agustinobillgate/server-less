#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def bk_check_mpbl(blockid:string):
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