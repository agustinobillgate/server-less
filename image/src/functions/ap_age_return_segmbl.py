from functions.additional_functions import *
import decimal
from models import L_segment

def ap_age_return_segmbl(segm:int):
    avail_l_segment = False
    segm_bezeich = ""
    l_segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_segment, segm_bezeich, l_segment


        return {"avail_l_segment": avail_l_segment, "segm_bezeich": segm_bezeich}


    l_segment = db_session.query(L_segment).filter(
            (L_segmentcode == segm)).first()

    if l_segment:
        avail_l_segment = True
        segm_bezeich = l_segment.l_bezeich

    return generate_output()