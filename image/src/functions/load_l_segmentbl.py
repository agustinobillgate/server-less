from functions.additional_functions import *
import decimal
from models import L_segment

def load_l_segmentbl():
    t_l_segment_list = []
    l_segment = None

    t_l_segment = None

    t_l_segment_list, T_l_segment = create_model_like(L_segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_segment_list, l_segment


        nonlocal t_l_segment
        nonlocal t_l_segment_list
        return {"t-l-segment": t_l_segment_list}

    for l_segment in db_session.query(L_segment).all():
        t_l_segment = T_l_segment()
        t_l_segment_list.append(t_l_segment)

        buffer_copy(l_segment, t_l_segment)

    return generate_output()