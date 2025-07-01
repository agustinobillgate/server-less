#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Segment, H_bill

def ts_tbplan_load_segmentbl(vkey:int, bill_number:int, dept_number:int):

    prepare_cache ([H_bill])

    t_segment_list = []
    segment = h_bill = None

    t_segment = None

    t_segment_list, T_segment = create_model_like(Segment)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_list, segment, h_bill
        nonlocal vkey, bill_number, dept_number


        nonlocal t_segment
        nonlocal t_segment_list

        return {"t-segment": t_segment_list}

    if vkey == 1:

        for segment in db_session.query(Segment).filter(
                 (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.segmentcode).all():
            t_segment = T_segment()
            t_segment_list.append(t_segment)

            buffer_copy(segment, t_segment)

    elif vkey == 2:

        h_bill = get_cache (H_bill, {"rechnr": [(eq, bill_number)],"departement": [(eq, dept_number)],"segmentcode": [(ne, 0)]})

        if h_bill:

            if h_bill.resnr > 0:

                segment = get_cache (Segment, {"segmentcode": [(eq, h_bill.segmentcode)]})

                if segment:
                    t_segment = T_segment()
                    t_segment_list.append(t_segment)

                    buffer_copy(segment, t_segment)

    return generate_output()