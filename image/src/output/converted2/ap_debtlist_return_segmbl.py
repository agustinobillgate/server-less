#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_segment

def ap_debtlist_return_segmbl(segm:int):

    prepare_cache ([L_segment])

    avail_l_segment = False
    segm_bezeich = ""
    l_segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_segment, segm_bezeich, l_segment
        nonlocal segm

        return {"avail_l_segment": avail_l_segment, "segm_bezeich": segm_bezeich}


    l_segment = get_cache (L_segment, {"l_segmentcode": [(eq, segm)]})

    if l_segment:
        avail_l_segment = True
        segm_bezeich = l_segment.l_bezeich

    return generate_output()