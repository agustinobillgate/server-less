from functions.additional_functions import *
import decimal
from functions.get_vipnrbl import get_vipnrbl
from models import Segment, Guestseg

def get_vip_segmentbl(inp_gastnr:int):
    t_segment_list = []
    segm_code = 0
    segm_bez = ""
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    segment = guestseg = None

    t_segment = None

    t_segment_list, T_segment = create_model_like(Segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_segment_list, segm_code, segm_bez, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, segment, guestseg


        nonlocal t_segment
        nonlocal t_segment_list
        return {"t-segment": t_segment_list, "segm_code": segm_code, "segm_bez": segm_bez}


    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    guestseg = db_session.query(Guestseg).filter(
            (Guestseg.gastnr == inp_gastnr)).first()

    if not guestseg:

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr == 3)).all():
            t_segment = T_segment()
            t_segment_list.append(t_segment)

            buffer_copy(segment, t_segment)

    elif guestseg:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            segm_bez = entry(0, segment.bezeich, "$$0")

        for segment in db_session.query(Segment).filter(
                (Segment.betriebsnr == 3)).all():
            t_segment = T_segment()
            t_segment_list.append(t_segment)

            buffer_copy(segment, t_segment)

    return generate_output()