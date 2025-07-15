#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def select_segmbl():

    prepare_cache ([Segment])

    segm_list_data = []
    segment = None

    segm_list = None

    segm_list_data, Segm_list = create_model("Segm_list", {"code":int, "name":string, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_list_data, segment


        nonlocal segm_list
        nonlocal segm_list_data

        return {"segm-list": segm_list_data}

    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr <= 2) & (Segment.vip_level == 0) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment.segmentcode).all():
        segm_list = Segm_list()
        segm_list_data.append(segm_list)

        segm_list.code = segment.segmentcode
        segm_list.name = segment.bezeich
        segm_list.remark = segment.bemerkung

    return generate_output()