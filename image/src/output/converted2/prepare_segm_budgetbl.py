#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Segment, Segmentstat, Htparam

def prepare_segm_budgetbl():

    prepare_cache ([Htparam])

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    from_date = bill_date

    for segment in db_session.query(Segment).filter(
             (not_(matches(Segment.bezeich,("*$$0*"))))).order_by(Segment.segmentcode).all():
        segment_list = Segment_list()
        segment_list_list.append(segment_list)

        buffer_copy(segment, segment_list)

    segment_list = query(segment_list_list, first=True)

    if segment_list:

        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.segmentcode == segment_list.segmentcode) & (Segmentstat.datum >= from_date)).order_by(Segmentstat.datum).all():
            segmentstat_list = Segmentstat_list()
            segmentstat_list_list.append(segmentstat_list)

            buffer_copy(segmentstat, segmentstat_list)

    return generate_output()