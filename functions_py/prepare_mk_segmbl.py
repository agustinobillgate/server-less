#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 13/8/2025
# num_entries
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.get_vipnrbl import get_vipnrbl
from models import Segment, Guestseg

def prepare_mk_segmbl(gastnr:int):

    prepare_cache ([Guestseg])

    gtitle = ""
    mainscode = 0
    mainseg = 0
    vip_flag1 = False
    hsegm_list_data = []
    gsegm_list_data = []
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

    hsegm_list = gsegm_list = None

    hsegm_list_data, Hsegm_list = create_model_like(Segment)
    gsegm_list_data, Gsegm_list = create_model_like(Segment)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtitle, mainscode, mainseg, vip_flag1, hsegm_list_data, gsegm_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, segment, guestseg
        nonlocal gastnr


        nonlocal hsegm_list, gsegm_list
        nonlocal hsegm_list_data, gsegm_list_data

        return {"gtitle": gtitle, "mainscode": mainscode, "mainseg": mainseg, "vip_flag1": vip_flag1, "hsegm-list": hsegm_list_data, "gsegm-list": gsegm_list_data}

    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    # Rd 13/8/2025
    # num-entries
    # for segment in db_session.query(Segment).filter(
    #          (Segment.vip_level == 0) & (num_entries(Segment.bezeich, "$$0") == 1)).order_by(Segment._recid).all():
    for segment in db_session.query(Segment).filter(Segment.vip_level == 0).order_by(Segment._recid).all():
        if (num_entries(segment.bezeich, "$$0") == 1):
            hsegm_list = Hsegm_list()
            hsegm_list_data.append(hsegm_list)

            buffer_copy(segment, hsegm_list)

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == gastnr)).order_by(Guestseg._recid).all():

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
        gsegm_list = Gsegm_list()
        gsegm_list_data.append(gsegm_list)

        gsegm_list.segmentcode = segment.segmentcode
        gsegm_list.bezeich = segment.bezeich

        if guestseg.reihenfolge == 1:
            gtitle = " " + segment.bezeich
            mainscode = segment.segmentcode
            mainseg = mainscode

        hsegm_list = query(hsegm_list_data, filters=(lambda hsegm_list: hsegm_list.segmentcode == gsegm_list.segmentcode), first=True)

        if hsegm_list:
            hsegm_list_data.remove(hsegm_list)

    gsegm_list = query(gsegm_list_data, filters=(lambda gsegm_list:(gsegm_list.segmentcode == vipnr1 or gsegm_list.segmentcode == vipnr2 or gsegm_list.segmentcode == vipnr3 or gsegm_list.segmentcode == vipnr4 or gsegm_list.segmentcode == vipnr5 or gsegm_list.segmentcode == vipnr6 or gsegm_list.segmentcode == vipnr7 or gsegm_list.segmentcode == vipnr8 or gsegm_list.segmentcode == vipnr9)), first=True)

    if gsegm_list:
        vip_flag1 = True

    return generate_output()