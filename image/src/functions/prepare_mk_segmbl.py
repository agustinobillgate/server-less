from functions.additional_functions import *
import decimal
from functions.get_vipnrbl import get_vipnrbl
from models import Segment, Guestseg

def prepare_mk_segmbl(gastnr:int):
    gtitle = ""
    mainscode = 0
    mainseg = 0
    vip_flag1 = False
    hsegm_list_list = []
    gsegm_list_list = []
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

    hsegm_list_list, Hsegm_list = create_model_like(Segment)
    gsegm_list_list, Gsegm_list = create_model_like(Segment)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtitle, mainscode, mainseg, vip_flag1, hsegm_list_list, gsegm_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, segment, guestseg


        nonlocal hsegm_list, gsegm_list
        nonlocal hsegm_list_list, gsegm_list_list
        return {"gtitle": gtitle, "mainscode": mainscode, "mainseg": mainseg, "vip_flag1": vip_flag1, "hsegm-list": hsegm_list_list, "gsegm-list": gsegm_list_list}

    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    for segment in db_session.query(Segment).filter(
            (Segment.vip_level == 0) 
            # & (num_entries(Segment.bezeich, "$$0") == 1)
            ).all():
        if num_entries(segment.bezeich, "$$0") == 1:
            hsegm_list = Hsegm_list()
            hsegm_list_list.append(hsegm_list)

        buffer_copy(segment, hsegm_list)

    for guestseg in db_session.query(Guestseg).filter(
            (Guestseg.gastnr == gastnr)).all():

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()
        gsegm_list = Gsegm_list()
        gsegm_list_list.append(gsegm_list)

        gsegm_list.segmentcode = segment.segmentcode
        gsegm_list.bezeich = segment.bezeich

        if guestseg.reihenfolge == 1:
            gtitle = "        " + segment.bezeich
            mainscode = segment.segmentcode
            mainseg = mainscode

        hsegm_list = query(hsegm_list_list, filters=(lambda hsegm_list :hsegm_list.segmentcode == gsegm_list.segmentcode), first=True)

        if hsegm_list:
            hsegm_list_list.remove(hsegm_list)

    gsegm_list = query(gsegm_list_list, filters=(lambda gsegm_list :(gsegm_list.segmentcode == vipnr1 or 
                                                                     gsegm_list.segmentcode == vipnr2 or 
                                                                     gsegm_list.segmentcode == vipnr3 or 
                                                                     gsegm_list.segmentcode == vipnr4 or 
                                                                     gsegm_list.segmentcode == vipnr5 or 
                                                                     gsegm_list.segmentcode == vipnr6 or 
                                                                     gsegm_list.segmentcode == vipnr7 or 
                                                                     gsegm_list.segmentcode == vipnr8 or 
                                                                     gsegm_list.segmentcode == vipnr9)), 
                                                                     first=True)

    if gsegm_list:
        vip_flag1 = True

    return generate_output()