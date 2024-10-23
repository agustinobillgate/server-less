from functions.additional_functions import *
import decimal
from datetime import date

def bk_getdatebl(blockid:str):
    startdate = None
    enddate = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal startdate, enddate
        nonlocal blockid


        return {"startdate": startdate, "enddate": enddate}


    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.block_id == blockid)).first()

    if bk_master:
        startdate = bk_master.startdate
        enddate = bk_master.enddate

    return generate_output()