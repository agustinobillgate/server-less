from functions.additional_functions import *
import decimal
from datetime import date
from models import Segmentstat

def delete_segmentstatbl(case_type:int, int1:int, int2:int, date1:date):
    success_flag = False
    segmentstat = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, segmentstat


        return {"success_flag": success_flag}


    if case_type == 1:

        segmentstat = db_session.query(Segmentstat).filter(
                (Segmentstat.segmentcode == int1) &  (Segmentstat.datum == date1)).first()

        if segmentstat:
            db_session.delete(segmentstat)
            success_flag = True


    return generate_output()