#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Segment

def segm_adminbl():
    sbuff_data = []
    segment = None

    sbuff = None

    sbuff_data, Sbuff = create_model_like(Segment, {"long_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sbuff_data, segment


        nonlocal sbuff
        nonlocal sbuff_data

        return {"sbuff": sbuff_data}

    for segment in db_session.query(Segment).order_by(Segment.betriebsnr, Segment.segmentgrup, Segment.segmentcode).all():
        sbuff = Sbuff()
        sbuff_data.append(sbuff)

        buffer_copy(segment, sbuff)
        sbuff.long_bezeich = segment.bezeich

    return generate_output()