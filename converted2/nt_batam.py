from functions.additional_functions import *
import decimal
from datetime import date
from models import Segment, Reservation, Htparam, Zimmer, Res_line

def nt_batam():
    add_fact:int = 10
    curr_resnr:int = 0
    curr_anz:int = 0
    n100:int = 0
    actual_occ:int = 0
    soll_occ:int = 0
    soll_arr_occ:int = 0
    soll_inh_occ:int = 0
    act_arr_today:int = 0
    act_inhouse:int = 0
    remain_occ:int = 0
    inh_occ:int = 0
    inh_occ1:int = 0
    min_occ:int = 50
    max_occ:int = 70
    arr_fact:decimal = 0.7
    ci_date:date = None
    bill_date:date = None
    max_date:date = None
    curr_date:date = None
    segment = reservation = htparam = zimmer = res_line = None

    s_list = res_list = sbuff = rbuff = tbuff = None

    s_list_list, S_list = create_model("S_list", {"segmentcode":int, "actual_anz":int, "soll_anz":int})
    res_list_list, Res_list = create_model("Res_list", {"segmentcode":int, "resnr":int, "actual_anz":int})

    Sbuff = create_buffer("Sbuff",Segment)
    Rbuff = create_buffer("Rbuff",Reservation)
    Tbuff = S_list
    tbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal add_fact, curr_resnr, curr_anz, n100, actual_occ, soll_occ, soll_arr_occ, soll_inh_occ, act_arr_today, act_inhouse, remain_occ, inh_occ, inh_occ1, min_occ, max_occ, arr_fact, ci_date, bill_date, max_date, curr_date, segment, reservation, htparam, zimmer, res_line
        nonlocal sbuff, rbuff, tbuff


        nonlocal s_list, res_list, sbuff, rbuff, tbuff
        nonlocal s_list_list, res_list_list

        return {}

    def cal_actual_occ(do_flag:bool):

        nonlocal add_fact, curr_resnr, curr_anz, n100, actual_occ, soll_occ, soll_arr_occ, soll_inh_occ, act_arr_today, act_inhouse, remain_occ, inh_occ, inh_occ1, min_occ, max_occ, arr_fact, ci_date, bill_date, max_date, curr_date, segment, reservation, htparam, zimmer, res_line
        nonlocal sbuff, rbuff, tbuff


        nonlocal s_list, res_list, sbuff, rbuff, tbuff
        nonlocal s_list_list, res_list_list

        segbuff = None
        Segbuff =  create_buffer("Segbuff",Segment)
        actual_occ = 0
        act_arr_today = 0
        act_inhouse = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.abreise > ci_date)).order_by(Res_line.ankunft.desc()).all():

            if do_flag:

                reservation = db_session.query(Reservation).filter(
                         (Reservation.resnr == res_line.resnr)).first()

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == reservation.segmentcode)).first()

                if max_date == None:
                    max_date = res_line.ankunft

                if segment.vip_level > 0:

                    rbuff = db_session.query(Rbuff).filter(
                             (Rbuff._recid == reservation._recid)).first()
                    rbuff.segmentcode = segment.vip_level

            if res_line.ankunft <= ci_date:
                actual_occ = actual_occ + res_line.zimmeranz

            if res_line.ankunft == ci_date:
                act_arr_today = act_arr_today + res_line.zimmeranz
            else:
                act_inhouse = act_inhouse + res_line.zimmeranz


    def do_arrival():

        nonlocal add_fact, curr_resnr, curr_anz, n100, actual_occ, soll_occ, soll_arr_occ, soll_inh_occ, act_arr_today, act_inhouse, remain_occ, inh_occ, inh_occ1, min_occ, max_occ, arr_fact, ci_date, bill_date, max_date, curr_date, segment, reservation, htparam, zimmer, res_line
        nonlocal sbuff, rbuff, tbuff


        nonlocal s_list, res_list, sbuff, rbuff, tbuff
        nonlocal s_list_list, res_list_list


        inh_occ = 0
        inh_occ1 = 0
        curr_resnr = 0


        s_list_list.clear()
        res_list_list.clear()

        res_line_obj_list = []
        for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                 (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zipreis > 0) & (Res_line.ankunft == ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.zimmeranz).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            s_list = query(s_list_list, filters=(lambda s_list: s_list.segmentcode == reservation.segmentcode), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.segmentcode = reservation.segmentcode


            inh_occ = inh_occ + res_line.zimmeranz
            s_list.actual_anz = s_list.actual_anz + res_line.zimmeranz

            res_list = query(res_list_list, filters=(lambda res_list: res_list.segmentcode == reservation.segmentcode and res_list.resnr == reservation.resnr), first=True)

            if not res_list:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.resnr = reservation.resnr
                res_list.segmentcode = reservation.segmentcode


            res_list.actual_anz = res_list.actual_anz + res_line.zimmeranz

        for s_list in query(s_list_list, sort_by=[("actual_anz",False)]):
            s_list.soll_anz = s_list.actual_anz * remain_occ / inh_occ

            if s_list.soll_anz == 0:
                s_list.soll_anz = 1
            inh_occ1 = inh_occ1 + s_list.soll_anz

        for s_list in query(s_list_list, sort_by=[("actual_anz",True)]):
            s_list.soll_anz = s_list.soll_anz - (inh_occ1 - remain_occ)

            if s_list.soll_anz <= 0:
                s_list.soll_anz = 1

            elif s_list.soll_anz > s_list.actual_anz:
                s_list.soll_anz = s_list.actual_anz

            tbuff = query(tbuff_list, filters=(lambda tbuff: tbuff._recid == s_list._recid), first=True)
            break

        for s_list in query(s_list_list, sort_by=[("soll_anz",False)]):
            inh_occ = 0

            for res_list in query(res_list_list, filters=(lambda res_list: res_list.segmentcode == s_list.segmentcode), sort_by=[("actual_anz",True)]):

                res_line_obj_list = []
                for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == s_list.segmentcode)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                         (Res_line.resnr == res_list.resnr) & (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.gratis == 0) & (Res_line.ankunft == ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.resnr, Res_line.zimmeranz, Res_line.abreise.desc()).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    if curr_resnr == 0:
                        curr_resnr = res_line.resnr

                    if res_line.resstatus != 13:
                        inh_occ = inh_occ + res_line.zimmeranz

                    if inh_occ <= s_list.soll_anz:

                        if segment.vip_level > 0:

                            rbuff = db_session.query(Rbuff).filter(
                                     (Rbuff.resnr == res_line.resnr)).first()
                            rbuff.segmentcode = segment.vip_level

                    elif (inh_occ > s_list.soll_anz) and (segment.vip_level == 0):

                        if curr_resnr != res_line.resnr:

                            sbuff = db_session.query(Sbuff).filter(
                                     (Sbuff.vip_level == segment.segmentcode)).first()

                            rbuff = db_session.query(Rbuff).filter(
                                     (Rbuff.resnr == res_line.resnr)).first()
                            rbuff.segmentcode = sbuff.segmentcode

                        elif res_line.resstatus != 13:
                            tbuff.soll_anz = tbuff.soll_anz - res_line.zimmeranz


                    curr_resnr = res_line.resnr


    def do_inhouse():

        nonlocal add_fact, curr_resnr, curr_anz, n100, actual_occ, soll_occ, soll_arr_occ, soll_inh_occ, act_arr_today, act_inhouse, remain_occ, inh_occ, inh_occ1, min_occ, max_occ, arr_fact, ci_date, bill_date, max_date, curr_date, segment, reservation, htparam, zimmer, res_line
        nonlocal sbuff, rbuff, tbuff


        nonlocal s_list, res_list, sbuff, rbuff, tbuff
        nonlocal s_list_list, res_list_list


        inh_occ = 0
        inh_occ1 = 0
        curr_resnr = 0


        s_list_list.clear()
        res_list_list.clear()

        res_line_obj_list = []
        for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                 (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zipreis > 0) & (Res_line.ankunft < ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.zimmeranz).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            s_list = query(s_list_list, filters=(lambda s_list: s_list.segmentcode == reservation.segmentcode), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.segmentcode = reservation.segmentcode


            inh_occ = inh_occ + res_line.zimmeranz
            s_list.actual_anz = s_list.actual_anz + res_line.zimmeranz

            res_list = query(res_list_list, filters=(lambda res_list: res_list.segmentcode == reservation.segmentcode and res_list.resnr == reservation.resnr), first=True)

            if not res_list:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.resnr = reservation.resnr
                res_list.segmentcode = reservation.segmentcode


            res_list.actual_anz = res_list.actual_anz + res_line.zimmeranz

        for s_list in query(s_list_list, sort_by=[("actual_anz",False)]):
            s_list.soll_anz = s_list.actual_anz * remain_occ / inh_occ

            if s_list.soll_anz == 0:
                s_list.soll_anz = 1
            inh_occ1 = inh_occ1 + s_list.soll_anz

        for s_list in query(s_list_list, sort_by=[("actual_anz",True)]):
            s_list.soll_anz = s_list.soll_anz - (inh_occ1 - remain_occ)

            if s_list.soll_anz <= 0:
                s_list.soll_anz = 1

            elif s_list.soll_anz > s_list.actual_anz:
                s_list.soll_anz = s_list.actual_anz

            tbuff = query(tbuff_list, filters=(lambda tbuff: tbuff._recid == s_list._recid), first=True)
            break

        for s_list in query(s_list_list, sort_by=[("soll_anz",False)]):
            inh_occ = 0

            for res_list in query(res_list_list, filters=(lambda res_list: res_list.segmentcode == s_list.segmentcode), sort_by=[("actual_anz",True)]):

                res_line_obj_list = []
                for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == s_list.segmentcode)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                         (Res_line.resnr == res_list.resnr) & (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.gratis == 0) & (Res_line.ankunft < ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.resnr, Res_line.zimmeranz, Res_line.abreise.desc()).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    if curr_resnr == 0:
                        curr_resnr = res_line.resnr

                    if res_line.resstatus != 13:
                        inh_occ = inh_occ + res_line.zimmeranz

                    if inh_occ <= s_list.soll_anz:

                        if segment.vip_level > 0:

                            rbuff = db_session.query(Rbuff).filter(
                                     (Rbuff.resnr == res_line.resnr)).first()
                            rbuff.segmentcode = segment.vip_level

                    elif (inh_occ > s_list.soll_anz) and (segment.vip_level == 0):

                        if curr_resnr != res_line.resnr:

                            sbuff = db_session.query(Sbuff).filter(
                                     (Sbuff.vip_level == segment.segmentcode)).first()

                            rbuff = db_session.query(Rbuff).filter(
                                     (Rbuff.resnr == res_line.resnr)).first()
                            rbuff.segmentcode = sbuff.segmentcode

                        elif res_line.resstatus != 13:
                            tbuff.soll_anz = tbuff.soll_anz - res_line.zimmeranz


                    curr_resnr = res_line.resnr


    def next_days_occ():

        nonlocal add_fact, curr_resnr, curr_anz, n100, actual_occ, soll_occ, soll_arr_occ, soll_inh_occ, act_arr_today, act_inhouse, remain_occ, inh_occ, inh_occ1, min_occ, max_occ, arr_fact, ci_date, bill_date, max_date, curr_date, segment, reservation, htparam, zimmer, res_line
        nonlocal sbuff, rbuff, tbuff


        nonlocal s_list, res_list, sbuff, rbuff, tbuff
        nonlocal s_list_list, res_list_list

        rline = None
        Rline =  create_buffer("Rline",Res_line)
        inh_occ = 0
        inh_occ1 = 0
        curr_resnr = 0


        s_list_list.clear()
        res_list_list.clear()

        res_line_obj_list = []
        for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode) & (Segment.vip_level == 0)).filter(
                 (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zipreis > 0) & (Res_line.ankunft <= ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.zimmeranz).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            inh_occ = inh_occ + res_line.zimmeranz

        if inh_occ <= soll_occ:

            return
        inh_occ = 0

        res_line_obj_list = []
        for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                 (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zipreis > 0) & (Res_line.ankunft <= ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.zimmeranz).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            s_list = query(s_list_list, filters=(lambda s_list: s_list.segmentcode == reservation.segmentcode), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.segmentcode = reservation.segmentcode


            inh_occ = inh_occ + res_line.zimmeranz
            s_list.actual_anz = s_list.actual_anz + res_line.zimmeranz

            res_list = query(res_list_list, filters=(lambda res_list: res_list.segmentcode == reservation.segmentcode and res_list.resnr == reservation.resnr), first=True)

            if not res_list:
                res_list = Res_list()
                res_list_list.append(res_list)

                res_list.resnr = reservation.resnr
                res_list.segmentcode = reservation.segmentcode


            res_list.actual_anz = res_list.actual_anz + res_line.zimmeranz

        for s_list in query(s_list_list, sort_by=[("actual_anz",False)]):
            s_list.soll_anz = s_list.actual_anz * soll_occ / inh_occ

            if s_list.soll_anz == 0:
                s_list.soll_anz = 1
            inh_occ1 = inh_occ1 + s_list.soll_anz

        for s_list in query(s_list_list, sort_by=[("actual_anz",True)]):
            s_list.soll_anz = s_list.soll_anz - (inh_occ1 - soll_occ)

            if s_list.soll_anz <= 0:
                s_list.soll_anz = 1

            elif s_list.soll_anz > s_list.actual_anz:
                s_list.soll_anz = s_list.actual_anz

            tbuff = query(tbuff_list, filters=(lambda tbuff: tbuff._recid == s_list._recid), first=True)
            break
        inh_occ1 = 0

        for s_list in query(s_list_list, sort_by=[("soll_anz",False)]):
            inh_occ = 0

            for res_list in query(res_list_list, filters=(lambda res_list: res_list.segmentcode == s_list.segmentcode), sort_by=[("actual_anz",True)]):

                res_line_obj_list = []
                for res_line, reservation, segment in db_session.query(Res_line, Reservation, Segment).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode == s_list.segmentcode)).join(Segment,(Segment.segmentcode == Reservation.segmentcode)).filter(
                         (Res_line.resnr == res_list.resnr) & (Res_line.active_flag <= 1) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.gratis == 0) & (Res_line.ankunft <= ci_date) & (Res_line.abreise > ci_date)).order_by(Res_line.resnr, Res_line.zimmeranz, Res_line.abreise.desc()).all():
                    if res_line._recid in res_line_obj_list:
                        continue
                    else:
                        res_line_obj_list.append(res_line._recid)

                    if curr_resnr == 0:
                        curr_resnr = res_line.resnr

                    if (inh_occ <= s_list.soll_anz):

                        if (segment.vip_level == 0) and (res_line.resstatus != 13):
                            inh_occ1 = inh_occ1 + res_line.zimmeranz
                            inh_occ = inh_occ + res_line.zimmeranz

                    elif (inh_occ > s_list.soll_anz) and (segment.vip_level == 0):

                        rline = db_session.query(Rline).filter(
                                 (Rline.resnr == res_line.resnr) & (Rline.ankunft <= bill_date)).first()

                        if (curr_resnr != res_line.resnr) and not rline:

                            sbuff = db_session.query(Sbuff).filter(
                                     (Sbuff.vip_level == segment.segmentcode)).first()

                            rbuff = db_session.query(Rbuff).filter(
                                     (Rbuff.resnr == res_line.resnr)).first()
                            rbuff.segmentcode = sbuff.segmentcode

                        elif res_line.resstatus != 13:
                            tbuff.soll_anz = tbuff.soll_anz - res_line.zimmeranz


                    curr_resnr = res_line.resnr

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate
    bill_date = htparam.fdate

    for zimmer in db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).order_by(Zimmer._recid).all():
        n100 = n100 + 1
    cal_actual_occ(True)

    if actual_occ > min_occ:
        soll_occ = min_occ + (1 - (n100 - actual_occ) / (n100 - min_occ)) * (max_occ - min_occ)

        if act_arr_today <= (arr_fact * soll_occ):
            remain_occ = soll_occ - act_arr_today
            do_inhouse()

        elif act_arr_today > (arr_fact * soll_occ):
            remain_occ = arr_fact * soll_occ

            if (soll_occ - remain_occ) > act_inhouse:
                remain_occ = soll_occ - act_inhouse
            do_arrival()
            remain_occ = soll_occ - remain_occ
            do_inhouse()
    ci_date = ci_date + timedelta(days=1)
    while ci_date <= max_date:
        cal_actual_occ(False)
        add_fact = add_fact + 1

        if add_fact > 20:
            add_fact = 20

        if actual_occ > min_occ:
            soll_occ = min_occ + (1 - (n100 - actual_occ) / (n100 - min_occ)) * (max_occ - min_occ)
            soll_occ = soll_occ * (1 + add_fact * 0.01)
            remain_occ = actual_occ - soll_occ
            next_days_occ()
        ci_date = ci_date + timedelta(days=1)

    return generate_output()