#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_segment

def prepare_segment_adminbl():

    prepare_cache ([L_segment])

    t_l_segment_data = []
    l_segment = None

    t_l_segment = None

    t_l_segment_data, T_l_segment = create_model("T_l_segment", {"l_segmentcode":int, "l_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_segment_data, l_segment


        nonlocal t_l_segment
        nonlocal t_l_segment_data

        return {"t-l-segment": t_l_segment_data}

    for l_segment in db_session.query(L_segment).order_by(L_segment._recid).all():
        t_l_segment = T_l_segment()
        t_l_segment_data.append(t_l_segment)

        t_l_segment.l_segmentcode = l_segment.l_segmentcode
        t_l_segment.l_bezeich = l_segment.l_bezeich

    return generate_output()