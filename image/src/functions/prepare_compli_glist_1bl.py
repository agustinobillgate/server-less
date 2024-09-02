from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Segment

def prepare_compli_glist_1bl():
    ci_date = None
    first_segment = ""
    segm_list_list = []
    segment = None

    segm_list = None

    segm_list_list, Segm_list = create_model("Segm_list", {"segm_code":int, "segm_bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, first_segment, segm_list_list, segment


        nonlocal segm_list
        nonlocal segm_list_list
        return {"ci_date": ci_date, "first_segment": first_segment, "segm-list": segm_list_list}


    ci_date = get_output(htpdate(87))

    segment = db_session.query(Segment).first()

    if segment:
        first_segment = " "

    for segment in db_session.query(Segment).filter(
            (Segment.bezeich != first_segment) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).all():
        segm_list = Segm_list()
        segm_list_list.append(segm_list)

        segm_list.segm_code = segmentcode
        segm_list.segm_bezeich = segment.bezeich

    return generate_output()