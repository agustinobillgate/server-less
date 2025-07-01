#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def delete_segmentbl(case_type:int, int1:int, char1:string):
    successflag = False
    segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, segment
        nonlocal case_type, int1, char1

        return {"successflag": successflag}


    if case_type == 1:

        segment = get_cache (Segment, {"segmentcode": [(eq, int1)]})

        if segment:
            db_session.delete(segment)
            pass
            successflag = True

    return generate_output()