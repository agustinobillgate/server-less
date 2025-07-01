#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def bk_getdatebl(blockid:string):
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