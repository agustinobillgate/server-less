#using conversion tools version: 1.0.0.117

#-----------------------------------------
# Rd, 17-July-25, ()"*").lower() -> "*"
#-----------------------------------------


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Kontline, Htparam, Guest, Guest_pr, Zimkateg, Res_line, Zimmer, Reservation, Segment, Outorder

temp_list_data, Temp_list = create_model("Temp_list", {"rcode":string, "rmtype":string, "zikatnr":int})

def if_custom_pushall_availbl(currcode:string, from_date:date, to_date:date, becode:int, inp_str:string, pushrate:bool, temp_list_data:[Temp_list]):

    prepare_cache ([Queasy, Kontline, Htparam, Guest, Guest_pr, Zimkateg, Res_line, Zimmer, Reservation])

    done = False
    incl_tentative:bool = False
    allotment:bool = False
    end_date:date = None
    ci_date:date = None
    date_110:date = None
    curr_date:date = None
    cat_flag:bool = False
    all_room:bool = True
    do_it:bool = False
    bedsetup:bool = False
    catnr:int = 0
    cm_gastno:int = 0
    i:int = 0
    rm_occ:int = 0
    rm_ooo:int = 0
    rm_allot:int = 0
    occ_room:int = 0
    queasy = kontline = htparam = guest = guest_pr = zimkateg = res_line = zimmer = reservation = segment = outorder = None

    allotment = temp_list = rmcat_list = r_list = qsy = kline = None

    allotment_data, allotment = create_model("allotment", {"datum":date, "zikatnr":int, "res_allot":int, "allot":int, "ruecktage":int})
    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "typ":int, "sleeping":bool}, {"sleeping": True})
    r_list_data, R_list = create_model("R_list", {"rcode":string})

    Qsy = create_buffer("Qsy",Queasy)
    Kline = create_buffer("Kline",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, incl_tentative, allotment, end_date, ci_date, date_110, curr_date, cat_flag, all_room, do_it, bedsetup, catnr, cm_gastno, i, rm_occ, rm_ooo, rm_allot, occ_room, queasy, kontline, htparam, guest, guest_pr, zimkateg, res_line, zimmer, reservation, segment, outorder
        nonlocal currcode, from_date, to_date, becode, inp_str, pushrate
        nonlocal qsy, kline


        nonlocal allotment, temp_list, rmcat_list, r_list, qsy, kline
        nonlocal allotment_data, rmcat_list_data, r_list_data

        return {"done": done}

    def custom_pushall_avail():

        nonlocal done, incl_tentative, allotment, end_date, ci_date, date_110, curr_date, cat_flag, all_room, do_it, bedsetup, catnr, cm_gastno, i, rm_occ, rm_ooo, rm_allot, occ_room, queasy, kontline, htparam, guest, guest_pr, zimkateg, res_line, zimmer, reservation, segment, outorder
        nonlocal currcode, from_date, to_date, becode, inp_str, pushrate
        nonlocal qsy, kline


        nonlocal allotment, temp_list, rmcat_list, r_list, qsy, kline
        nonlocal allotment_data, rmcat_list_data, r_list_data

        vhp_limited:bool = False
        rline_origcode:string = ""
        iftask:string = ""
        for curr_date in date_range(from_date,to_date) :

            for rmcat_list in query(rmcat_list_data):
                rm_occ = 0
                rm_ooo = 0
                rm_allot = 0

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"char1": [(eq, "")],"number1": [(eq, rmcat_list.zikatnr)],"betriebsnr": [(eq, becode)]})

                if queasy:
                    rm_occ, rm_ooo, rm_allot = count_availability(queasy.date1, queasy.number1)

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.number3 = rm_ooo
                        qsy.logi1 = False
                        qsy.logi3 = True

                        if allotment:
                            qsy.number2 = rm_occ + rm_allot
                        else:
                            qsy.number2 = rm_occ
                        pass
                        pass
                else:
                    rm_occ, rm_ooo, rm_allot = count_availability(curr_date, rmcat_list.zikatnr)
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 171
                    queasy.number1 = rmcat_list.zikatnr
                    queasy.number3 = rm_ooo
                    queasy.date1 = curr_date
                    queasy.logi1 = False
                    queasy.logi2 = False
                    queasy.logi3 = True
                    queasy.char1 = ""
                    queasy.betriebsnr = becode

                    if allotment:
                        queasy.number2 = rm_occ + rm_allot
                    else:
                        queasy.number2 = rm_occ

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"char1": [(ne, "")],"number1": [(eq, rmcat_list.zikatnr)],"betriebsnr": [(eq, becode)]})

                if queasy:
                    occ_room = 0

                    if cat_flag:

                        res_line_obj_list = {}
                        res_line = Res_line()
                        zimkateg = Zimkateg()
                        for res_line.zinr, res_line.resnr, res_line.zimmer_wunsch, res_line.zimmeranz, res_line.kontignr, res_line._recid, zimkateg.typ, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.resnr, Res_line.zimmer_wunsch, Res_line.zimmeranz, Res_line.kontignr, Res_line._recid, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.typ == queasy.number1)).filter(
                                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= queasy.date1) & (Res_line.abreise > queasy.date1) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (matches(Res_line.zimmer_wunsch,("*$OrigCode$*")))).order_by(Res_line._recid).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            do_it = True

                            if res_line.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                rline_origcode = ""
                                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                                        rline_origcode = substring(iftask, 10)
                                        break

                                if rline_origcode == queasy.char1:
                                    occ_room = occ_room + res_line.zimmeranz

                    else:

                        for res_line in db_session.query(Res_line).filter(
                                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= queasy.date1) & (Res_line.abreise > queasy.date1) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (matches(Res_line.zimmer_wunsch,("*$OrigCode$*"))) & (Res_line.zikatnr == queasy.number1)).order_by(Res_line._recid).all():
                            do_it = True

                            if res_line.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                rline_origcode = ""
                                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                    iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                                    if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                                        rline_origcode = substring(iftask, 10)
                                        break

                                if rline_origcode == queasy.char1:
                                    occ_room = occ_room + res_line.zimmeranz


                    if cat_flag:

                        zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})
                    else:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                    if queasy.number2 != occ_room:

                        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                        if qsy:
                            qsy.number2 = occ_room
                            qsy.logi1 = False
                            qsy.logi2 = False
                            qsy.logi3 = True


                            pass
                            pass


    def rmtype_pushall_avail():

        nonlocal done, incl_tentative, allotment, end_date, ci_date, date_110, curr_date, cat_flag, all_room, do_it, bedsetup, catnr, cm_gastno, i, rm_occ, rm_ooo, rm_allot, occ_room, queasy, kontline, htparam, guest, guest_pr, zimkateg, res_line, zimmer, reservation, segment, outorder
        nonlocal currcode, from_date, to_date, becode, inp_str, pushrate
        nonlocal qsy, kline


        nonlocal allotment, temp_list, rmcat_list, r_list, qsy, kline
        nonlocal allotment_data, rmcat_list_data, r_list_data

        vhp_limited:bool = False
        rline_origcode:string = ""
        iftask:string = ""
        zikatnr:int = 0

        temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.rmtype.lower()  == (currcode).lower()), first=True)

        if temp_list:
            zikatnr = temp_list.zikatnr
        for curr_date in date_range(from_date,to_date) :
            rm_occ = 0
            rm_ooo = 0
            rm_allot = 0

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"char1": [(eq, "")],"number1": [(eq, zikatnr)],"betriebsnr": [(eq, becode)]})

            if queasy:
                rm_occ, rm_ooo, rm_allot = count_availability(queasy.date1, queasy.number1)

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.number3 = rm_ooo
                    qsy.logi1 = False
                    qsy.logi3 = True

                    if allotment:
                        qsy.number2 = rm_occ + rm_allot
                    else:
                        qsy.number2 = rm_occ
                    pass
                    pass
            else:
                rm_occ, rm_ooo, rm_allot = count_availability(curr_date, zikatnr)
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 171
                queasy.number1 = zikatnr
                queasy.number3 = rm_ooo
                queasy.date1 = curr_date
                queasy.logi1 = False
                queasy.logi2 = False
                queasy.logi3 = True
                queasy.char1 = ""
                queasy.betriebsnr = becode

                if allotment:
                    queasy.number2 = rm_occ + rm_allot
                else:
                    queasy.number2 = rm_occ

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"char1": [(ne, "")],"number1": [(eq, zikatnr)],"betriebsnr": [(eq, becode)]})

            if queasy:
                occ_room = 0

                if cat_flag:

                    res_line_obj_list = {}
                    res_line = Res_line()
                    zimkateg = Zimkateg()
                    for res_line.zinr, res_line.resnr, res_line.zimmer_wunsch, res_line.zimmeranz, res_line.kontignr, res_line._recid, zimkateg.typ, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.resnr, Res_line.zimmer_wunsch, Res_line.zimmeranz, Res_line.kontignr, Res_line._recid, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.typ == queasy.number1)).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= queasy.date1) & (Res_line.abreise > queasy.date1) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (matches(Res_line.zimmer_wunsch,("*$OrigCode$*")))).order_by(Res_line._recid).all():
                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rline_origcode = ""
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                                    rline_origcode = substring(iftask, 10)
                                    break

                            if rline_origcode == queasy.char1:
                                occ_room = occ_room + res_line.zimmeranz

                else:

                    for res_line in db_session.query(Res_line).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= queasy.date1) & (Res_line.abreise > queasy.date1) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (matches(Res_line.zimmer_wunsch,("*$OrigCode$*"))) & (Res_line.zikatnr == queasy.number1)).order_by(Res_line._recid).all():
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rline_origcode = ""
                            for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                                iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                                if substring(iftask, 0, 10) == ("$OrigCode$").lower() :
                                    rline_origcode = substring(iftask, 10)
                                    break

                            if rline_origcode == queasy.char1:
                                occ_room = occ_room + res_line.zimmeranz


                if cat_flag:

                    zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})
                else:

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                if queasy.number2 != occ_room:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.number2 = occ_room
                        qsy.logi1 = False
                        qsy.logi2 = False
                        qsy.logi3 = True


                        pass
                        pass


    def count_rmcateg():

        nonlocal done, incl_tentative, allotment, end_date, ci_date, date_110, curr_date, cat_flag, all_room, do_it, bedsetup, catnr, cm_gastno, i, rm_occ, rm_ooo, rm_allot, occ_room, queasy, kontline, htparam, guest, guest_pr, zimkateg, res_line, zimmer, reservation, segment, outorder
        nonlocal currcode, from_date, to_date, becode, inp_str, pushrate
        nonlocal qsy, kline


        nonlocal allotment, temp_list, rmcat_list, r_list, qsy, kline
        nonlocal allotment_data, rmcat_list_data, r_list_data

        zikatnr:int = 0
        rmcat_list_data.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg and zimkateg.verfuegbarkeit:

                if cat_flag and zimkateg.typ != 0:
                    zikatnr = zimkateg.typ
                else:
                    zikatnr = zimkateg.zikatnr

                temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.zikatnr == zikatnr), first=True)

                if (not all_room and temp_list) or all_room:

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zikatnr), first=True)

                    if not rmcat_list:
                        rmcat_list = Rmcat_list()
                        rmcat_list_data.append(rmcat_list)

                        rmcat_list.zikatnr = zikatnr
                        rmcat_list.typ = zimkateg.typ
                        rmcat_list.anzahl = 1


                    else:
                        rmcat_list.anzahl = rmcat_list.anzahl + 1


    def count_availability(curr_date:date, i_typ:int):

        nonlocal done, incl_tentative, allotment, end_date, ci_date, date_110, cat_flag, all_room, bedsetup, catnr, cm_gastno, i, rm_occ, rm_ooo, rm_allot, occ_room, queasy, kontline, htparam, guest, guest_pr, zimkateg, res_line, zimmer, reservation, segment, outorder
        nonlocal currcode, from_date, to_date, becode, inp_str, pushrate
        nonlocal qsy, kline


        nonlocal allotment, temp_list, rmcat_list, r_list, qsy, kline
        nonlocal allotment_data, rmcat_list_data, r_list_data

        rm_occ = 0
        rm_ooo = 0
        rm_allot = 0
        vhp_limited:bool = False
        do_it:bool = False

        def generate_inner_output():
            return (rm_occ, rm_ooo, rm_allot)


        kontline_obj_list = {}
        kontline = Kontline()
        zimkateg = Zimkateg()
        for kontline.zimmeranz, kontline.betriebsnr, kontline._recid, kontline.kontcode, zimkateg.typ, zimkateg.zikatnr, zimkateg._recid in db_session.query(Kontline.zimmeranz, Kontline.betriebsnr, Kontline._recid, Kontline.kontcode, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Kontline.zikatnr)).filter(
                 (Kontline.kontstatus == 1) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True

            if allotment and kontline.betriebsnr == 0 and curr_date >= (ci_date + timedelta(days=kontline.ruecktage)):
                do_it = True

            elif not allotment and kontline.betriebsnr == 1:
                do_it = True

            if do_it:

                if cat_flag and zimkateg.typ == i_typ:
                    rm_allot = rm_allot + kontline.zimmeranz

                elif not cat_flag and zimkateg.zikatnr == i_typ:
                    rm_allot = rm_allot + kontline.zimmeranz

        if cat_flag:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            for res_line.zinr, res_line.resnr, res_line.zimmer_wunsch, res_line.zimmeranz, res_line.kontignr, res_line._recid, zimkateg.typ, zimkateg.zikatnr, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.resnr, Res_line.zimmer_wunsch, Res_line.zimmeranz, Res_line.kontignr, Res_line._recid, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.typ == i_typ)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    rm_occ = rm_occ + res_line.zimmeranz

                kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kline:

                    if allotment and curr_date >= (ci_date + timedelta(days=kline.ruecktage)):

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
                    else:

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                    if kontline:
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rm_allot = rm_allot - res_line.zimmeranz

        else:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.zikatnr == i_typ) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    rm_occ = rm_occ + res_line.zimmeranz

                kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kline:

                    if allotment and curr_date >= (ci_date + timedelta(days=kline.ruecktage)):

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
                    else:

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                    if kontline:
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rm_allot = rm_allot - res_line.zimmeranz


        outorder_obj_list = {}
        for outorder, zimmer, zimkateg in db_session.query(Outorder, Zimmer, Zimkateg).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).filter(
                 (Outorder.betriebsnr <= 1) & (curr_date >= Outorder.gespstart) & (curr_date <= Outorder.gespende)).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            if cat_flag and zimkateg.typ == i_typ:
                rm_ooo = rm_ooo + 1

            elif not cat_flag and zimkateg.zikatnr == i_typ:
                rm_ooo = rm_ooo + 1

        if not allotment:
            rm_occ = rm_occ + rm_allot

        return generate_inner_output()


    done = False

    if num_entries(inp_str, "=") >= 2:
        incl_tentative = logical(entry(0, inp_str, "="))

    if num_entries(inp_str, "=") >= 3:
        allotment = logical(entry(2, inp_str, "="))

    if num_entries(inp_str, "=") >= 4:
        bedsetup = logical(entry(3, inp_str, "="))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        date_110 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam:

        if htparam.flogical:

            if date_110 < get_current_date():

                return generate_output()

    temp_list = query(temp_list_data, first=True)

    if temp_list:
        all_room = False

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:

        guest = get_cache (Guest, {"gastnr": [(eq, queasy.number2)]})

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

        if guest_pr:
            cm_gastno = guest.gastnr
        else:

            return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if bedsetup:
        cat_flag = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for temp_list in query(temp_list_data):

        if cat_flag:

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, temp_list.rmtype)]})

            if queasy:
                temp_list.zikatnr = queasy.number1
        else:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, temp_list.rmtype),(eq, temp_list.rmtype)]})

            if zimkateg:
                temp_list.zikatnr = zimkateg.zikatnr
    r_list_data.clear()

    if not all_room:

        for temp_list in query(temp_list_data):

            r_list = query(r_list_data, filters=(lambda r_list: r_list.rcode == temp_list.rcode), first=True)

            if not r_list:
                r_list = R_list()
                r_list_data.append(r_list)

                r_list.rcode = temp_list.rcode
    else:

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == cm_gastno)).order_by(Guest_pr._recid).all():
            r_list = R_list()
            r_list_data.append(r_list)

            r_list.rcode = guest_pr.code
    count_rmcateg()

    # if currcode.lower()  == ("*").lower() :
    if currcode.lower()  == "*" :
        custom_pushall_avail()
    else:
        rmtype_pushall_avail()
    done = True

    return generate_output()