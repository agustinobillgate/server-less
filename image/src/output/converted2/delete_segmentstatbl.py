#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Segmentstat

def delete_segmentstatbl(case_type:int, int1:int, int2:int, date1:date):
    success_flag = False
    segmentstat = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, segmentstat
        nonlocal case_type, int1, int2, date1

        return {"success_flag": success_flag}


    if case_type == 1:

        segmentstat = get_cache (Segmentstat, {"segmentcode": [(eq, int1)],"datum": [(eq, date1)]})

        if segmentstat:
            db_session.delete(segmentstat)
            success_flag = True
            pass

    return generate_output()