#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.get_vipnrbl import get_vipnrbl
from models import Segment, Guestseg, Res_line

def update_vip_segmentbl(inp_gastnr:int, inp_segmcode:int):
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    vip_flag1:bool = False
    vip_flag2:bool = False
    vip_segm:int = 0
    prev_segm:int = 0
    segment = guestseg = res_line = None

    gsegm_list = hsegm_list = None

    gsegm_list_list, Gsegm_list = create_model_like(Segment)
    hsegm_list_list, Hsegm_list = create_model_like(Segment)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vip_flag1, vip_flag2, vip_segm, prev_segm, segment, guestseg, res_line
        nonlocal inp_gastnr, inp_segmcode


        nonlocal gsegm_list, hsegm_list
        nonlocal gsegm_list_list, hsegm_list_list

        return {}

    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == inp_gastnr)).order_by(Guestseg._recid).all():
        db_session.delete(guestseg)

    if inp_segmcode == 0:

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, inp_gastnr)]})

        if guestseg:
            db_session.delete(guestseg)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnrmember == inp_gastnr) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():
            res_line.betrieb_gastmem = 0

    segment = get_cache (Segment, {"segmentcode": [(eq, inp_segmcode)]})

    if segment:
        guestseg = Guestseg()
        db_session.add(guestseg)

        guestseg.gastnr = inp_gastnr
        guestseg.segmentcode = inp_segmcode
        guestseg.reihenfolge = 1

    guestseg = get_cache (Guestseg, {"gastnr": [(eq, inp_gastnr)]})

    if guestseg:
        prev_segm = guestseg.segmentcode

        if prev_segm != inp_segmcode:
            guestseg.segmentcode = inp_segmcode

    segment = get_cache (Segment, {"segmentcode": [(eq, inp_segmcode)]})

    if segment:
        vip_flag2 = True

        if (inp_segmcode == vipnr1 or inp_segmcode == vipnr2 or inp_segmcode == vipnr3 or inp_segmcode == vipnr4 or inp_segmcode == vipnr5 or inp_segmcode == vipnr6 or inp_segmcode == vipnr7 or inp_segmcode == vipnr8 or inp_segmcode == vipnr9):
            vip_segm = segment.segmentcode

    for segment in db_session.query(Segment).filter(
             (Segment.vip_level == 0) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment._recid).all():
        hsegm_list = Hsegm_list()
        hsegm_list_list.append(hsegm_list)

        buffer_copy(segment, hsegm_list)

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == inp_gastnr)).order_by(Guestseg._recid).all():

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
        gsegm_list = Gsegm_list()
        gsegm_list_list.append(gsegm_list)

        gsegm_list.segmentcode = segment.segmentcode
        gsegm_list.bezeich = segment.bezeich

        hsegm_list = query(hsegm_list_list, filters=(lambda hsegm_list: hsegm_list.segmentcode == gsegm_list.segmentcode), first=True)

        if hsegm_list:
            hsegm_list_list.remove(hsegm_list)

    gsegm_list = query(gsegm_list_list, filters=(lambda gsegm_list:(gsegm_list.segmentcode == vipnr1 or gsegm_list.segmentcode == vipnr2 or gsegm_list.segmentcode == vipnr3 or gsegm_list.segmentcode == vipnr4 or gsegm_list.segmentcode == vipnr5 or gsegm_list.segmentcode == vipnr6 or gsegm_list.segmentcode == vipnr7 or gsegm_list.segmentcode == vipnr8 or gsegm_list.segmentcode == vipnr9)), first=True)

    if gsegm_list:
        vip_flag1 = True

    if vip_flag1:

        res_line = get_cache (Res_line, {"gastnrmember": [(eq, inp_gastnr)],"active_flag": [(le, 1)]})
        while None != res_line:
            pass
            res_line.betrieb_gastmem = vip_segm
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnrmember == inp_gastnr) & (Res_line.active_flag <= 1) & (Res_line._recid > curr_recid)).first()

    return generate_output()