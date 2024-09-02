from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Guestseg, Segment

def read_guestsegbl(case_type:int, gastno:int, segmcode:int):
    t_guestseg_list = []
    vipnr1:int = 0
    vipnr2:int = 0
    vipnr3:int = 0
    vipnr4:int = 0
    vipnr5:int = 0
    vipnr6:int = 0
    vipnr7:int = 0
    vipnr8:int = 0
    vipnr9:int = 0
    guestseg = segment = None

    t_guestseg = None

    t_guestseg_list, T_guestseg = create_model_like(Guestseg)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_guestseg_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guestseg, segment


        nonlocal t_guestseg
        nonlocal t_guestseg_list
        return {"t-guestseg": t_guestseg_list}

    def get_vipnr():

        nonlocal t_guestseg_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guestseg, segment


        nonlocal t_guestseg
        nonlocal t_guestseg_list

        intout:int = 0
        intout = get_output(htpint(700))

        if intout != 0:
            vipnr1 = intout
        intout = get_output(htpint(701))

        if intout != 0:
            vipnr2 = intout
        intout = get_output(htpint(702))

        if intout != 0:
            vipnr3 = intout
        intout = get_output(htpint(703))

        if intout != 0:
            vipnr4 = intout
        intout = get_output(htpint(704))

        if intout != 0:
            vipnr5 = intout
        intout = get_output(htpint(705))

        if intout != 0:
            vipnr6 = intout
        intout = get_output(htpint(706))

        if intout != 0:
            vipnr7 = intout
        intout = get_output(htpint(707))

        if intout != 0:
            vipnr8 = intout
        intout = get_output(htpint(708))

        if intout != 0:
            vipnr9 = intout

    if case_type == 1:

        if segmcode == 0:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastno)).first()
        else:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastno) &  (Guestseg.segmentcode == segmcode)).first()

        if guestseg:
            t_guestseg = T_guestseg()
            t_guestseg_list.append(t_guestseg)

            buffer_copy(guestseg, t_guestseg)
    elif case_type == 2:
        get_vipnr()

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastno) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:
            t_guestseg = T_guestseg()
            t_guestseg_list.append(t_guestseg)

            buffer_copy(guestseg, t_guestseg)
    elif case_type == 3:

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastno) &  (Guestseg.reihenfolge == 1)).first()

        if not guestseg:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == gastno)).first()

        if guestseg:
            t_guestseg = T_guestseg()
            t_guestseg_list.append(t_guestseg)

            buffer_copy(guestseg, t_guestseg)
    elif case_type == 4:

        for guestseg in db_session.query(Guestseg).filter(
                (Guestseg.gastnr == gastno)).all():
            t_guestseg = T_guestseg()
            t_guestseg_list.append(t_guestseg)

            buffer_copy(guestseg, t_guestseg)

    elif case_type == 5:

        guestseg_obj_list = []
        for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) &  (Segment.betriebsnr == 4)).filter(
                (Guestseg.gastnr == gastno)).all():
            if guestseg._recid in guestseg_obj_list:
                continue
            else:
                guestseg_obj_list.append(guestseg._recid)


            t_guestseg = T_guestseg()
            t_guestseg_list.append(t_guestseg)

            buffer_copy(guestseg, t_guestseg)

            return generate_output()


    return generate_output()