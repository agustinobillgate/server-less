from functions.additional_functions import *
import decimal
from models import Segment

def get_vip():
    vipnr1 = 999999
    vipnr2 = 999999
    vipnr3 = 999999
    vipnr4 = 999999
    vipnr5 = 999999
    vipnr6 = 999999
    vipnr7 = 999999
    vipnr8 = 999999
    vipnr9 = 999999
    segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, segment

        return {"vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9}


    for segment in db_session.query(Segment).filter(
             (Segment.betriebsnr == 3)).order_by(Segment.segmentcode).all():

        if vipnr1 == 999999:
            vipnr1 = segment.segmentcode

        elif vipnr2 == 999999:
            vipnr2 = segment.segmentcode

        elif vipnr3 == 999999:
            vipnr3 = segment.segmentcode

        elif vipnr4 == 999999:
            vipnr4 = segment.segmentcode

        elif vipnr5 == 999999:
            vipnr5 = segment.segmentcode

        elif vipnr6 == 999999:
            vipnr6 = segment.segmentcode

        elif vipnr7 == 999999:
            vipnr7 = segment.segmentcode

        elif vipnr8 == 999999:
            vipnr8 = segment.segmentcode

        elif vipnr9 == 999999:
            vipnr9 = segment.segmentcode

    return generate_output()