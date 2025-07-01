#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def correct_statistic_disp_segmentbl():

    prepare_cache ([Segment])

    t_segment_list = []
    segment = None

    t_segment = None

    t_segment_list, T_segment = create_model("T_segment", {"segmentcode":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_list, segment


        nonlocal t_segment
        nonlocal t_segment_list

        return {"t-segment": t_segment_list}

    for segment in db_session.query(Segment).order_by(Segment._recid).all():
        t_segment = T_segment()
        t_segment_list.append(t_segment)

        t_segment.segmentcode = segment.segmentcode
        t_segment.bezeich = segment.bezeich

    return generate_output()