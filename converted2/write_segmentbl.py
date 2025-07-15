#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

t_segment_data, T_segment = create_model_like(Segment)

def write_segmentbl(case_type:int, t_segment_data:[T_segment]):
    success_flag = False
    segment = None

    t_segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, segment
        nonlocal case_type


        nonlocal t_segment

        return {"success_flag": success_flag}

    t_segment = query(t_segment_data, first=True)

    if not t_segment:

        return generate_output()

    if case_type == 1:
        segment = Segment()
        db_session.add(segment)

        buffer_copy(t_segment, segment)
        pass
        success_flag = True
    elif case_type == 2:

        segment = get_cache (Segment, {"segmentcode": [(eq, t_segment.segmentcode)]})

        if segment:
            buffer_copy(t_segment, segment)
            pass
            success_flag = True

    return generate_output()