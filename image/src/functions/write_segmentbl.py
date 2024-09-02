from functions.additional_functions import *
import decimal
from models import Segment

def write_segmentbl(case_type:int, t_segment:[T_segment]):
    success_flag = False
    segment = None

    t_segment = None

    t_segment_list, T_segment = create_model_like(Segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, segment


        nonlocal t_segment
        nonlocal t_segment_list
        return {"success_flag": success_flag}

    t_segment = query(t_segment_list, first=True)

    if not t_segment:

        return generate_output()

    if case_type == 1:
        segment = Segment()
        db_session.add(segment)

        buffer_copy(t_segment, segment)

        success_flag = True
    elif case_type == 2:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == t_Segmentcode)).first()

        if segment:
            buffer_copy(t_segment, segment)

            success_flag = True

    return generate_output()