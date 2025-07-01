#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guestseg, Segment

def chg_gcf_btn_segmentbl(gastnr:int):

    prepare_cache ([Guestseg, Segment])

    mainsegm = ""
    segment_a_list = []
    guestseg = segment = None

    segment_a = None

    segment_a_list, Segment_a = create_model("Segment_a", {"bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainsegm, segment_a_list, guestseg, segment
        nonlocal gastnr


        nonlocal segment_a
        nonlocal segment_a_list

        return {"mainsegm": mainsegm, "segment-a": segment_a_list}

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == gastnr)).order_by(Guestseg._recid).all():

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            segment_a = Segment_a()
            segment_a_list.append(segment_a)

            segment_a.bezeich = segment.bezeich

    guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastnr)],"reihenfolge": [(eq, 1)]})

    if guestseg:

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")

    return generate_output()