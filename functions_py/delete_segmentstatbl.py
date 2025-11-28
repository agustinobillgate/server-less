#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
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

        # segmentstat = get_cache (Segmentstat, {"segmentcode": [(eq, int1)],"datum": [(eq, date1)]})
        segmentstat = db_session.query(Segmentstat).filter(
                            (Segmentstat.segmentcode == int1) &
                            (Segmentstat.datum == date1)
                        ).with_for_update().first()

        if segmentstat:
            db_session.delete(segmentstat)
            success_flag = True
            pass

    return generate_output()