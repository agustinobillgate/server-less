#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from models import Htparam, Guestseg, Segment

def black_vip_listbl(pvilanguage:int, gastno:int):

    prepare_cache ([Htparam, Guestseg, Segment])

    msg_str = ""
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    lvcarea:string = "black-vip-list"
    htparam = guestseg = segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment
        nonlocal pvilanguage, gastno

        return {"msg_str": msg_str}

    def get_vipnr():

        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment
        nonlocal pvilanguage, gastno

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger


    def check_black_vip_list():

        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment
        nonlocal pvilanguage, gastno

        integerflag:int = 0
        integerflag = get_output(htpint(709))

        if integerflag != 0:

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastno)],"segmentcode": [(eq, integerflag)]})

            if guestseg:

                segment = get_cache (Segment, {"segmentcode": [(eq, integerflag)]})
                msg_str = "&W" + translateExtended ("ATTENTION: ", lvcarea, "") + chr_unicode(10) + translateExtended ("SegmentCode:", lvcarea, "") + " " + segment.bezeich + chr_unicode(2)

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gastno) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
            msg_str = msg_str + translateExtended ("VIP Guest: ", lvcarea, "") + chr_unicode(10) + translateExtended ("SegmentCode:", lvcarea, "") + " " + segment.bezeich


    get_vipnr()
    check_black_vip_list()

    return generate_output()