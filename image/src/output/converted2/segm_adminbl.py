#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def segm_adminbl():
    sbuff_list = []
    segment = None

    sbuff = None

    sbuff_list, Sbuff = create_model_like(Segment, {"long_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sbuff_list, segment


        nonlocal sbuff
        nonlocal sbuff_list

        return {"sbuff": sbuff_list}

    for segment in db_session.query(Segment).order_by(Segment.betriebsnr, Segment.segmentgrup, Segment.segmentcode).all():
        sbuff = Sbuff()
        sbuff_list.append(sbuff)

        buffer_copy(segment, sbuff)
        sbuff.long_bezeich = segment.bezeich

    return generate_output()