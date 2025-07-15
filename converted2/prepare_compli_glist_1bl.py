#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Segment

def prepare_compli_glist_1bl():

    prepare_cache ([Segment])

    ci_date = None
    first_segment = ""
    segm_list_data = []
    segment = None

    segm_list = None

    segm_list_data, Segm_list = create_model("Segm_list", {"segm_code":int, "segm_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, first_segment, segm_list_data, segment


        nonlocal segm_list
        nonlocal segm_list_data

        return {"ci_date": ci_date, "first_segment": first_segment, "segm-list": segm_list_data}


    ci_date = get_output(htpdate(87))

    segment = db_session.query(Segment).first()

    if segment:
        first_segment = " "

    for segment in db_session.query(Segment).filter(
             (Segment.bezeich != (first_segment).lower()) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).order_by(Segment._recid).all():
        segm_list = Segm_list()
        segm_list_data.append(segm_list)

        segm_list.segm_code = segment.segmentcode
        segm_list.segm_bezeich = segment.bezeich

    return generate_output()