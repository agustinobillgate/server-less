#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_segment

def segment_admin_btn_delartbl(l_segmentcode:int):
    flag = 0
    l_segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_segment
        nonlocal l_segmentcode

        return {"flag": flag}


    l_segment = get_cache (L_segment, {"l_segmentcode": [(eq, l_segmentcode)]})

    if l_segment:
        flag = 1
    else:
        pass

        if l_segment:
            db_session.delete(l_segment)

    return generate_output()