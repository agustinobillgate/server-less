#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.get_vipnrbl import get_vipnrbl
from models import Segment, Guestseg, Htparam, Res_line

gsegm_list_data, Gsegm_list = create_model_like(Segment)

def mk_segmbl(gsegm_list_data:[Gsegm_list], gastnr:int, done:bool, flag:bool, change_it:bool, vip_flag1:bool, mainscode:int, mainseg:int):

    prepare_cache ([Htparam])

    vip_flag2:bool = False
    vip_segm:int = 0
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    vipnr10:int = 999999999
    segment = guestseg = htparam = res_line = None

    gsegm_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vip_flag2, vip_segm, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, segment, guestseg, htparam, res_line
        nonlocal gastnr, done, flag, change_it, vip_flag1, mainscode, mainseg


        nonlocal gsegm_list

        return {}


    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    if done  and flag  and change_it:

        for guestseg in db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gastnr)).order_by(Guestseg._recid).all():
            db_session.delete(guestseg)

        gsegm_list = query(gsegm_list_data, filters=(lambda gsegm_list: gsegm_list.segmentcode == mainscode), first=True)

        if gsegm_list:
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = gastnr
            guestseg.segmentcode = gsegm_list.segmentcode
            guestseg.reihenfolge = 1

        for gsegm_list in query(gsegm_list_data, filters=(lambda gsegm_list: gsegm_list.segmentcode != mainscode)):
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = gastnr
            guestseg.segmentcode = gsegm_list.segmentcode

        if mainscode != mainseg:
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})

    if htparam and htparam.finteger != 0:
        vipnr10 = htparam.finteger

    gsegm_list = query(gsegm_list_data, filters=(lambda gsegm_list:(gsegm_list.segmentcode == vipnr1 or gsegm_list.segmentcode == vipnr2 or gsegm_list.segmentcode == vipnr3 or gsegm_list.segmentcode == vipnr4 or gsegm_list.segmentcode == vipnr5 or gsegm_list.segmentcode == vipnr6 or gsegm_list.segmentcode == vipnr7 or gsegm_list.segmentcode == vipnr8 or gsegm_list.segmentcode == vipnr9 or gsegm_list.segmentcode == vipnr10)), first=True)

    if gsegm_list:
        vip_flag2 = True
        vip_segm = gsegm_list.segmentcode

    if vip_flag1 != vip_flag2:

        res_line = get_cache (Res_line, {"gastnrmember": [(eq, gastnr)],"active_flag": [(le, 1)]})
        while None != res_line:
            pass
            res_line.betrieb_gastmem = vip_segm
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnrmember == gastnr) & (Res_line.active_flag <= 1) & (Res_line._recid > curr_recid)).first()

    return generate_output()