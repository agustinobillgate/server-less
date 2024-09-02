from functions.additional_functions import *
import decimal
from models import Segment

def correct_statistic_disp_segmentbl():
    t_segment_list = []
    segment = None

    t_segment = None

    t_segment_list, T_segment = create_model("T_segment", {"segmentcode":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_list, segment


        nonlocal t_segment
        nonlocal t_segment_list
        return {"t-segment": t_segment_list}

    for segment in db_session.query(Segment).all():
        t_segment = T_segment()
        t_segment_list.append(t_segment)

        t_segmentcode = segmentcode
        t_segment.bezeich = segment.bezeich

    return generate_output()