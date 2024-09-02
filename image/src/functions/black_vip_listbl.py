from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Htparam, Guestseg, Segment

def black_vip_listbl(pvilanguage:int, gastno:int):
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
    lvcarea:str = "black_vip_list"
    htparam = guestseg = segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment


        return {"msg_str": msg_str}

    def get_vipnr():

        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 700)).first()

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 701)).first()

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 702)).first()

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 703)).first()

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 704)).first()

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 705)).first()

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 706)).first()

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 707)).first()

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 708)).first()

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger

    def check_black_vip_list():

        nonlocal msg_str, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, htparam, guestseg, segment

        integerflag:int = 0
        integerflag = get_output(htpint(709))

        if integerflag != 0:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastno) &  (Guestseg.segmentcode == integerflag)).first()

            if guestseg:

                segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == integerflag)).first()
                msg_str = "&W" + translateExtended ("ATTENTION: ", lvcarea, "") + chr(10) + translateExtended ("SegmentCode:", lvcarea, "") + " " + segment.bezeich + chr(2)

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastno) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode)).first()
            msg_str = msg_str + translateExtended ("VIP Guest: ", lvcarea, "") + chr(10) + translateExtended ("SegmentCode:", lvcarea, "") + " " + segment.bezeich

    get_vipnr()
    check_black_vip_list()

    return generate_output()