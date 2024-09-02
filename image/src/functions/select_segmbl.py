from functions.additional_functions import *
import decimal
from models import Segment

def select_segmbl():
    segm_list_list = []
    segment = None

    segm_list = None

    segm_list_list, Segm_list = create_model("Segm_list", {"code":int, "name":str, "remark":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_list_list, segment


        nonlocal segm_list
        nonlocal segm_list_list
        return {"segm-list": segm_list_list}

    for segment in db_session.query(Segment).filter(
            (Segment.betriebsnr <= 2) &  (Segment.vip_level == 0) &  (num_entries(Segment.bezeich, "$$0") == 1)).all():
        segm_list = Segm_list()
        segm_list_list.append(segm_list)

        segm_list.code = segmentcode
        segm_list.name = segment.bezeich
        segm_list.remark = segment.bemerkung

    return generate_output()