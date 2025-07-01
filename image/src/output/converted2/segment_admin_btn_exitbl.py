#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_segment

l_list_list, L_list = create_model_like(L_segment)

def segment_admin_btn_exitbl(l_list_list:[L_list], case_type:int):

    prepare_cache ([L_segment])

    l_segment = None

    t_l_segment = l_list = None

    t_l_segment_list, T_l_segment = create_model("T_l_segment", {"l_segmentcode":int, "l_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_segment
        nonlocal case_type


        nonlocal t_l_segment, l_list
        nonlocal t_l_segment_list

        return {}


    l_list = query(l_list_list, first=True)

    if not l_list:

        return generate_output()

    if case_type == 1:
        l_segment = L_segment()
        db_session.add(l_segment)

        l_segment.l_segmentcode = l_list.l_segmentcode


        l_segment.l_bezeich = l_list.l_bezeich

    elif case_type == 2:

        l_segment = get_cache (L_segment, {"l_segmentcode": [(eq, l_list.l_segmentcode)]})

        if l_segment:
            pass
            l_segment.l_bezeich = l_list.l_bezeich


            pass
            pass

    return generate_output()