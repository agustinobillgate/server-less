from functions.additional_functions import *
import decimal
from models import Guestseg, Segment

def chg_gcf_btn_segmentbl(gastnr:int):
    mainsegm = ""
    segment_a_list = []
    guestseg = segment = None

    segment_a = None

    segment_a_list, Segment_a = create_model("Segment_a", {"bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainsegm, segment_a_list, guestseg, segment


        nonlocal segment_a
        nonlocal segment_a_list
        return {"mainsegm": mainsegm, "segment-a": segment_a_list}

    for guestseg in db_session.query(Guestseg).filter(
            (Guestseg.gastnr == gastnr)).all():

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            segment_a = Segment_a()
            segment_a_list.append(segment_a)

            segment_a.bezeich = segment.bezeich

    guestseg = db_session.query(Guestseg).filter(
            (Guestseg.gastnr == gastnr) &  (Guestseg.reihenfolge == 1)).first()

    if guestseg:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")

    return generate_output()