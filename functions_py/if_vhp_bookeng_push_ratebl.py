#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rulita, 18/08/2025
# Recompile program 
# ticket: A96F0C
# Rd, 13/11/2025
# CM Push rate
#--------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Ratecode, Zimkateg, Waehrung, Arrangement, Queasy, Kontline, Res_line, Htparam, Guest, Guest_pr, Artikel, Zimmer, Reservation, Segment

temp_list_data, Temp_list = create_model("Temp_list", {"rcode":string, "rmtype":string, "zikatnr":int})

def if_vhp_bookeng_push_ratebl(inp_str:string, start_counter:int, pushpax:bool, fdate:date, tdate:date, adult:int, child:int, becode:int, temp_list_data:[Temp_list]):

    prepare_cache ([Queasy, Kontline, Res_line, Htparam, Guest, Guest_pr, Artikel, Zimmer, Reservation])

    done = False
    push_rate_list_data = []
    curr_rate:Decimal = to_decimal("0.0")
    curr_recid:int = 0
    curr_scode:string = ""
    curr_bezeich:string = ""
    temp_zikat:string = ""
    starttime:int = 0
    curr_date:date = None
    ankunft:date = None
    ci_date:date = None
    co_date:date = None
    datum:date = None
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    grpcode:string = ""
    global_occ:bool = False
    splited_occ:bool = False
    q_recid:int = 0
    vhp_limited:bool = False
    do_it:bool = False
    exist:bool = False
    cat_flag:bool = False
    pushall:bool = False
    re_calculaterate:bool = False
    createrate:bool = False
    cm_gastno:int = 0
    counter:int = 0
    counter170:int = 0
    i:int = 0
    occ_room:int = 0
    end_date:date = None
    max_occ:int = 0
    rm_occ:int = 0
    rm_ooo:int = 0
    room:int = 0
    maxroom:int = 0
    def_rate:string = ""
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    tax_included:bool = False
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    strl:string = ""
    strll:string = ""
    loopi:int = 0
    loopj:int = 0
    currtype:string = ""
    frmtype:int = 0
    n:int = 0
    m:int = 0
    k:int = 0
    j:int = 0
    ratecode = zimkateg = waehrung = arrangement = queasy = kontline = res_line = htparam = guest = guest_pr = artikel = zimmer = reservation = segment = None

    dynarate_list = r_list = s_list = rate_list = push_rate_list = change_room = temp_list = grp_type = bratecode = t_zimkateg = t_waehrung = t_arrangement = t_queasy = t_queasy170 = bqueasy = t_qsy18 = t_qsy145 = t_qsy152 = q_curr = t_qsy171 = t_qsy170 = grtype = qsy = currqsy = kline = bqsy170 = qsy170 = qsy159 = bresline = None

    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":string, "dynacode":string})
    r_list_data, R_list = create_model("R_list", {"rcode":string})
    s_list_data, S_list = create_model("S_list", {"static_code":string})
    rate_list_data, Rate_list = create_model("Rate_list", {"startperiode":date, "endperiode":date, "zikatnr":int, "counter":int, "rcode":string, "bezeich":string, "pax":int, "child":int, "rmrate":Decimal, "flag":bool, "currency":string, "scode":string}, {"flag": True})
    push_rate_list_data, Push_rate_list = create_model_like(Rate_list, {"str_date1":string, "str_date2":string})
    change_room_data, Change_room = create_model("Change_room", {"datum":date, "zikatnr":int, "occ":int})
    grp_type_data, Grp_type = create_model("Grp_type", {"gtype":string, "rm_type":int})
    bratecode_data, Bratecode = create_model_like(Ratecode)
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    t_waehrung_data, T_waehrung = create_model_like(Waehrung)
    t_arrangement_data, T_arrangement = create_model_like(Arrangement)
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_queasy170_data, T_queasy170 = create_model_like(Queasy)
    bqueasy_data, Bqueasy = create_model_like(Queasy)
    t_qsy18_data, T_qsy18 = create_model_like(Queasy)
    t_qsy145_data, T_qsy145 = create_model_like(Queasy)
    t_qsy152_data, T_qsy152 = create_model_like(Queasy)
    q_curr_data, Q_curr = create_model_like(Queasy)
    t_qsy171_data, T_qsy171 = create_model_like(Queasy)
    t_qsy170_data, T_qsy170 = create_model_like(Queasy, {"rec_id":int})
    grtype_data, Grtype = create_model_like(Grp_type)

    Qsy = create_buffer("Qsy",Queasy)
    Currqsy = create_buffer("Currqsy",Queasy)
    Kline = create_buffer("Kline",Kontline)
    Bqsy170 = create_buffer("Bqsy170",Queasy)
    Qsy170 = create_buffer("Qsy170",Queasy)
    Qsy159 = create_buffer("Qsy159",Queasy)
    Bresline = create_buffer("Bresline",Res_line)


    db_session = local_storage.db_session
    inp_str = inp_str.strip()

    def generate_output():
        nonlocal done, push_rate_list_data, curr_rate, curr_recid, curr_scode, curr_bezeich, temp_zikat, starttime, curr_date, ankunft, ci_date, co_date, datum, tokcounter, iftask, mestoken, mesvalue, grpcode, global_occ, splited_occ, q_recid, vhp_limited, do_it, exist, cat_flag, pushall, re_calculaterate, createrate, cm_gastno, counter, counter170, i, occ_room, end_date, max_occ, rm_occ, rm_ooo, room, maxroom, def_rate, w_day, wd_array, tax_included, serv, vat, strl, strll, loopi, loopj, currtype, frmtype, n, m, k, j, ratecode, zimkateg, waehrung, arrangement, queasy, kontline, res_line, htparam, guest, guest_pr, artikel, zimmer, reservation, segment
        nonlocal inp_str, start_counter, pushpax, fdate, tdate, adult, child, becode
        nonlocal qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline


        nonlocal dynarate_list, r_list, s_list, rate_list, push_rate_list, change_room, temp_list, grp_type, bratecode, t_zimkateg, t_waehrung, t_arrangement, t_queasy, t_queasy170, bqueasy, t_qsy18, t_qsy145, t_qsy152, q_curr, t_qsy171, t_qsy170, grtype, qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline
        nonlocal dynarate_list_data, r_list_data, s_list_data, rate_list_data, push_rate_list_data, change_room_data, grp_type_data, bratecode_data, t_zimkateg_data, t_waehrung_data, t_arrangement_data, t_queasy_data, t_queasy170_data, bqueasy_data, t_qsy18_data, t_qsy145_data, t_qsy152_data, q_curr_data, t_qsy171_data, t_qsy170_data, grtype_data

        return {"done": done, "push-rate-list": push_rate_list_data}

    def create_queasy170(q_date:date, q_zikatnr:int, q_pax:int, q_child:int, q_rmrate:Decimal, q_rcode:string, q_scode:string, q_currency:string):

        nonlocal done, push_rate_list_data, curr_rate, curr_recid, curr_scode, curr_bezeich, temp_zikat, starttime, curr_date, ankunft, ci_date, co_date, datum, tokcounter, iftask, mestoken, mesvalue, grpcode, global_occ, splited_occ, q_recid, vhp_limited, do_it, exist, cat_flag, pushall, re_calculaterate, createrate, cm_gastno, counter, counter170, i, occ_room, end_date, max_occ, rm_occ, rm_ooo, room, maxroom, def_rate, w_day, wd_array, tax_included, serv, vat, strl, strll, loopi, loopj, currtype, frmtype, n, m, k, j, ratecode, zimkateg, waehrung, arrangement, queasy, kontline, res_line, htparam, guest, guest_pr, artikel, zimmer, reservation, segment
        nonlocal inp_str, start_counter, pushpax, fdate, tdate, adult, child, becode
        nonlocal qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline


        nonlocal dynarate_list, r_list, s_list, rate_list, push_rate_list, change_room, temp_list, grp_type, bratecode, t_zimkateg, t_waehrung, t_arrangement, t_queasy, t_queasy170, bqueasy, t_qsy18, t_qsy145, t_qsy152, q_curr, t_qsy171, t_qsy170, grtype, qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline
        nonlocal dynarate_list_data, r_list_data, s_list_data, rate_list_data, push_rate_list_data, change_room_data, grp_type_data, bratecode_data, t_zimkateg_data, t_waehrung_data, t_arrangement_data, t_queasy_data, t_queasy170_data, bqueasy_data, t_qsy18_data, t_qsy145_data, t_qsy152_data, q_curr_data, t_qsy171_data, t_qsy170_data, grtype_data


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 170
        queasy.date1 = q_date
        queasy.number1 = q_zikatnr
        queasy.number2 = q_pax
        queasy.number3 = q_child
        queasy.deci1 =  to_decimal(q_rmrate)
        queasy.char1 = q_rcode
        queasy.char2 = q_scode
        queasy.char3 = q_currency
        queasy.betriebsnr = becode


    def count_availability(curr_date:date, i_typ:int):

        nonlocal done, push_rate_list_data, curr_rate, curr_recid, curr_scode, curr_bezeich, temp_zikat, starttime, ankunft, ci_date, co_date, datum, tokcounter, iftask, mestoken, mesvalue, grpcode, global_occ, splited_occ, q_recid, exist, cat_flag, pushall, re_calculaterate, createrate, cm_gastno, counter, counter170, i, occ_room, end_date, max_occ, rm_occ, rm_ooo, room, maxroom, def_rate, w_day, wd_array, tax_included, serv, vat, strl, strll, loopi, loopj, currtype, frmtype, n, m, k, j, ratecode, zimkateg, waehrung, arrangement, queasy, kontline, res_line, htparam, guest, guest_pr, artikel, zimmer, reservation, segment
        nonlocal inp_str, start_counter, pushpax, fdate, tdate, adult, child, becode
        nonlocal qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline


        nonlocal dynarate_list, r_list, s_list, rate_list, push_rate_list, change_room, temp_list, grp_type, bratecode, t_zimkateg, t_waehrung, t_arrangement, t_queasy, t_queasy170, bqueasy, t_qsy18, t_qsy145, t_qsy152, q_curr, t_qsy171, t_qsy170, grtype, qsy, currqsy, kline, bqsy170, qsy170, qsy159, bresline
        nonlocal dynarate_list_data, r_list_data, s_list_data, rate_list_data, push_rate_list_data, change_room_data, grp_type_data, bratecode_data, t_zimkateg_data, t_waehrung_data, t_arrangement_data, t_queasy_data, t_queasy170_data, bqueasy_data, t_qsy18_data, t_qsy145_data, t_qsy152_data, q_curr_data, t_qsy171_data, t_qsy170_data, grtype_data

        rm_occ = 0
        vhp_limited:bool = False
        do_it:bool = False
        rm_allot:int = 0

        def generate_inner_output():
            return (rm_occ)

        rm_occ = 0
        rm_allot = 0
        grpcode = ""


        grtype_data.clear()

        if not splited_occ:

            if global_occ:

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                    rm_allot = rm_allot + kontline.zimmeranz

                bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
                while None != bresline :
                    do_it = True

                    if bresline.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        rm_occ = rm_occ + bresline.zimmeranz

                    kline = get_cache (Kontline, {"kontignr": [(eq, bresline.kontignr)],"kontstatus": [(eq, 1)]})

                    if kline:

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                        if kontline:
                            do_it = True

                            if bresline.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                rm_allot = rm_allot - bresline.zimmeranz

                    curr_recid = bresline._recid
                    bresline = db_session.query(Bresline).filter(
                             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= curr_date) & (Bresline.abreise > curr_date) & (Bresline.kontignr >= 0) & (Bresline.l_zuordnung[inc_value(2)] == 0) & (Bresline._recid > curr_recid)).first()
                rm_occ = rm_occ + rm_allot

            if not global_occ:

                if cat_flag:

                    t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.typ == i_typ), first=True)

                    if t_zimkateg:
                        i_typ = t_zimkateg.zikatnr

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (Kontline.zikatnr == i_typ) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                    rm_allot = rm_allot + kontline.zimmeranz

                bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"zikatnr": [(eq, i_typ)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
                while None != bresline:
                    do_it = True

                    if bresline.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                        if reservation:

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0
                        else:
                            do_it = False

                    if do_it:
                        rm_occ = rm_occ + bresline.zimmeranz

                    kline = get_cache (Kontline, {"kontignr": [(eq, bresline.kontignr)],"kontstatus": [(eq, 1)]})

                    if kline:

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                        if kontline:
                            do_it = True

                            if bresline.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                                if reservation:

                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                    do_it = None != segment and segment.vip_level == 0
                                else:
                                    do_it = False

                            if do_it:
                                rm_allot = rm_allot - bresline.zimmeranz

                    curr_recid = bresline._recid
                    bresline = db_session.query(Bresline).filter(
                             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.zikatnr == i_typ) & (Bresline.ankunft <= curr_date) & (Bresline.abreise > curr_date) & (Bresline.kontignr >= 0) & (Bresline.l_zuordnung[inc_value(2)] == 0) & (Bresline._recid > curr_recid)).first()
                rm_occ = rm_occ + rm_allot

        if splited_occ:

            if cat_flag:

                t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.typ == i_typ), first=True)

                if t_zimkateg:
                    i_typ = t_zimkateg.zikatnr

            grp_type = query(grp_type_data, filters=(lambda grp_type: grp_type.rm_type == i_typ), first=True)

            if grp_type:
                grpcode = grp_type.gtype

                for grp_type in query(grp_type_data, filters=(lambda grp_type: grp_type.gtype.lower()  == (grpcode).lower())):
                    grtype = Grtype()
                    grtype_data.append(grtype)

                    buffer_copy(grp_type, grtype)

            if global_occ:

                kontline_obj_list = {}
                for kontline in db_session.query(Kontline).filter(
                         (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                    grtype = query(grtype_data, (lambda grtype: grtype.rm_type == kontline.zikatnr), first=True)
                    if not grtype:
                        continue

                    if kontline_obj_list.get(kontline._recid):
                        continue
                    else:
                        kontline_obj_list[kontline._recid] = True


                    rm_allot = rm_allot + kontline.zimmeranz

                bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
                while None != bresline :

                    grtype = query(grtype_data, filters=(lambda grtype: grtype.rm_type == bresline.zikatnr), first=True)

                    if grtype:
                        do_it = True

                        if bresline.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rm_occ = rm_occ + bresline.zimmeranz

                        kline = get_cache (Kontline, {"kontignr": [(eq, bresline.kontignr)],"kontstatus": [(eq, 1)]})

                        if kline:

                            kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                            if kontline:
                                do_it = True

                                if bresline.zinr != "":

                                    zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                                    do_it = zimmer.sleeping

                                if do_it and vhp_limited:

                                    reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                    do_it = None != segment and segment.vip_level == 0

                                if do_it:
                                    rm_allot = rm_allot - bresline.zimmeranz

                    curr_recid = bresline._recid
                    bresline = db_session.query(Bresline).filter(
                             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= curr_date) & (Bresline.abreise > curr_date) & (Bresline.kontignr >= 0) & (Bresline.l_zuordnung[inc_value(2)] == 0) & (Bresline._recid > curr_recid)).first()
                rm_occ = rm_occ + rm_allot

            if not global_occ:

                if cat_flag:

                    t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.typ == i_typ), first=True)

                    if t_zimkateg:
                        i_typ = t_zimkateg.zikatnr

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (Kontline.zikatnr == i_typ) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                    rm_allot = rm_allot + kontline.zimmeranz

                bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"zikatnr": [(eq, i_typ)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
                while None != bresline:
                    do_it = True

                    if bresline.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                        if reservation:

                            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                            do_it = None != segment and segment.vip_level == 0
                        else:
                            do_it = False

                    if do_it:
                        rm_occ = rm_occ + bresline.zimmeranz

                    kline = get_cache (Kontline, {"kontignr": [(eq, bresline.kontignr)],"kontstatus": [(eq, 1)]})

                    if kline:

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                        if kontline:
                            do_it = True

                            if bresline.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, bresline.resnr)]})

                                if reservation:

                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                    do_it = None != segment and segment.vip_level == 0
                                else:
                                    do_it = False

                            if do_it:
                                rm_allot = rm_allot - bresline.zimmeranz

                    curr_recid = bresline._recid
                    bresline = db_session.query(Bresline).filter(
                             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.zikatnr == i_typ) & (Bresline.ankunft <= curr_date) & (Bresline.abreise > curr_date) & (Bresline.kontignr >= 0) & (Bresline.l_zuordnung[inc_value(2)] == 0) & (Bresline._recid > curr_recid)).first()
                rm_occ = rm_occ + rm_allot

        return generate_inner_output()


    starttime = get_current_time_in_seconds()
    bratecode_data.clear()
    t_zimkateg_data.clear()
    t_waehrung_data.clear()
    t_arrangement_data.clear()
    bqueasy_data.clear()
    t_qsy18_data.clear()
    t_qsy145_data.clear()
    t_qsy152_data.clear()
    t_qsy170_data.clear()
    t_qsy171_data.clear()
    q_curr_data.clear()
    t_queasy_data.clear()
    dynarate_list_data.clear()
    grp_type_data.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1364)],"bezeichnung": [(ne, "not used")]})

    if htparam and htparam.fchar.strip() != "":
        for loopi in range(1,num_entries(htparam.fchar, ";")  + 1) :
            strl = entry(loopi - 1, htparam.fchar, ";")


            for loopj in range(1,num_entries(strl, ",")  + 1) :
                strll = entry(loopj - 1, strl, ",")

                if loopj == 1:
                    currtype = substring(strll, 0, 1)
                    frmtype = to_int(substring(strll, 1, 1))


                grp_type = Grp_type()
                grp_type_data.append(grp_type)

                grp_type.gtype = currtype

                if loopj == 1:
                    grp_type.rm_type = frmtype


                else:
                    grp_type.rm_type = to_int(strll)

    waehrung = db_session.query(Waehrung).first()
    while None != waehrung:
        t_waehrung = T_waehrung()
        t_waehrung_data.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

        curr_recid = waehrung._recid
        waehrung = db_session.query(Waehrung).filter(Waehrung._recid > curr_recid).first()

    arrangement = db_session.query(Arrangement).first()
    while None != arrangement:
        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        curr_recid = arrangement._recid
        arrangement = db_session.query(Arrangement).filter(Arrangement._recid > curr_recid).first()

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.active)).first()
    while None != zimkateg:
        t_zimkateg = T_zimkateg()
        t_zimkateg_data.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

        curr_recid = zimkateg._recid
        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.active) & (Zimkateg._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 2)]})
    while None != queasy:
        bqueasy = Bqueasy()
        bqueasy_data.append(bqueasy)

        buffer_copy(queasy, bqueasy)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 18)]})
    while None != queasy:
        t_qsy18 = T_qsy18()
        t_qsy18_data.append(t_qsy18)

        buffer_copy(queasy, t_qsy18)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 18) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})
    while None != queasy:
        t_qsy152 = T_qsy152()
        t_qsy152_data.append(t_qsy152)

        buffer_copy(queasy, t_qsy152)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 152) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 164)]})
    while None != queasy:
        q_curr = Q_curr()
        q_curr_data.append(q_curr)

        buffer_copy(queasy, q_curr)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 164) & (Queasy._recid > curr_recid)).first()
    adult = 2
    done = False
    maxroom = 0
    def_rate = ""

    if num_entries(inp_str, "=") >= 2:
        pushall = logical(entry(0, inp_str, "="))
        re_calculaterate = logical(entry(1, inp_str, "="))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

    if htparam:
        tax_included = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam:

        if htparam.flogical:

            return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:

        guest = get_cache (Guest, {"gastnr": [(eq, queasy.number2)]})

        if guest:

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

            if guest_pr:
                cm_gastno = guest.gastnr
            else:

                return generate_output()

    t_qsy152 = query(t_qsy152_data, first=True)

    if t_qsy152:
        cat_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    if fdate == ci_date:
        ankunft = ci_date
    else:
        ankunft = fdate + timedelta(days=2)

    for temp_list in query(temp_list_data):

        if cat_flag:

            t_qsy152 = query(t_qsy152_data, filters=(lambda t_qsy152: t_qsy152.char1 == temp_list.rmtype), first=True)

            if t_qsy152:
                temp_list.zikatnr = t_qsy152.number1
        else:

            t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.kurzbez == temp_list.rmtype), first=True)

            if t_zimkateg:
                temp_list.zikatnr = t_zimkateg.zikatnr
    r_list_data.clear()
    s_list_data.clear()

    temp_list = query(temp_list_data, first=True)

    if temp_list:

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

    queasy = get_cache (Queasy, {"key": [(eq, 170)],"betriebsnr": [(gt, 0)]})

    if queasy:

        for qsy159 in db_session.query(Qsy159).filter(
                 (Qsy159.key == 159) & (Qsy159.number2 == 0)).order_by(Qsy159._recid).all():

            qsy170 = get_cache (Queasy, {"key": [(eq, 170)],"betriebsnr": [(eq, qsy159.number1)]})
            while None != qsy170:

                qsy = get_cache (Queasy, {"_recid": [(eq, qsy170._recid)]})

                if qsy:
                    db_session.delete(qsy)
                    pass

                curr_recid = qsy170._recid
                qsy170 = db_session.query(Qsy170).filter(
                         (Qsy170.key == 170) & (Qsy170.betriebsnr == qsy159.number1) & (Qsy170._recid > curr_recid)).first()

        qsy170 = get_cache (Queasy, {"key": [(eq, 170)],"betriebsnr": [(eq, 0)]})
        while None != qsy170:

            qsy = get_cache (Queasy, {"_recid": [(eq, qsy170._recid)]})

            if qsy:
                db_session.delete(qsy)
                pass

            curr_recid = qsy170._recid
            qsy170 = db_session.query(Qsy170).filter(
                     (Qsy170.key == 170) & (Qsy170.betriebsnr == 0) & (Qsy170._recid > curr_recid)).first()
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 170)],"betriebsnr": [(eq, 0)]})
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.betriebsnr = becode


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & (Queasy.betriebsnr == 0) & (Queasy._recid > curr_recid)).first()

    if pushall:

        currqsy = get_cache (Queasy, {"key": [(eq, 170)],"betriebsnr": [(eq, becode)]})
        while None != currqsy:
            db_session.delete(currqsy)
            pass

            curr_recid = currqsy._recid
            currqsy = db_session.query(Currqsy).filter(
                     (Currqsy.key == 170) & (Currqsy.betriebsnr == becode) & (Currqsy._recid > curr_recid)).first()

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(ge, fdate),(le, tdate)],"betriebsnr": [(eq, becode)]})
        while None != queasy:
            t_qsy171 = T_qsy171()
            t_qsy171_data.append(t_qsy171)

            buffer_copy(queasy, t_qsy171)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

        queasy = get_cache (Queasy, {"key": [(eq, 145)],"date1": [(ge, fdate),(le, tdate)]})
        while None != queasy:
            t_qsy145 = T_qsy145()
            t_qsy145_data.append(t_qsy145)

            buffer_copy(queasy, t_qsy145)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 145) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy._recid > curr_recid)).first()
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(lt, fdate - 2)],"betriebsnr": [(eq, becode)]})

        if queasy:

            currqsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(lt, fdate - 2)],"betriebsnr": [(eq, becode)]})
            while None != currqsy:
                db_session.delete(currqsy)
                pass

                curr_recid = currqsy._recid
                currqsy = db_session.query(Currqsy).filter(
                         (Currqsy.key == 170) & (Currqsy.date1 < fdate - timedelta(days=2)) & (Currqsy.betriebsnr == becode) & (Currqsy._recid > curr_recid)).first()

        qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, tdate)],"betriebsnr": [(eq, becode)]})

        if not qsy:
            createrate = True

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, tdate)],"betriebsnr": [(eq, becode)]})
            while None != queasy:
                t_qsy171 = T_qsy171()
                t_qsy171_data.append(t_qsy171)

                buffer_copy(queasy, t_qsy171)

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.date1 == tdate) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

            queasy = get_cache (Queasy, {"key": [(eq, 145)],"date1": [(eq, tdate)]})
            while None != queasy:
                t_qsy145 = T_qsy145()
                t_qsy145_data.append(t_qsy145)

                buffer_copy(queasy, t_qsy145)

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 145) & (Queasy.date1 == tdate) & (Queasy._recid > curr_recid)).first()

    for r_list in query(r_list_data):
        bqueasy = query(bqueasy_data, (lambda bqueasy: bqueasy.char1 == r_list.rcode), first=True)
        if not bqueasy:
            continue


        if bqueasy.logi2:

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.code == r_list.rcode)).order_by(Ratecode._recid).all():
                dynarate_list = Dynarate_list()
                dynarate_list_data.append(dynarate_list)

                dynarate_list.dynacode = ratecode.code
                iftask = ratecode.char1[4]


                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "CN":
                        dynarate_list.counter = to_int(mesvalue)
                    elif mestoken == "RT":
                        dynarate_list.rmtype = mesvalue
                    elif mestoken == "WD":
                        dynarate_list.w_day = to_int(mesvalue)
                    elif mestoken == "FR":
                        dynarate_list.fr_room = to_int(mesvalue)
                    elif mestoken == "TR":
                        dynarate_list.to_room = to_int(mesvalue)
                    elif mestoken == "D1":
                        dynarate_list.days1 = to_int(mesvalue)
                    elif mestoken == "D2":
                        dynarate_list.days2 = to_int(mesvalue)
                    elif mestoken == "RC":
                        dynarate_list.rcode = mesvalue

                if dynarate_list.to_room > maxroom:
                    def_rate = dynarate_list.rcode
                    maxroom = dynarate_list.to_room

    htparam = get_cache (Htparam, {"paramnr": [(eq, 439)]})

    grp_type = query(grp_type_data, first=True)

    if grp_type:
        splited_occ = True

    dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
    global_occ = None != dynarate_list and htparam.finteger == 1

    if global_occ:

        for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
            dynarate_list_data.remove(dynarate_list)

    else:

        for dynarate_list in query(dynarate_list_data):

            t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.kurzbez == dynarate_list.rmtype), first=True)

            if cat_flag:

                temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.typ), first=True)

                if not temp_list:
                    dynarate_list_data.remove(dynarate_list)
            else:

                temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.zikatnr), first=True)

                if not temp_list:
                    dynarate_list_data.remove(dynarate_list)

    dynarate_list = query(dynarate_list_data, first=True)

    if dynarate_list:

        for dynarate_list in query(dynarate_list_data):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.static_code == dynarate_list.rcode), first=True)

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.static_code = dynarate_list.rcode

        for s_list in query(s_list_data):

            if cat_flag:

                for ratecode in db_session.query(Ratecode).filter(
                         (Ratecode.code == s_list.static_code) & (Ratecode.startperiode <= tdate) & (Ratecode.endperiode >= fdate) & (Ratecode.erwachs > 0)).order_by(Ratecode._recid).all():

                    t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == ratecode.zikatnr), first=True)

                    temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.typ), first=True)

                    if temp_list:
                        bratecode = Bratecode()
                        bratecode_data.append(bratecode)

                        buffer_copy(ratecode, bratecode)
            else:

                for ratecode in db_session.query(Ratecode).filter(
                         (Ratecode.code == s_list.static_code) & (Ratecode.startperiode <= tdate) & (Ratecode.endperiode >= fdate) & (Ratecode.erwachs > 0)).order_by(Ratecode._recid).all():

                    temp_list = query(temp_list_data, filters=(lambda temp_list: temp_list.zikatnr == ratecode.zikatnr), first=True)

                    if temp_list:
                        bratecode = Bratecode()
                        bratecode_data.append(bratecode)

                        buffer_copy(ratecode, bratecode)

    if pushall or start_counter == 0 or re_calculaterate or createrate:
        loopi = 0
        loopj = 0

        if pushpax:
            n = 1 
            k == 0


        else:
            n = adult 
            m == adult 
            k == 0 
            j == 0

        if createrate:

            # t_qsy171 = query(t_qsy171_data, filters=(lambda t_qsy171: t_qsy171.char1 == "" and t_qsy171.date1 == tdate), first=True)
            t_qsy171_list = [    t_qsy171
                            for t_qsy171 in t_qsy171_data
                            if t_qsy171.char1 == "" and t_qsy171.date1 == tdate
                        ]
        else:
            # t_qsy171 = query(t_qsy171_data, filters=(lambda t_qsy171: t_qsy171.char1 == ""), first=True)
            t_qsy171_list = [    t_qsy171
                            for t_qsy171 in t_qsy171_data
                            if t_qsy171.char1 == "" 
                        ]
        for t_qsy171 in t_qsy171_list:
        # while None != t_qsy171:
            w_day = wd_array[get_weekday(t_qsy171.date1) - 1]

            for r_list in query(r_list_data):
                bqueasy = query(bqueasy_data, (lambda bqueasy: bqueasy.char1 == r_list.rcode), first=True)
                if not bqueasy:
                    continue

                do_it = True

                if cat_flag:

                    t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.typ == t_qsy171.number1), first=True)
                else:

                    t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == t_qsy171.number1), first=True)

                queasy = get_cache (Queasy, {"key": [(eq, 170)],"char1": [(eq, r_list.rcode)],"date1": [(eq, t_qsy171.date1)],"number1": [(eq, t_qsy171.number1)],"betriebsnr": [(eq, becode)]})

                if queasy:
                    do_it = False

                elif bqueasy.number3 > 0 and bqueasy.number3 > (ankunft - timedelta(days=ci_date)):
                    do_it = False

                elif bqueasy.deci3 > 0 and bqueasy.deci3 < (ankunft - timedelta(days=ci_date)):
                    do_it = False

                if not do_it:
                    pass

                elif not bqueasy.logi2:

                    if pushpax:

                        for ratecode in db_session.query(Ratecode).filter(
                                     (Ratecode.code == r_list.rcode) & (Ratecode.zikatnr == t_zimkateg.zikatnr) & (Ratecode.startperiode <= t_qsy171.date1) & (Ratecode.endperiode >= t_qsy171.date1) & (Ratecode.erwachs > 0)).order_by(Ratecode.erwachs.desc()).all():
                            m = ratecode.erwachs
                            j = ratecode.kind1


                            break
                    for loopi in range(n,m + 1) :

                        ratecode = get_cache (Ratecode, {"code": [(eq, r_list.rcode)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"startperiode": [(le, t_qsy171.date1)],"endperiode": [(ge, t_qsy171.date1)],"wday": [(eq, w_day)],"kind1": [(eq, child)],"erwachs": [(eq, loopi)]})

                        if not ratecode:

                            ratecode = get_cache (Ratecode, {"code": [(eq, r_list.rcode)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"startperiode": [(le, t_qsy171.date1)],"endperiode": [(ge, t_qsy171.date1)],"wday": [(eq, 0)],"kind1": [(eq, child)],"erwachs": [(eq, loopi)]})

                        if ratecode:

                            t_arrangement = query(t_arrangement_data, filters=(lambda t_arrangement: t_arrangement.argtnr == ratecode.argtnr), first=True)

                            if t_arrangement:

                                artikel = get_cache (Artikel, {"artnr": [(eq, t_arrangement.argt_artikelnr)]})

                                if artikel:
                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, t_qsy171.date1, artikel.service_code, artikel.mwst_code))
                            counter = counter + 1
                            rate_list = Rate_list()
                            rate_list_data.append(rate_list)

                            rate_list.zikatnr = t_qsy171.number1
                            rate_list.rcode = ratecode.code
                            rate_list.startperiode = t_qsy171.date1
                            rate_list.endperiode = t_qsy171.date1
                            rate_list.counter = counter
                            rate_list.pax = ratecode.erwachs
                            rate_list.child = ratecode.kind1

                            if ratecode.erwachs != 0:
                                rate_list.rmrate =  to_decimal(ratecode.zipreis)
                            else:
                                rate_list.rmrate =  to_decimal(ratecode.ch1preis)

                            if not tax_included:
                                rate_list.rmrate = to_decimal(round(to_decimal(rate_list.rmrate * (1 + serv + vat)) , 0))

                            t_qsy18 = query(t_qsy18_data, filters=(lambda t_qsy18: t_qsy18.number1 == ratecode.marknr), first=True)

                            if t_qsy18:

                                t_waehrung = query(t_waehrung_data, filters=(lambda t_waehrung: t_waehrung.wabkurz == t_qsy18.char3), first=True)

                                if t_waehrung:

                                    q_curr = query(q_curr_data, filters=(lambda q_curr: q_curr.char1 == t_waehrung.wabkurz and q_curr.number1 == becode), first=True)

                                    if q_curr:
                                        rate_list.currency = q_curr.char2
                                    else:
                                        rate_list.currency = "IDR"
                                else:
                                    rate_list.currency = "IDR"

                            if cat_flag:

                                t_qsy152 = query(t_qsy152_data, filters=(lambda t_qsy152: t_qsy152.number1 == t_qsy171.number1), first=True)

                                if t_qsy152:
                                    rate_list.bezeich = t_qsy152.char1
                            else:
                                rate_list.bezeich = t_zimkateg.kurzbez

                elif bqueasy.logi2:
                    curr_scode = ""
                    occ_room = 0


                    occ_room = count_availability(t_qsy171.date1, t_qsy171.number1)

                    if not global_occ:

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)

                        if not dynarate_list:

                            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)
                    else:

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode), first=True)

                        if not dynarate_list:

                            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode), first=True)

                    if dynarate_list:

                        if not global_occ:

                            t_qsy145 = query(t_qsy145_data, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == t_zimkateg.zikatnr and t_qsy145.deci1 == dynarate_list.w_day and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                            if not t_qsy145:

                                t_qsy145 = query(t_qsy145_data, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == t_zimkateg.zikatnr and t_qsy145.deci1 == 0 and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)
                        else:

                            t_qsy145 = query(t_qsy145_data, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == 0 and t_qsy145.deci1 == dynarate_list.w_day and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                            if not t_qsy145:

                                t_qsy145 = query(t_qsy145_data, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == 0 and t_qsy145.deci1 == 0 and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                        if t_qsy145:
                            curr_scode = t_qsy145.char3
                        else:
                            curr_scode = dynarate_list.rcode

                        if pushpax:

                            for bratecode in query(bratecode_data, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.erwachs > 0), sort_by=[("erwachs",True)]):
                                m = bratecode.erwachs
                                j = bratecode.kind1


                                break
                        for loopi in range(n,m + 1) :

                            bratecode = query(bratecode_data, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.erwachs == loopi and bratecode.kind1 == child and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.wday == w_day), first=True)

                            if not bratecode:

                                bratecode = query(bratecode_data, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.erwachs == loopi and bratecode.kind1 == child and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.wday == 0), first=True)

                            if bratecode:

                                t_arrangement = query(t_arrangement_data, filters=(lambda t_arrangement: t_arrangement.argtnr == bratecode.argtnr), first=True)

                                if t_arrangement:

                                    artikel = get_cache (Artikel, {"artnr": [(eq, t_arrangement.argt_artikelnr)]})

                                    if artikel:
                                        serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, t_qsy171.date1, artikel.service_code, artikel.mwst_code))
                                counter = counter + 1
                                rate_list = Rate_list()
                                rate_list_data.append(rate_list)

                                rate_list.zikatnr = t_qsy171.number1
                                rate_list.rcode = r_list.rcode
                                rate_list.startperiode = t_qsy171.date1
                                rate_list.endperiode = t_qsy171.date1
                                rate_list.counter = counter
                                rate_list.scode = curr_scode
                                rate_list.pax = bratecode.erwachs
                                rate_list.child = bratecode.kind1

                                if bratecode.erwachs != 0:
                                    rate_list.rmrate =  to_decimal(bratecode.zipreis)
                                else:
                                    rate_list.rmrate =  to_decimal(bratecode.ch1preis)

                                if not tax_included:
                                    rate_list.rmrate = to_decimal(round(to_decimal(rate_list.rmrate * (1 + serv + vat)) , 0))

                                t_qsy18 = query(t_qsy18_data, filters=(lambda t_qsy18: t_qsy18.number1 == bratecode.marknr), first=True)

                                t_waehrung = query(t_waehrung_data, filters=(lambda t_waehrung: t_waehrung.wabkurz == t_qsy18.char3), first=True)

                                if t_waehrung:

                                    q_curr = query(q_curr_data, filters=(lambda q_curr: q_curr.char1 == t_waehrung.wabkurz and q_curr.number1 == becode), first=True)

                                    if q_curr:
                                        rate_list.currency = q_curr.char2
                                    else:
                                        rate_list.currency = "IDR"
                                else:
                                    rate_list.currency = "IDR"

                                if cat_flag:

                                    t_qsy152 = query(t_qsy152_data, filters=(lambda t_qsy152: t_qsy152.number1 == t_qsy171.number1), first=True)
                                    rate_list.bezeich = t_qsy152.char1
                                else:
                                    rate_list.bezeich = t_zimkateg.kurzbez

            # if createrate:
            #     t_qsy171 = query(t_qsy171_data, filters=(lambda t_qsy171: t_qsy171.char1 == "" and t_qsy171.date1 == tdate), next=True)
            # else:

            #     t_qsy171 = query(t_qsy171_data, filters=(lambda t_qsy171: t_qsy171.char1 == ""), next=True)

        rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.startperiode >= fdate and rate_list.endperiode <= tdate), first=True)
        while None != rate_list:

            t_qsy170 = query(t_qsy170_data, filters=(lambda t_qsy170: t_qsy170.char1 == rate_list.rcode and t_qsy170.number1 == rate_list.zikatnr and t_qsy170.date1 == rate_list.startperiode and t_qsy170.number2 == rate_list.pax and t_qsy170.number3 == rate_list.child and t_qsy170.betriebsnr == becode), first=True)

            if t_qsy170 and t_qsy170.deci1 == rate_list.rmrate:

                if t_qsy170.logi1:
                    rate_list.flag = True
                else:
                    rate_list.flag = False

            elif t_qsy170 and t_qsy170.deci1 != rate_list.rmrate:

                qsy = get_cache (Queasy, {"_recid": [(eq, t_qsy170._recid)]})

                if qsy:
                    qsy.logi1 = True
                    qsy.deci1 =  to_decimal(rate_list.rmrate)
                    qsy.char2 = rate_list.scode


                    pass
                    pass

            elif not t_qsy170:
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                t_queasy.key = 170
                t_queasy.date1 = rate_list.startperiode
                t_queasy.number1 = rate_list.zikatnr
                t_queasy.number2 = rate_list.pax
                t_queasy.number3 = rate_list.child
                t_queasy.deci1 =  to_decimal(rate_list.rmrate)
                t_queasy.char1 = rate_list.rcode
                t_queasy.char2 = rate_list.scode
                t_queasy.char3 = rate_list.currency
                t_queasy.betriebsnr = becode

                if createrate:
                    t_queasy.logi1 = False
                    t_queasy.logi2 = False
                    t_queasy.logi3 = True

            rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.startperiode >= fdate and rate_list.endperiode <= tdate), next=True)

        if createrate:
            pass
        else:

            for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.startperiode >= fdate and rate_list.endperiode <= tdate and rate_list.flag)):
                push_rate_list = Push_rate_list()
                push_rate_list_data.append(push_rate_list)

                buffer_copy(rate_list, push_rate_list)


    for t_queasy in query(t_queasy_data):
        bqsy170 = Queasy()
        db_session.add(bqsy170)

        buffer_copy(t_queasy, bqsy170)

    if pushpax:

        queasy = get_cache (Queasy, {"key": [(eq, 170)],"number2": [(eq, 0)],"betriebsnr": [(eq, becode)]})

        if queasy:

            bqsy170 = get_cache (Queasy, {"key": [(eq, 170)],"number2": [(eq, 0)],"betriebsnr": [(eq, becode)]})
            while None != bqsy170:
                db_session.delete(bqsy170)
                pass

                curr_recid = bqsy170._recid
                bqsy170 = db_session.query(Bqsy170).filter(
                         (Bqsy170.key == 170) & (Bqsy170.number2 == 0) & (Bqsy170.betriebsnr == becode) & (Bqsy170._recid > curr_recid)).first()
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 170)],"number2": [(le, 1)],"betriebsnr": [(eq, becode)]})

        if queasy:

            bqsy170 = get_cache (Queasy, {"key": [(eq, 170)],"number2": [(le, 1)],"betriebsnr": [(eq, becode)]})
            while None != bqsy170:
                db_session.delete(bqsy170)
                pass

                curr_recid = bqsy170._recid
                bqsy170 = db_session.query(Bqsy170).filter(
                         (Bqsy170.key == 170) & (Bqsy170.number2 <= 1) & (Bqsy170.betriebsnr == becode) & (Bqsy170._recid > curr_recid)).first()

    if not pushall or not createrate:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & (Queasy.logi2) & (Queasy.betriebsnr == becode)).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = qsy.logi2
                qsy.logi2 = False


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & (Queasy.logi2) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & (Queasy.logi1) & (Queasy.betriebsnr == becode)).first()
        while None != queasy:
            w_day = wd_array[get_weekday(queasy.date1) - 1]
            do_it = True

            if cat_flag:

                t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.typ == queasy.number1), first=True)
            else:

                t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == queasy.number1), first=True)

            bqueasy = query(bqueasy_data, filters=(lambda bqueasy: bqueasy.char1 == queasy.char1), first=True)

            if not bqueasy:
                do_it = False

            elif bqueasy and bqueasy.number3 > 0 and bqueasy.number3 > (ankunft - timedelta(days=ci_date)):
                do_it = False

            elif bqueasy and bqueasy.deci3 > 0 and bqueasy.deci3 < (ankunft - timedelta(days=ci_date)):
                do_it = False

            if not do_it:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi1 = False
                    pass
                    pass

            elif not bqueasy.logi2:

                ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"erwachs": [(eq, queasy.number2)],"kind1": [(eq, queasy.number3)],"startperiode": [(le, queasy.date1)],"endperiode": [(ge, queasy.date1)],"wday": [(eq, w_day)]})

                if not ratecode:

                    ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"erwachs": [(eq, queasy.number2)],"kind1": [(eq, queasy.number3)],"startperiode": [(le, queasy.date1)],"endperiode": [(ge, queasy.date1)],"wday": [(eq, 0)]})

                if ratecode:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:

                        if ratecode.erwachs != 0:

                            if ratecode.zipreis != qsy.deci1:
                                qsy.deci1 =  to_decimal(ratecode.zipreis)
                                qsy.logi3 = True
                                qsy.logi1 = False


                            else:
                                qsy.logi1 = False

                        elif ratecode.kind1 != 0:

                            if ratecode.ch1preis != qsy.deci1:
                                qsy.deci1 =  to_decimal(ratecode.ch1preis)
                                qsy.logi3 = True
                                qsy.logi1 = False


                            else:
                                qsy.logi1 = False


                        pass
                        pass

            elif bqueasy.logi2:
                occ_room = 0
                curr_scode = ""


                occ_room = count_availability(queasy.date1, queasy.number1)

                if not global_occ:

                    dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == queasy.char1 and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)

                    if not dynarate_list:

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == queasy.char1 and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)
                else:

                    dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == queasy.char1), first=True)

                    if not dynarate_list:

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == queasy.char1), first=True)

                if dynarate_list:

                    if not global_occ:

                        qsy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, queasy.char1)],"char2": [(eq, dynarate_list.rcode)],"number1": [(eq, t_zimkateg.zikatnr)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, queasy.date1)]})

                        if not qsy:

                            qsy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, queasy.char1)],"char2": [(eq, dynarate_list.rcode)],"number1": [(eq, t_zimkateg.zikatnr)],"deci1": [(eq, 0)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, queasy.date1)]})
                    else:

                        qsy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, queasy.char1)],"char2": [(eq, dynarate_list.rcode)],"number1": [(eq, 0)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, queasy.date1)]})

                        if not qsy:

                            qsy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, queasy.char1)],"char2": [(eq, dynarate_list.rcode)],"number1": [(eq, 0)],"deci1": [(eq, 0)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, queasy.date1)]})

                    if qsy:
                        curr_scode = qsy.char3
                    else:
                        curr_scode = dynarate_list.rcode

                    bratecode = query(bratecode_data, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.kind1 == queasy.number3 and bratecode.erwach == queasy.number2 and bratecode.startperiode <= queasy.date1 and bratecode.endperiode >= queasy.date1 and bratecode.wday == w_day), first=True)

                    if not bratecode:

                        bratecode = query(bratecode_data, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.kind1 == queasy.number3 and bratecode.erwach == queasy.number2 and bratecode.startperiode <= queasy.date1 and bratecode.endperiode >= queasy.date1 and bratecode.wday == 0), first=True)

                    if bratecode:

                        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                        if qsy:

                            if bratecode.erwachs != 0:

                                if bratecode.zipreis != qsy.deci1:
                                    qsy.deci1 =  to_decimal(bratecode.zipreis)
                                    qsy.logi3 = True
                                    qsy.logi1 = False
                                    qsy.char2 = bratecode.code


                                else:
                                    qsy.logi1 = False

                            elif bratecode.kind1 != 0:

                                if bratecode.ch1preis != qsy.deci1:
                                    qsy.deci1 =  to_decimal(bratecode.zipreis)
                                    qsy.logi3 = True
                                    qsy.logi1 = False
                                    qsy.char2 = bratecode.code


                                else:
                                    qsy.logi1 = False


                            pass
                            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & (Queasy.logi1) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

    if pushpax:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 170) & (Queasy.logi3) & (Queasy.betriebsnr == becode)).order_by(Queasy._recid).all():

            qsy = get_cache (Queasy, {"key": [(eq, 170)],"number1": [(eq, queasy.number1)],"char1": [(eq, queasy.char1)],"date1": [(eq, queasy.date1)],"logi3": [(eq, False)],"betriebsnr": [(eq, becode)]})

            if qsy:

                currqsy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                if currqsy:
                    currqsy.logi3 = True


                    pass
                    pass

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 170) & (Queasy.logi3) & (Queasy.betriebsnr == becode)).first()
    while None != queasy:

        if cat_flag:
            t_qsy152 = query(t_qsy152_data, filters=(lambda t_qsy152: t_qsy152.number1 == queasy.number1), first=True)

            if t_qsy152:
                curr_bezeich = t_qsy152.char1
        else:
            t_zimkateg = query(t_zimkateg_data, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == queasy.number1), first=True)

            if t_zimkateg:
                curr_bezeich = t_zimkateg.kurzbez
        push_rate_list = Push_rate_list()
        push_rate_list_data.append(push_rate_list)

        push_rate_list.rcode = queasy.char1
        push_rate_list.startperiode = queasy.date1
        push_rate_list.endperiode = queasy.date1
        push_rate_list.zikatnr = queasy.number1
        push_rate_list.pax = queasy.number2
        push_rate_list.child = queasy.number3
        push_rate_list.rmrate =  to_decimal(queasy.deci1)
        push_rate_list.currency = queasy.char3
        push_rate_list.bezeich = curr_bezeich

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & (Queasy.logi3) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()
    done = True

    return generate_output()