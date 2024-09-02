from functions.additional_functions import *
import decimal
from datetime import date
from models import Segment, Segmentstat, Htparam

def prepare_segm_budgetbl():
    price_decimal = 0
    bill_date = None
    from_date = None
    segment_list_list = []
    segmentstat_list_list = []
    segment = segmentstat = htparam = None

    segment_list = segmentstat_list = None

    segment_list_list, Segment_list = create_model_like(Segment)
    segmentstat_list_list, Segmentstat_list = create_model_like(Segmentstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, bill_date, from_date, segment_list_list, segmentstat_list_list, segment, segmentstat, htparam


        nonlocal segment_list, segmentstat_list
        nonlocal segment_list_list, segmentstat_list_list
        return {"price_decimal": price_decimal, "bill_date": bill_date, "from_date": from_date, "segment-list": segment_list_list, "segmentstat-list": segmentstat_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    from_date = bill_date

    for segment in db_session.query(Segment).filter(
            (not Segment.bezeich.op("~")(".*\$\$0.*"))).all():
        segment_list = Segment_list()
        segment_list_list.append(segment_list)

        buffer_copy(segment, segment_list)

    segment_list = query(segment_list_list, first=True)

    if segment_list:

        for segmentstat in db_session.query(Segmentstat).filter(
                (Segmentstat.segmentcode == segment_list.segmentcode) &  (Segmentstat.datum >= from_date)).all():
            segmentstat_list = Segmentstat_list()
            segmentstat_list_list.append(segmentstat_list)

            buffer_copy(segmentstat, segmentstat_list)

    return generate_output()