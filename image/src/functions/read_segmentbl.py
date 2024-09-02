from functions.additional_functions import *
import decimal, traceback
from models import Segment

def read_segmentbl(case_type:int, segmentno:int, segmname:str):
    t_segment_list = []
    segment = None

    t_segment = None

    t_segment_list, T_segment = create_model_like(Segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_list, segment


        nonlocal t_segment
        nonlocal t_segment_list
        return {"t-segment": t_segment_list}

    try:
        if case_type == 1:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == segmentno)).first()

            if segment:
                t_segment = T_segment()
                t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)
        elif case_type == 2:

            for segment in db_session.query(Segment).filter(
                    (Segment.betriebsnr <= 2) 
                    # & (num_entries(Segment.bezeich, "$$0") == 1)
                ).all():
                if num_entries(segment.bezeich, "$$0") == 1:
                    t_segment = T_segment()
                    t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)

        elif case_type == 3:

            segment = db_session.query(Segment).filter(
                    (entry(0, Segment.bezeich, "$$0") == segmname)).first()

            if segment:
                t_segment = T_segment()
                t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)
        elif case_type == 4:

            segment = db_session.query(Segment).filter(
                    (Segment.betriebsnr == 0)).first()

            if segment:
                t_segment = T_segment()
                t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)
        elif case_type == 5:

            for segment in db_session.query(Segment).filter(
                    (Segment.segmentcode != segmentno) &  (Segment.segmentgrup != 0)).all():
                t_segment = T_segment()
                t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)
        elif case_type == 6:
            for segment in db_session.query(Segment).filter(
                    (Segment.vip_level == 0) & 
                    (Segment.bezeich != '') 
                    # & (num_entries(Segment.bezeich, "$$0") == 1)
                    ).all():
                
                if num_entries(segment.bezeich, "$$0") == 1:
                    t_segment = T_segment()
                    t_segment_list.append(t_segment)

                buffer_copy(segment, t_segment)
            

    except Exception as e:
        error_message = traceback.format_exc()
        print("Error:", error_message)
        


    return generate_output()