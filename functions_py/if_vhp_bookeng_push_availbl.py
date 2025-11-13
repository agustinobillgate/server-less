#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 12/11/2025
# CM: tidak termasuk tentative booking
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Ratecode, Res_line, Htparam, Guest, Guest_pr, Zimkateg, Kontline, Zimmer, Outorder, Reservation, Segment, Paramtext

temp_list_data, Temp_list = create_model("Temp_list", {"rcode":string, "rmtype":string, "zikatnr":int})

def if_vhp_bookeng_push_availbl(pushrate:bool, inp_str:string, fdate:date, tdate:date, becode:int, temp_list_data:[Temp_list]):

    prepare_cache ([Queasy, Ratecode, Res_line, Htparam, Guest, Guest_pr, Zimkateg, Kontline, Zimmer, Reservation, Paramtext])

    done = False
    push_allot_list_data = []
    curr_rate:Decimal = to_decimal("0.0")
    curr_recid:int = 0
    curr_rcode:string = ""
    curr_bezeich:string = ""
    curr_anz:int = 0
    starttime:int = 0
    curr_date:date = None
    ankunft:date = None
    ci_date:date = None
    date_110:date = None
    datum:date = None
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    rline_origcode:string = ""
    global_occ:bool = False
    vhp_limited:bool = False
    do_it:bool = False
    zero_flag:bool = False
    availbratecode:bool = False
    cat_flag:bool = False
    pushall:bool = False
    re_calculaterate:bool = False
    change_allot:bool = False
    all_room:bool = True
    allotment:bool = False
    bedsetup:bool = False
    avail_rmcat:bool = False
    cm_gastno:int = 0
    z_nr:int = 0
    counter_avail:int = 0
    i:int = 0
    occ_room:int = 0
    push_quantity:int = 0
    end_date:date = None
    start_date:date = None
    valid_date:date = None
    catnr:int = 0
    rm_occ:int = 0
    rm_ooo:int = 0
    rm_allot:int = 0
    res_allot:int = 0
    room:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    statnr:int = 0
    queasy = ratecode = res_line = htparam = guest = guest_pr = zimkateg = kontline = zimmer = outorder = reservation = segment = paramtext = None

    rmcat_list = r_list = push_allot_list = buff = q_list = change_room = temp_list = allotment = rmlist = bqueasy = q_curr = qsy = qsy159 = qsy_allot = qsy2 = bratecode = bresline = kline = rqsy = da_qsy = None

    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "typ":int, "sleeping":bool}, {"sleeping": True})
    r_list_data, R_list = create_model("R_list", {"rcode":string})
    # push_allot_list_data, Push_allot_list = create_model("Push_allot_list", {"startperiode":date, "endperiode":date, "zikatnr":int, "counter":int, "rcode":string, "bezeich":string, "qty":int, "flag":bool, "str_date1":string, "str_date2":string, "minlos":int, "maxlos":int, "statnr":int, "ota":string, "bsetup":string, "rmtype":string}, {"flag": True})
    
    #bedsetup dan ota dihapus dari model Push_allot_list
    push_allot_list_data, Push_allot_list = create_model("Push_allot_list", {"startperiode":date, "endperiode":date, "zikatnr":int, 
                                                                             "counter":int, "rcode":string, "bezeich":string, "qty":int, 
                                                                             "flag":bool, "str_date1":string, "str_date2":string, "minlos":int, 
                                                                             "maxlos":int, "statnr":int, "rmtype":string}, {"flag": True, "str_date1":"YYYY-MM-DD", "str_date2":"YYYY-MM-DD"})

    q_list_data, Q_list = create_model("Q_list", {"rcode":string, "scode":string, "dcode":string, "zikatnr":int, "allot_flag":bool})
    change_room_data, Change_room = create_model("Change_room", {"datum":date, "zikatnr":int, "occ":int})
    allotment_data, allotment = create_model("allotment", {"datum":date, "zikatnr":int, "res_allot":int, "allot":int, "ruecktage":int})
    rmlist_data, Rmlist = create_model("Rmlist", {"typ":int, "rmcode":string})

    Buff = Push_allot_list
    buff_data = push_allot_list_data

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Q_curr = create_buffer("Q_curr",Queasy)
    Qsy = create_buffer("Qsy",Queasy)
    Qsy159 = create_buffer("Qsy159",Queasy)
    Qsy_allot = create_buffer("Qsy_allot",Queasy)
    Qsy2 = create_buffer("Qsy2",Queasy)
    Bratecode = create_buffer("Bratecode",Ratecode)
    Bresline = create_buffer("Bresline",Res_line)
    Kline = create_buffer("Kline",Kontline)
    Rqsy = create_buffer("Rqsy",Queasy)
    Da_qsy = create_buffer("Da_qsy",Queasy)


    db_session = local_storage.db_session

    inp_str = inp_str.strip()

    def generate_output():
        nonlocal done, push_allot_list_data, curr_rate, curr_recid, curr_rcode, curr_bezeich, curr_anz, starttime, curr_date, ankunft, ci_date, date_110, datum, tokcounter, iftask, mestoken, mesvalue, rline_origcode, global_occ, vhp_limited, do_it, zero_flag, availbratecode, cat_flag, pushall, re_calculaterate, change_allot, all_room, allotment, bedsetup, avail_rmcat, cm_gastno, z_nr, counter_avail, i, occ_room, push_quantity, end_date, start_date, valid_date, catnr, rm_occ, rm_ooo, rm_allot, res_allot, room, w_day, wd_array, statnr, queasy, ratecode, res_line, htparam, guest, guest_pr, zimkateg, kontline, zimmer, outorder, reservation, segment, paramtext
        nonlocal pushrate, inp_str, fdate, tdate, becode
        nonlocal buff, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy


        nonlocal rmcat_list, r_list, push_allot_list, buff, q_list, change_room, temp_list, allotment, rmlist, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy
        nonlocal rmcat_list_data, r_list_data, push_allot_list_data, q_list_data, change_room_data, allotment_data, rmlist_data

        return {"done": done, "push-allot-list": push_allot_list_data}

    def find_date(curr_date:date):

        nonlocal done, push_allot_list_data, curr_rate, curr_recid, curr_rcode, curr_bezeich, curr_anz, starttime, ankunft, ci_date, date_110, tokcounter, iftask, mestoken, mesvalue, rline_origcode, global_occ, vhp_limited, do_it, zero_flag, availbratecode, cat_flag, pushall, re_calculaterate, change_allot, all_room, allotment, bedsetup, avail_rmcat, cm_gastno, z_nr, counter_avail, i, occ_room, push_quantity, end_date, start_date, valid_date, catnr, rm_occ, rm_ooo, rm_allot, res_allot, room, w_day, wd_array, statnr, queasy, ratecode, res_line, htparam, guest, guest_pr, zimkateg, kontline, zimmer, outorder, reservation, segment, paramtext
        nonlocal pushrate, inp_str, fdate, tdate, becode
        nonlocal buff, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy


        nonlocal rmcat_list, r_list, push_allot_list, buff, q_list, change_room, temp_list, allotment, rmlist, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy
        nonlocal rmcat_list_data, r_list_data, push_allot_list_data, q_list_data, change_room_data, allotment_data, rmlist_data

        curr_anz = 0
        mm:int = 0
        yy:int = 0
        datum:date = None
        end_month:int = 0
        prev_day:int = 0

        def generate_inner_output():
            return (curr_anz)

        mm = get_month(curr_date)
        yy = get_year(curr_date)

        if mm == 1:
            prev_day = 0
        else:
            for i in range(1,mm - 1 + 1) :
                datum = date_mdy(i + 1, 1, yy)
                datum = datum - timedelta(days=1)
                prev_day = prev_day + get_day(datum)


        curr_anz = prev_day + get_day(curr_date)

        return generate_inner_output()


    def count_rmcateg():

        nonlocal done, push_allot_list_data, curr_rate, curr_recid, curr_rcode, curr_bezeich, curr_anz, starttime, curr_date, ankunft, ci_date, date_110, datum, tokcounter, iftask, mestoken, mesvalue, rline_origcode, global_occ, vhp_limited, do_it, zero_flag, availbratecode, cat_flag, pushall, re_calculaterate, change_allot, all_room, allotment, bedsetup, avail_rmcat, cm_gastno, z_nr, counter_avail, i, occ_room, push_quantity, end_date, start_date, valid_date, catnr, rm_occ, rm_ooo, rm_allot, res_allot, room, w_day, wd_array, statnr, queasy, ratecode, res_line, htparam, guest, guest_pr, zimkateg, kontline, zimmer, outorder, reservation, segment, paramtext
        nonlocal pushrate, inp_str, fdate, tdate, becode
        nonlocal buff, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy


        nonlocal rmcat_list, r_list, push_allot_list, buff, q_list, change_room, temp_list, allotment, rmlist, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy
        nonlocal rmcat_list_data, r_list_data, push_allot_list_data, q_list_data, change_room_data, allotment_data, rmlist_data

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

        nonlocal done, push_allot_list_data, curr_rate, curr_recid, curr_rcode, curr_bezeich, curr_anz, starttime, ankunft, ci_date, date_110, datum, tokcounter, iftask, mestoken, mesvalue, rline_origcode, global_occ, zero_flag, availbratecode, cat_flag, pushall, re_calculaterate, change_allot, all_room, allotment, bedsetup, avail_rmcat, cm_gastno, z_nr, counter_avail, i, occ_room, push_quantity, end_date, start_date, valid_date, catnr, rm_occ, rm_ooo, rm_allot, res_allot, room, w_day, wd_array, statnr, queasy, ratecode, res_line, htparam, guest, guest_pr, zimkateg, kontline, zimmer, outorder, reservation, segment, paramtext
        nonlocal pushrate, inp_str, fdate, tdate, becode
        nonlocal buff, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy


        nonlocal rmcat_list, r_list, push_allot_list, buff, q_list, change_room, temp_list, allotment, rmlist, bqueasy, q_curr, qsy, qsy159, qsy_allot, qsy2, bratecode, bresline, kline, rqsy, da_qsy
        nonlocal rmcat_list_data, r_list_data, push_allot_list_data, q_list_data, change_room_data, allotment_data, rmlist_data

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
        for kontline.zimmeranz, kontline.ankunft, kontline.abreise, kontline.ruecktage, kontline.betriebsnr, kontline._recid, kontline.kontcode, zimkateg.typ, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg._recid in db_session.query(Kontline.zimmeranz, Kontline.ankunft, Kontline.abreise, Kontline.ruecktage, Kontline.betriebsnr, Kontline._recid, Kontline.kontcode, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Kontline.zikatnr)).filter(
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

            bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
            while None != bresline :

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, bresline.zikatnr)],"typ": [(eq, i_typ)]})

                if zimkateg:
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

                        if allotment and curr_date >= (ci_date + timedelta(days=kline.ruecktage)):

                            kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
                        else:

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
            else:

                bresline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(le, 6),(ne, 3),(ne, 4),(ne, 12),(ne, 11),(ne, 13)],"zikatnr": [(eq, i_typ)],"ankunft": [(le, curr_date)],"abreise": [(gt, curr_date)],"kontignr": [(ge, 0)],"l_zuordnung[2]": [(eq, 0)]})
                while None != bresline:
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

                        if allotment and curr_date >= (ci_date + timedelta(days=kline.ruecktage)):

                            kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
                        else:

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
                             (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.zikatnr == i_typ) & (Bresline.ankunft <= curr_date) & (Bresline.abreise > curr_date) & (Bresline.kontignr >= 0) & (Bresline.l_zuordnung[inc_value(2)] == 0) & (Bresline._recid > curr_recid)).first()

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


    starttime = get_current_time_in_seconds()
    allotment_data.clear()
    done = False

    if num_entries(inp_str, "=") >= 2:
        pushall = logical(entry(0, inp_str, "="))
        re_calculaterate = logical(entry(1, inp_str, "="))

    if num_entries(inp_str, "=") >= 3:
        allotment = logical(entry(2, inp_str, "="))

    if num_entries(inp_str, "=") >= 4:
        bedsetup = logical(entry(3, inp_str, "="))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    date_110 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam.flogical:

        if date_110 < get_current_date():

            return generate_output()

    temp_list = query(temp_list_data, first=True)

    if temp_list:
        all_room = False

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:

        guest = get_cache (Guest, {"gastnr": [(eq, queasy.number2)]})
        if not guest:
            return generate_output()
        
        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

        if guest_pr:
            cm_gastno = guest.gastnr
        else:
            return generate_output()
    else:

        return generate_output()
    
    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        avail_rmcat = True
        cat_flag = True

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 152)).order_by(Queasy._recid).all():
            rmlist = Rmlist()
            rmlist_data.append(rmlist)

            rmlist.typ = queasy.number1


            rmlist.rmcode = queasy.char1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 439)]})
    global_occ = htparam.finteger == 1

    if bedsetup :
        cat_flag = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if fdate == ci_date:
        ankunft = ci_date
    else:
        ankunft = fdate + timedelta(days=2)

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

    queasy = get_cache (Queasy, {"key": [(eq, 171)],"betriebsnr": [(gt, 0)]})

    if queasy:

        for qsy159 in db_session.query(Qsy159).filter(
                     (Qsy159.key == 159) & (Qsy159.number2 == 0)).order_by(Qsy159._recid).all():

            q_curr = get_cache (Queasy, {"key": [(eq, 171)],"betriebsnr": [(eq, qsy159.number1)]})
            while None != q_curr:

                qsy = get_cache (Queasy, {"_recid": [(eq, q_curr._recid)]})

                if qsy:
                    db_session.delete(qsy)
                    pass

                curr_recid = q_curr._recid
                q_curr = db_session.query(Q_curr).filter(
                             (Q_curr.key == 171) & (Q_curr.betriebsnr == qsy159.number1) & (Q_curr._recid > curr_recid)).first()

        q_curr = get_cache (Queasy, {"key": [(eq, 171)],"betriebsnr": [(eq, 0)]})
        while None != q_curr:

            qsy = get_cache (Queasy, {"_recid": [(eq, q_curr._recid)]})

            if qsy:
                db_session.delete(qsy)
                pass

            curr_recid = q_curr._recid
            q_curr = db_session.query(Q_curr).filter(
                         (Q_curr.key == 171) & (Q_curr.betriebsnr == 0) & (Q_curr._recid > curr_recid)).first()
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"betriebsnr": [(eq, 0)]})
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.betriebsnr = becode


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.betriebsnr == 0) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 174)],"number3": [(gt, 0)]})
    while None != queasy :

        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

        if qsy:
            db_session.delete(qsy)
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 174) & (Queasy.number3 > 0) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 175)],"number3": [(gt, 0)]})
    while None != queasy :

        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

        if qsy:
            db_session.delete(qsy)
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & (Queasy.number3 > 0) & (Queasy._recid > curr_recid)).first()

    valid_date = tdate
    if pushall:

        for temp_list in query(temp_list_data):

            if cat_flag:

                zimkateg = get_cache (Zimkateg, {"typ": [(eq, temp_list.zikatnr)]})

                if zimkateg:
                    z_nr = zimkateg.zikatnr


            else:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, temp_list.zikatnr)]})

                if zimkateg:
                    z_nr = zimkateg.zikatnr


            valid_date = tdate

            for bratecode in db_session.query(Bratecode).filter(
                         (Bratecode.zikatnr == z_nr) & (Bratecode.code == temp_list.rcode) & (Bratecode.endperiode >= fdate)).order_by(Bratecode.endperiode.desc()).all():

                if bratecode.endperiode > valid_date:
                    valid_date = bratecode.endperiode


                break

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")],"betriebsnr": [(eq, becode)]})
        while None != queasy:
            db_session.delete(queasy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()
        for curr_date in date_range(fdate,tdate) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(ne, "")],"date1": [(eq, curr_date)],"betriebsnr": [(eq, becode)]})
            while None != queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.number2 = 0
                    qsy.logi1 = False
                    qsy.logi2 = False
                    qsy.logi3 = True


                    pass
                    pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 171) & (Queasy.char1 != "") & (Queasy.date1 == curr_date) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

        kontline_obj_list = {}
        kontline = Kontline()
        zimkateg = Zimkateg()
        for kontline.zimmeranz, kontline.ankunft, kontline.abreise, kontline.ruecktage, kontline.betriebsnr, \
                kontline._recid, kontline.kontcode, zimkateg.typ, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg._recid \
                in db_session.query(Kontline.zimmeranz, Kontline.ankunft, Kontline.abreise, Kontline.ruecktage, Kontline.betriebsnr, \
                                    Kontline._recid, Kontline.kontcode, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg._recid)\
                .join(Zimkateg,(Zimkateg.zikatnr == Kontline.zikatnr))\
                .filter(
                     (Kontline.kontstatus == 1) & (Kontline.ankunft <= valid_date) & (Kontline.abreise >= fdate)).order_by(Kontline._recid).all():
            
            if kontline_obj_list.get(kontline._recid):
                continue
            else:
                kontline_obj_list[kontline._recid] = True

            if allotment and kontline.betriebsnr == 0:
                do_it = True

            elif not allotment and kontline.betriebsnr == 1:
                do_it = True

            if do_it:

                if cat_flag:
                    catnr = zimkateg.typ
                else:
                    catnr = zimkateg.zikatnr

                if kontline.ankunft <= fdate:
                    start_date = fdate
                else:
                    start_date = kontline.ankunft

                if kontline.abreise > valid_date:
                    end_date = valid_date
                else:
                    end_date = kontline.abreise
                for datum in date_range(start_date,end_date) :

                    allotment = query(allotment_data, filters=(lambda allotment: allotment.zikatnr == catnr and allotment.datum == datum), first=True)

                    if not allotment:
                        allotment = allotment()
                        allotment_data.append(allotment)

                        allotment.zikatnr = catnr
                        allotment.datum = datum
                        allotment.allot = kontline.zimmeranz
                        allotment.ruecktage = kontline.ruecktage


                    else:
                        allotment.allot = allotment.allot + kontline.zimmeranz
            do_it = False
        for curr_date in date_range(fdate,valid_date) :

            for rmcat_list in query(rmcat_list_data):
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 171
                queasy.number1 = rmcat_list.zikatnr
                queasy.date1 = curr_date
                queasy.logi1 = False
                queasy.logi2 = False
                queasy.logi3 = False
                queasy.char1 = ""
                queasy.betriebsnr = becode

                allotment = query(allotment_data, filters=(lambda allotment: allotment.datum == curr_date and allotment.zikatnr == rmcat_list.zikatnr), first=True)

                if allotment and curr_date >= (ci_date + timedelta(days=allotment.ruecktage)):
                    queasy.number2 = allotment.allot

        outorder_obj_list = {}
        for outorder, zimmer, zimkateg in db_session.query(Outorder, Zimmer, Zimkateg).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).filter(
                     (Outorder.betriebsnr <= 1) & ((Outorder.gespstart >= fdate) | (Outorder.gespende >= fdate))).order_by(Outorder._recid).all():
            if outorder_obj_list.get(outorder._recid):
                continue
            else:
                outorder_obj_list[outorder._recid] = True

            if cat_flag:
                catnr = zimkateg.typ
            else:
                catnr = zimkateg.zikatnr
            for datum in date_range(outorder.gespstart,outorder.gespende) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"number1": [(eq, catnr)],"date1": [(eq, datum)],"char1": [(eq, "")],"betriebsnr": [(eq, becode)]})

                if queasy:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.number3 = qsy.number3 + 1


                        pass
                        pass

        res_line_obj_list = {}
        res_line = Res_line()
        zimkateg = Zimkateg()
        for res_line.zinr, res_line.resnr, res_line.abreise, res_line.ankunft, res_line.kontignr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line._recid, res_line.zikatnr, zimkateg.typ, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.resnr, Res_line.abreise, Res_line.ankunft, Res_line.kontignr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line._recid, Res_line.zikatnr, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= valid_date) & (Res_line.abreise >= fdate)).order_by(Res_line._recid).all():
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

                if res_line.ankunft == res_line.abreise:
                    end_date = res_line.abreise
                else:
                    end_date = res_line.abreise - timedelta(days=1)

                if cat_flag:
                    catnr = zimkateg.typ
                else:
                    catnr = zimkateg.zikatnr

                if res_line.ankunft <= fdate:
                    start_date = fdate
                else:
                    start_date = res_line.ankunft

                if end_date >= valid_date:
                    end_date = valid_date
                for datum in date_range(start_date,end_date) :
                    res_allot = 0

                    if res_line.kontignr > 0:

                        kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                        if kline:

                            if allotment and datum >= (ci_date + timedelta(days=kontline.ruecktage)):

                                kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})
                            else:

                                kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                            if kontline:
                                res_allot = res_line.zimmeranz

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"number1": [(eq, catnr)],"date1": [(eq, datum)],"char1": [(eq, "")],"betriebsnr": [(eq, becode)]})

                    if queasy:

                        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                        if qsy:
                            qsy.number2 = qsy.number2 + res_line.zimmeranz - res_allot


                            pass
                            pass

                if matches(res_line.zimmer_wunsch,r"*$OrigCode$*"):
                    rline_origcode = ""
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(iftask, 0, 10) == ("$OrigCode$") :
                            rline_origcode = substring(iftask, 10)
                            break

                    if rline_origcode != "":
                        for datum in date_range(start_date,end_date) :

                            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, catnr)],"char1": [(eq, rline_origcode)],"betriebsnr": [(eq, becode)]})

                            if queasy:

                                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                                if qsy:
                                    qsy.number2 = qsy.number2 + res_line.zimmeranz


                                    pass
                                    pass
        for curr_date in date_range(fdate,tdate) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"betriebsnr": [(eq, becode)]})
            while None != queasy:
                queasy.logi3 = True


                pass
                pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 171) & (Queasy.date1 == curr_date) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

    if not pushall:

        # queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(lt, fdate - 2)],"betriebsnr": [(eq, becode)]})
        queasys = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 < fdate - timedelta(days=2)) & (Queasy.betriebsnr == becode)).all()
        # while None != queasy:
        for queasy in queasys:
            # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
            qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).first()

            if qsy:
                db_session.delete(qsy)
                pass

            # curr_recid = queasy._recid
            # queasy = db_session.query(Queasy).filter(
            #              (Queasy.key == 171) & (Queasy.date1 < fdate - timedelta(days=2)) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

        # queasy = db_session.query(Queasy).filter(
        #              (Queasy.key == 171) & (Queasy.logi2) & (Queasy.betriebsnr == becode)).first()
        queasys = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.logi2) & (Queasy.betriebsnr == becode)).all()
        #
        for queasy in queasys:

            # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
            qsy = db_session.query(Queasy).filter(Queasy._recid == queasy._recid).first()

            if qsy:
                qsy.logi1 = qsy.logi2
                qsy.logi2 = False


            #     pass
            #     pass

            # curr_recid = queasy._recid
            # queasy = db_session.query(Queasy).filter(
            #              (Queasy.key == 171) & (Queasy.logi2) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()


        # queasy = db_session.query(Queasy).filter(
        #              (Queasy.key == 171) & (Queasy.logi1) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode)).first()
        # while None != queasy:
        queasys = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.logi1) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode)).all() 
        for queasy in queasys:
            rm_occ = 0
            rm_ooo = 0
            rm_allot = 0


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

            if pushrate:

                for r_list in query(r_list_data):

                    if global_occ:

                        bqueasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, queasy.date1)],"char1": [(eq, r_list.rcode)],"logi1": [(eq, False)],"logi2": [(eq, False)],"betriebsnr": [(eq, becode)]})
                        while None != bqueasy:

                            qsy2 = db_session.query(Qsy2).filter(
                                         (Qsy2.key == 2) & (Qsy2.char1 == bqueasy.char1) & (Qsy2.logi2)).first()

                            if qsy2:

                                qsy = get_cache (Queasy, {"_recid": [(eq, bqueasy._recid)]})

                                if qsy:
                                    qsy.logi1 = True
                                    qsy.logi2 = False


                                    pass
                                    pass

                            curr_recid = bqueasy._recid
                            bqueasy = db_session.query(Bqueasy).filter(
                                         (Bqueasy.key == 170) & (Bqueasy.date1 == queasy.date1) & (Bqueasy.char1 == r_list.rcode) & (Bqueasy.logi1 == False) & (Bqueasy.logi2 == False) & (Bqueasy.betriebsnr == becode) & (Bqueasy._recid > curr_recid)).first()
                    else:

                        bqueasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"char1": [(eq, r_list.rcode)],"logi1": [(eq, False)],"logi2": [(eq, False)],"betriebsnr": [(eq, becode)]})
                        while None != bqueasy:

                            qsy2 = db_session.query(Qsy2).filter(
                                         (Qsy2.key == 2) & (Qsy2.char1 == bqueasy.char1) & (Qsy2.logi2)).first()

                            if qsy2:

                                qsy = get_cache (Queasy, {"_recid": [(eq, bqueasy._recid)]})

                                if qsy:
                                    qsy.logi1 = True
                                    qsy.logi2 = False


                                    pass
                                    pass

                            curr_recid = bqueasy._recid
                            bqueasy = db_session.query(Bqueasy).filter(
                                         (Bqueasy.key == 170) & (Bqueasy.date1 == queasy.date1) & (Bqueasy.number1 == queasy.number1) & (Bqueasy.char1 == r_list.rcode) & (Bqueasy.logi1 == False) & (Bqueasy.logi2 == False) & (Bqueasy.betriebsnr == becode) & (Bqueasy._recid > curr_recid)).first()

            # curr_recid = queasy._recid
            # queasy = db_session.query(Queasy).filter(
            #              (Queasy.key == 171) & (Queasy.logi1) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()


        # queasy = db_session.query(Queasy).filter(
        #              (Queasy.key == 171) & (Queasy.char1 != "") & (Queasy.logi1) & (Queasy.betriebsnr == becode)).first()
        # while None != queasy:
        queasys = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.char1 != "") & (Queasy.logi1) & (Queasy.betriebsnr == becode)).all()
        for queasy in queasys:
            occ_room = 0

            if cat_flag:

                res_line_obj_list = {}
                res_line = Res_line()
                zimkateg = Zimkateg()
                for res_line.zinr, res_line.resnr, res_line.abreise, res_line.ankunft, res_line.kontignr, res_line.zimmeranz, res_line.zimmer_wunsch, res_line._recid, res_line.zikatnr, zimkateg.typ, zimkateg.zikatnr, zimkateg.kurzbez, zimkateg._recid in db_session.query(Res_line.zinr, Res_line.resnr, Res_line.abreise, Res_line.ankunft, Res_line.kontignr, Res_line.zimmeranz, Res_line.zimmer_wunsch, Res_line._recid, Res_line.zikatnr, Zimkateg.typ, Zimkateg.zikatnr, Zimkateg.kurzbez, Zimkateg._recid).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr) & (Zimkateg.typ == queasy.number1)).filter(
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

                            if substring(iftask, 0, 10) == ("$OrigCode$") :
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

                            if substring(iftask, 0, 10) == ("$OrigCode$") :
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

            curr_recid = queasy._recid
            # queasy = db_session.query(Queasy).filter(
            #              (Queasy.key == 171) & (Queasy.char1 != "") & (Queasy.logi1) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

        if tdate != None:

            # queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, tdate)],"betriebsnr": [(eq, becode)]})
            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & (Queasy.date1 == tdate) & (Queasy.betriebsnr == becode)).first()

            if not queasy:

                for rmcat_list in query(rmcat_list_data):
                    rm_occ, rm_ooo, rm_allot = count_availability(tdate, rmcat_list.zikatnr)
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 171
                    queasy.number1 = rmcat_list.zikatnr
                    queasy.number3 = rm_ooo
                    queasy.date1 = tdate
                    queasy.logi1 = False
                    queasy.logi2 = False
                    queasy.logi3 = True
                    queasy.char1 = ""
                    queasy.betriebsnr = becode

                    if allotment:
                        queasy.number2 = rm_occ + rm_allot
                    else:
                        queasy.number2 = rm_occ

    for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 171) & (Queasy.char1 == "") & (Queasy.logi3) & (Queasy.betriebsnr == becode)).order_by(Queasy._recid).all():

        bqueasy = db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 171) & (Bqueasy.betriebsnr == becode) & (Bqueasy.char1 != "") & (Bqueasy.date1 == queasy.date1) & (Bqueasy.number1 == queasy.number1) & not_ (Bqueasy.logi3)).first()
        while None != bqueasy:
            pass
            bqueasy.logi3 = True
            pass
            pass

            curr_recid = bqueasy._recid
            bqueasy = db_session.query(Bqueasy).filter(
                         (Bqueasy.key == 171) & (Bqueasy.betriebsnr == becode) & (Bqueasy.char1 != "") & (Bqueasy.date1 == queasy.date1) & (Bqueasy.number1 == queasy.number1) & not_ (Bqueasy.logi3) & (Bqueasy._recid > curr_recid)).first()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 171) & (Queasy.logi3) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode)).first()
    while None != queasy:

        for r_list in query(r_list_data):

            qsy_allot = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, r_list.rcode)],
                                            "date1": [(eq, queasy.date1)],
                                            "betriebsnr": [(eq, becode)],
                                            "number1": [(eq, queasy.number1)],
                                            "number3": [(ne, 0)]})

            if not qsy_allot:

                qsy2 = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, r_list.rcode)]})

                if qsy2:
                    statnr = 0
                    curr_anz = 0

                    rqsy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, r_list.rcode)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)]})

                    if rqsy:

                        if to_int(entry(0, rqsy.char2, ";")) == 1:
                            statnr = 1

                        elif to_int(entry(1, rqsy.char2, ";")) == 1 and to_int(entry(2, rqsy.char2, ";")) == 0:
                            statnr = 2

                        elif to_int(entry(2, rqsy.char2, ";")) == 1 and to_int(entry(1, rqsy.char2, ";")) == 0:
                            statnr = 3

                        elif to_int(entry(1, rqsy.char2, ";")) == 1 and to_int(entry(2, rqsy.char2, ";")) == 1:
                            statnr = 4

                    rqsy = get_cache (Queasy, {"key": [(eq, 175)],"char1": [(eq, r_list.rcode)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)]})

                    if rqsy:

                        if rqsy.char2  == ("CLOSE")  and rqsy.number2 == 0:
                            statnr = 0

                        if rqsy.char2  == ("CTA")  and rqsy.number2 == 0:
                            statnr = 5

                        if rqsy.char2  == ("CTD")  and rqsy.number2 == 0:
                            statnr = 6

                        if rqsy.char2  == ("CLOSE")  and rqsy.number2 == 1:
                            statnr = 1

                        if rqsy.char2  == ("CTA")  and rqsy.number2 == 1:
                            statnr = 2

                        if rqsy.char2  == ("CTD")  and rqsy.number2 == 1:
                            statnr = 3
                    counter_avail = counter_avail + 1
                    push_allot_list = Push_allot_list()
                    push_allot_list_data.append(push_allot_list)

                    push_allot_list.startperiode = queasy.date1
                    push_allot_list.endperiode = queasy.date1
                    push_allot_list.rcode = r_list.rcode
                    push_allot_list.zikatnr = queasy.number1
                    push_allot_list.counter = counter_avail
                    push_allot_list.minlos = qsy2.number2
                    push_allot_list.maxlos = qsy2.deci2
                    push_allot_list.statnr = statnr


                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)
                    push_allot_list.qty = rmcat_list.anzahl - queasy.number2 - queasy.number3

                    if cat_flag:

                        qsy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, queasy.number1)]})

                        if qsy:
                            push_allot_list.bezeich = qsy.char1
                            push_allot_list.rmtype = qsy.char1

                    elif not bedsetup and not avail_rmcat:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                        if zimkateg:
                            push_allot_list.bezeich = zimkateg.kurzbez
                            push_allot_list.rmtype = zimkateg.kurzbez

                    elif bedsetup and avail_rmcat:

                        rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)

                        if rmcat_list:

                            rmlist = query(rmlist_data, filters=(lambda rmlist: rmlist.typ == rmcat_list.typ), first=True)

                            if rmlist:
                                push_allot_list.bezeich = rmlist.rmcode

                            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                            if zimkateg:
                                push_allot_list.rmtype = zimkateg.kurzbez

                            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                            if zimmer:

                                paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                                if paramtext:
                                    push_allot_list.bsetup = paramtext.ptexte

                    elif bedsetup and not avail_rmcat:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                        if zimkateg:
                            push_allot_list.bezeich = zimkateg.kurzbez
                            push_allot_list.rmtype = zimkateg.kurzbez

                        zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                        if zimmer:

                            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                            if paramtext:
                                push_allot_list.bsetup = paramtext.ptexte

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) & (Queasy.logi3) & (Queasy.char1 == "") & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 171) & (Queasy.logi3) & (Queasy.char1 != "") & (Queasy.betriebsnr == becode)).first()
    while None != queasy:

        qsy2 = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, queasy.char1)]})

        if qsy2:
            statnr = 0
            curr_anz = 0

            rqsy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, queasy.char1)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"number3": [(eq, 0)]})

            if rqsy:

                if to_int(entry(0, rqsy.char2, ";")) == 1:
                    statnr = 1

                elif to_int(entry(1, rqsy.char2, ";")) == 1 and to_int(entry(2, rqsy.char2, ";")) == 0:
                    statnr = 2

                elif to_int(entry(2, rqsy.char2, ";")) == 1 and to_int(entry(1, rqsy.char2, ";")) == 0:
                    statnr = 3

                elif to_int(entry(1, rqsy.char2, ";")) == 1 and to_int(entry(2, rqsy.char2, ";")) == 1:
                    statnr = 4

            rqsy = get_cache (Queasy, {"key": [(eq, 175)],"char1": [(eq, r_list.rcode)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)]})

            if rqsy:

                if rqsy.char2  == ("CLOSE")  and rqsy.number2 == 0:
                    statnr = 0

                if rqsy.char2  == ("CTA")  and rqsy.number2 == 0:
                    statnr = 5

                if rqsy.char2  == ("CTD")  and rqsy.number2 == 0:
                    statnr = 6

                if rqsy.char2  == ("CLOSE")  and rqsy.number2 == 1:
                    statnr = 1

                if rqsy.char2  == ("CTA")  and rqsy.number2 == 1:
                    statnr = 2

                if rqsy.char2  == ("CTD")  and rqsy.number2 == 1:
                    statnr = 3
            counter_avail = counter_avail + 1
            push_allot_list = Push_allot_list()
            push_allot_list_data.append(push_allot_list)

            push_allot_list.startperiode = queasy.date1
            push_allot_list.endperiode = queasy.date1
            push_allot_list.rcode = queasy.char1
            push_allot_list.zikatnr = queasy.number1
            push_allot_list.counter = counter_avail
            push_allot_list.minlos = qsy2.number2
            push_allot_list.maxlos = qsy2.deci2
            push_allot_list.statnr = statnr

            rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)
            push_allot_list.qty = queasy.number3 - queasy.number2

            qsy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"betriebsnr": [(eq, becode)]})

            if qsy:
                room = rmcat_list.anzahl - qsy.number2 - qsy.number3

                if room < push_allot_list.qty:
                    push_allot_list.qty = room

            if cat_flag:

                qsy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, queasy.number1)]})

                if qsy:
                    push_allot_list.bezeich = qsy.char1
                    push_allot_list.rmtype = qsy.char1

            elif not bedsetup and not avail_rmcat:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                if zimkateg:
                    push_allot_list.bezeich = zimkateg.kurzbez
                    push_allot_list.rmtype = zimkateg.kurzbez

            elif bedsetup and avail_rmcat:

                rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)

                if rmcat_list:

                    rmlist = query(rmlist_data, filters=(lambda rmlist: rmlist.typ == rmcat_list.typ), first=True)

                    if rmlist:
                        push_allot_list.bezeich = rmlist.rmcode

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                    if zimkateg:
                        push_allot_list.rmtype = zimkateg.kurzbez

                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                    if zimmer:

                        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                        if paramtext:
                            push_allot_list.bsetup = paramtext.ptexte

            elif bedsetup and not avail_rmcat:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                if zimkateg:
                    push_allot_list.bezeich = zimkateg.kurzbez
                    push_allot_list.rmtype = zimkateg.kurzbez

                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                if zimmer:

                    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                    if paramtext:
                        push_allot_list.bsetup = paramtext.ptexte

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) & (Queasy.logi3) & (Queasy.char1 != "") & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 175) & (Queasy.logi3)).first()
    while None != queasy :

        push_allot_list = query(push_allot_list_data, filters=(lambda push_allot_list: push_allot_list.startperiode == queasy.date1 and push_allot_list.rcode == queasy.char1 and push_allot_list.zikatnr == queasy.number1), first=True)

        if not push_allot_list:
            counter_avail = counter_avail + 1
            push_allot_list = Push_allot_list()
            push_allot_list_data.append(push_allot_list)

            push_allot_list.startperiode = queasy.date1
            push_allot_list.endperiode = queasy.date1
            push_allot_list.rcode = queasy.char1
            push_allot_list.zikatnr = queasy.number1
            push_allot_list.counter = counter_avail

            if queasy.number3 != 0:

                guest = get_cache (Guest, {"gastnr": [(eq, queasy.number3)],"karteityp": [(eq, 2)],"steuernr": [(ne, "")]})

                if guest:
                    push_allot_list.ota = trim(entry(0, guest.steuernr, "|"))

            if cat_flag:

                qsy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, queasy.number1)]})

                if qsy:
                    push_allot_list.bezeich = qsy.char1
                    push_allot_list.rmtype = qsy.char1

            elif not bedsetup and not avail_rmcat:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                if zimkateg:
                    push_allot_list.bezeich = zimkateg.kurzbez
                    push_allot_list.rmtype = zimkateg.kurzbez

            elif bedsetup and avail_rmcat:

                rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)

                if rmcat_list:

                    rmlist = query(rmlist_data, filters=(lambda rmlist: rmlist.typ == rmcat_list.typ), first=True)

                    if rmlist:
                        push_allot_list.bezeich = rmlist.rmcode

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                    if zimkateg:
                        push_allot_list.rmtype = zimkateg.kurzbez

                    zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                    if zimmer:

                        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                        if paramtext:
                            push_allot_list.bsetup = paramtext.ptexte

            elif bedsetup and not avail_rmcat:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, queasy.number1)]})

                if zimkateg:
                    push_allot_list.bezeich = zimkateg.kurzbez
                    push_allot_list.rmtype = zimkateg.kurzbez

                zimmer = get_cache (Zimmer, {"zikatnr": [(eq, queasy.number1)]})

                if zimmer:

                    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 9200 + zimmer.setup)]})

                    if paramtext:
                        push_allot_list.bsetup = paramtext.ptexte

            if queasy.number2 == 1:

                if queasy.char2  == ("Close") :
                    push_allot_list.statnr = 1

                elif queasy.char2  == ("CTA") :
                    push_allot_list.statnr = 2

                elif queasy.char2  == ("CTD") :
                    push_allot_list.statnr = 3

            elif queasy.number2 == 0:

                if queasy.char2  == ("Close") :
                    push_allot_list.statnr = 0

                elif queasy.char2  == ("CTA") :
                    push_allot_list.statnr = 5

                elif queasy.char2  == ("CTD") :
                    push_allot_list.statnr = 6

            if push_allot_list.statnr >= 0:

                qsy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, queasy.char1)],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"betriebsnr": [(eq, becode)]})

                if not qsy:

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"betriebsnr": [(eq, becode)]})

                if qsy:

                    qsy2 = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, queasy.char1)]})

                    if qsy2:
                        zero_flag = False

                        if qsy2.date1 != None or qsy2.date2 != None:

                            if qsy2.date1 != None and qsy2.date2 == None and ci_date < qsy2.date1:
                                zero_flag = True

                            elif qsy2.date1 == None and qsy2.date2 != None and ci_date > qsy2.date2:
                                zero_flag = True

                            elif qsy2.date1 != None and qsy2.date2 != None and (ci_date < qsy2.date1 or ci_date > qsy2.date2):
                                zero_flag = True

                        if zero_flag:
                            push_allot_list.qty = 0
                        else:

                            if qsy.char1 != "":

                                bqueasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")],"date1": [(eq, queasy.date1)],"number1": [(eq, queasy.number1)],"betriebsnr": [(eq, becode)]})

                                if bqueasy:

                                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)

                                    if rmcat_list:
                                        room = rmcat_list.anzahl - bqueasy.number2 - bqueasy.number3
                                push_allot_list.qty = qsy.number3 - qsy.number2

                                if room < push_allot_list.qty:
                                    push_allot_list.qty = room

                            elif qsy.char1 == "":

                                rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == queasy.number1), first=True)

                                if rmcat_list:
                                    room = rmcat_list.anzahl - qsy.number2 - qsy.number3
                                    push_allot_list.qty = room

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 175) & (Queasy.logi3) & (Queasy._recid > curr_recid)).first()
    done = True

    return generate_output()