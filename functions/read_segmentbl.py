#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def read_segmentbl(case_type:int, segmentno:int, segmname:string):
    t_segment_data = []
    segment = None

    t_segment = None

    t_segment_data, T_segment = create_model_like(Segment)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_data, segment
        nonlocal case_type, segmentno, segmname


        nonlocal t_segment
        nonlocal t_segment_data

        return {"t-segment": t_segment_data}

    if case_type == 1:

        segment = get_cache (Segment, {"segmentcode": [(eq, segmentno)]})

        if segment:
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)
    elif case_type == 2:

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr <= 2) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.betriebsnr, Segment.segmentcode).all():
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)

    elif case_type == 3:

        segment = db_session.query(Segment).filter(
                 (entry(0, Segment.bezeich, "$$0") == segmname)).first()

        if segment:
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)
    elif case_type == 4:

        segment = get_cache (Segment, {"betriebsnr": [(eq, 0)]})

        if segment:
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)
    elif case_type == 5:

        for segment in db_session.query(Segment).filter(
                 (Segment.segmentcode != segmentno) & (Segment.segmentgrup != 0)).order_by(Segment._recid).all():
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)
    elif case_type == 6:

        for segment in db_session.query(Segment).filter(
                 (Segment.vip_level == 0) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.betriebsnr, Segment.segmentcode).all():
            t_segment = T_segment()
            t_segment_data.append(t_segment)

            buffer_copy(segment, t_segment)


    return generate_output()