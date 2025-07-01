#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Queasy, Kontline, Ratecode, Zimkateg, Waehrung, Arrangement, Htparam, Guest, Guest_pr, Artikel, Res_line, Zimmer, Reservation, Segment

temp_list_list, Temp_list = create_model("Temp_list", {"rcode":string, "rmtype":string, "zikatnr":int})

def if_custom_pushall_ratebl(currcode:string, start_counter:int, inp_str:string, fdate:date, tdate:date, adult:int, child:int, becode:int, temp_list_list:[Temp_list]):

    prepare_cache ([Queasy, Kontline, Htparam, Guest, Guest_pr, Artikel, Res_line, Zimmer, Reservation])

    done = False
    curr_scode:string = ""
    rline_origcode:string = ""
    iftask:string = ""
    def_rate:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    end_date:date = None
    start_date:date = None
    date_110:date = None
    curr_date:date = None
    ci_date:date = None
    ankunft:date = None
    cat_flag:bool = False
    pushpax:bool = False
    do_it:bool = False
    incl_tentative:bool = False
    tax_included:bool = False
    global_occ:bool = False
    zikatnr:int = 0
    cm_gastno:int = 0
    i:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    maxroom:int = 0
    tokcounter:int = 0
    counter:int = 0
    occ_room:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    rmrate:Decimal = to_decimal("0.0")
    scode:string = ""
    tmp_date:int = 0
    loopi:int = 0
    n:int = 0
    m:int = 0
    loopj:int = 0
    k:int = 0
    j:int = 0
    queasy = kontline = ratecode = zimkateg = waehrung = arrangement = htparam = guest = guest_pr = artikel = res_line = zimmer = reservation = segment = None

    dynarate_list = r_list = s_list = rate_list = push_rate_list = change_room = temp_list = qsy = currqsy = kline = bqsy170 = qsy170 = qsy159 = bratecode = t_zimkateg = t_waehrung = t_arrangement = t_queasy = bqueasy = t_qsy18 = t_qsy145 = t_qsy152 = q_curr = t_qsy171 = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":string, "dynacode":string})
    r_list_list, R_list = create_model("R_list", {"rcode":string})
    s_list_list, S_list = create_model("S_list", {"static_code":string})
    rate_list_list, Rate_list = create_model("Rate_list", {"startperiode":date, "endperiode":date, "zikatnr":int, "counter":int, "rcode":string, "bezeich":string, "pax":int, "child":int, "rmrate":Decimal, "flag":bool, "currency":string, "scode":string}, {"flag": True})
    push_rate_list_list, Push_rate_list = create_model_like(Rate_list, {"str_date1":string, "str_date2":string})
    change_room_list, Change_room = create_model("Change_room", {"datum":date, "zikatnr":int, "occ":int})
    bratecode_list, Bratecode = create_model_like(Ratecode)
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_arrangement_list, T_arrangement = create_model_like(Arrangement)
    t_queasy_list, T_queasy = create_model_like(Queasy)
    bqueasy_list, Bqueasy = create_model_like(Queasy)
    t_qsy18_list, T_qsy18 = create_model_like(Queasy)
    t_qsy145_list, T_qsy145 = create_model_like(Queasy)
    t_qsy152_list, T_qsy152 = create_model_like(Queasy)
    q_curr_list, Q_curr = create_model_like(Queasy)
    t_qsy171_list, T_qsy171 = create_model_like(Queasy)

    Qsy = create_buffer("Qsy",Queasy)
    Currqsy = create_buffer("Currqsy",Queasy)
    Kline = create_buffer("Kline",Kontline)
    Bqsy170 = create_buffer("Bqsy170",Queasy)
    Qsy170 = create_buffer("Qsy170",Queasy)
    Qsy159 = create_buffer("Qsy159",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, curr_scode, rline_origcode, iftask, def_rate, mestoken, mesvalue, end_date, start_date, date_110, curr_date, ci_date, ankunft, cat_flag, pushpax, do_it, incl_tentative, tax_included, global_occ, zikatnr, cm_gastno, i, w_day, wd_array, maxroom, tokcounter, counter, occ_room, serv, vat, rmrate, scode, tmp_date, loopi, n, m, loopj, k, j, queasy, kontline, ratecode, zimkateg, waehrung, arrangement, htparam, guest, guest_pr, artikel, res_line, zimmer, reservation, segment
        nonlocal currcode, start_counter, inp_str, fdate, tdate, adult, child, becode
        nonlocal qsy, currqsy, kline, bqsy170, qsy170, qsy159


        nonlocal dynarate_list, r_list, s_list, rate_list, push_rate_list, change_room, temp_list, qsy, currqsy, kline, bqsy170, qsy170, qsy159, bratecode, t_zimkateg, t_waehrung, t_arrangement, t_queasy, bqueasy, t_qsy18, t_qsy145, t_qsy152, q_curr, t_qsy171
        nonlocal dynarate_list_list, r_list_list, s_list_list, rate_list_list, push_rate_list_list, change_room_list, bratecode_list, t_zimkateg_list, t_waehrung_list, t_arrangement_list, t_queasy_list, bqueasy_list, t_qsy18_list, t_qsy145_list, t_qsy152_list, q_curr_list, t_qsy171_list

        return {"done": done}

    def count_availability(curr_date:date, i_typ:int):

        nonlocal done, curr_scode, rline_origcode, iftask, def_rate, mestoken, mesvalue, end_date, start_date, date_110, ci_date, ankunft, cat_flag, pushpax, incl_tentative, tax_included, global_occ, zikatnr, cm_gastno, i, w_day, wd_array, maxroom, tokcounter, counter, occ_room, serv, vat, rmrate, scode, tmp_date, loopi, n, m, loopj, k, j, queasy, kontline, ratecode, zimkateg, waehrung, arrangement, htparam, guest, guest_pr, artikel, res_line, zimmer, reservation, segment
        nonlocal currcode, start_counter, inp_str, fdate, tdate, adult, child, becode
        nonlocal qsy, currqsy, kline, bqsy170, qsy170, qsy159


        nonlocal dynarate_list, r_list, s_list, rate_list, push_rate_list, change_room, temp_list, qsy, currqsy, kline, bqsy170, qsy170, qsy159, bratecode, t_zimkateg, t_waehrung, t_arrangement, t_queasy, bqueasy, t_qsy18, t_qsy145, t_qsy152, q_curr, t_qsy171
        nonlocal dynarate_list_list, r_list_list, s_list_list, rate_list_list, push_rate_list_list, change_room_list, bratecode_list, t_zimkateg_list, t_waehrung_list, t_arrangement_list, t_queasy_list, bqueasy_list, t_qsy18_list, t_qsy145_list, t_qsy152_list, q_curr_list, t_qsy171_list

        rm_occ = 0
        vhp_limited:bool = False
        do_it:bool = False
        rm_allot:int = 0

        def generate_inner_output():
            return (rm_occ)

        rm_occ = 0
        rm_allot = 0

        if global_occ:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                rm_allot = rm_allot + kontline.zimmeranz

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
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
            rm_occ = rm_occ + rm_allot
        else:

            if cat_flag:

                t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.typ == i_typ), first=True)

                if t_zimkateg:
                    i_typ = t_zimkateg.zikatnr

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontstatus == 1) & (Kontline.betriebsnr == 1) & (Kontline.zikatnr == i_typ) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                rm_allot = rm_allot + kontline.zimmeranz

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.zikatnr == i_typ) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    if reservation:

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0
                    else:
                        do_it = False

                if do_it:
                    rm_occ = rm_occ + res_line.zimmeranz

                kline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

                if kline:

                    kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

                    if kontline:
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                            if reservation:

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0
                            else:
                                do_it = False

                        if do_it:
                            rm_allot = rm_allot - res_line.zimmeranz
            rm_occ = rm_occ + rm_allot

        return generate_inner_output()


    bratecode_list.clear()
    t_zimkateg_list.clear()
    t_waehrung_list.clear()
    t_arrangement_list.clear()
    t_queasy_list.clear()
    bqueasy_list.clear()
    t_qsy18_list.clear()
    t_qsy145_list.clear()
    t_qsy152_list.clear()
    q_curr_list.clear()
    t_qsy171_list.clear()
    dynarate_list_list.clear()

    waehrung = db_session.query(Waehrung).first()
    while None != waehrung:
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

        curr_recid = waehrung._recid
        waehrung = db_session.query(Waehrung).filter(Waehrung._recid > curr_recid).first()

    arrangement = db_session.query(Arrangement).first()
    while None != arrangement:
        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        curr_recid = arrangement._recid
        arrangement = db_session.query(Arrangement).filter(Arrangement._recid > curr_recid).first()

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.active)).first()
    while None != zimkateg:
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

        curr_recid = zimkateg._recid
        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.active) & (Zimkateg._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 2)]})
    while None != queasy:
        bqueasy = Bqueasy()
        bqueasy_list.append(bqueasy)

        buffer_copy(queasy, bqueasy)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 18)]})
    while None != queasy:
        t_qsy18 = T_qsy18()
        t_qsy18_list.append(t_qsy18)

        buffer_copy(queasy, t_qsy18)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 18) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})
    while None != queasy:
        t_qsy152 = T_qsy152()
        t_qsy152_list.append(t_qsy152)

        buffer_copy(queasy, t_qsy152)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 152) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 164)]})
    while None != queasy:
        q_curr = Q_curr()
        q_curr_list.append(q_curr)

        buffer_copy(queasy, q_curr)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 164) & (Queasy._recid > curr_recid)).first()

    queasy = get_cache (Queasy, {"key": [(eq, 145)],"date1": [(ge, fdate),(le, tdate)]})
    while None != queasy:
        t_qsy145 = T_qsy145()
        t_qsy145_list.append(t_qsy145)

        buffer_copy(queasy, t_qsy145)

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 145) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy._recid > curr_recid)).first()

    t_qsy152 = query(t_qsy152_list, first=True)

    if t_qsy152:
        cat_flag = True

    for temp_list in query(temp_list_list):

        if cat_flag:

            t_qsy152 = query(t_qsy152_list, filters=(lambda t_qsy152: t_qsy152.char1 == temp_list.rmtype), first=True)

            if t_qsy152:
                temp_list.zikatnr = t_qsy152.number1
        else:

            t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.kurzbez == temp_list.rmtype), first=True)

            if t_zimkateg:
                temp_list.zikatnr = t_zimkateg.zikatnr

    if currcode.lower()  == ("*").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(ge, fdate),(le, tdate)],"betriebsnr": [(eq, becode)]})
        while None != queasy:
            t_qsy171 = T_qsy171()
            t_qsy171_list.append(t_qsy171)

            buffer_copy(queasy, t_qsy171)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()
    else:

        temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.rmtype.lower()  == (currcode).lower()), first=True)

        if temp_list:
            zikatnr = temp_list.zikatnr

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"number1": [(eq, zikatnr)],"date1": [(ge, fdate),(le, tdate)],"betriebsnr": [(eq, becode)]})
        while None != queasy:
            t_qsy171 = T_qsy171()
            t_qsy171_list.append(t_qsy171)

            buffer_copy(queasy, t_qsy171)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.number1 == zikatnr) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy.betriebsnr == becode) & (Queasy._recid > curr_recid)).first()
    adult = 2
    done = False

    if num_entries(inp_str, "=") >= 2:
        incl_tentative = logical(entry(0, inp_str, "="))
        pushpax = logical(entry(1, inp_str, "="))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

    if htparam:
        tax_included = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        date_110 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})

    if htparam:

        if htparam.flogical:

            if date_110 < get_current_date():

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    if fdate == ci_date:
        ankunft = ci_date
    else:
        ankunft = fdate + timedelta(days=2)
    r_list_list.clear()
    s_list_list.clear()

    temp_list = query(temp_list_list, first=True)

    if temp_list:

        for temp_list in query(temp_list_list):

            r_list = query(r_list_list, filters=(lambda r_list: r_list.rcode == temp_list.rcode), first=True)

            if not r_list:
                r_list = R_list()
                r_list_list.append(r_list)

                r_list.rcode = temp_list.rcode
    else:

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == cm_gastno)).order_by(Guest_pr._recid).all():
            r_list = R_list()
            r_list_list.append(r_list)

            r_list.rcode = guest_pr.code

    if pushpax:
        n = 1
        k = 0


    else:
        n = adult
        m = adult
        k = 0
        j = 0

    for r_list in query(r_list_list):
        bqueasy = query(bqueasy_list, (lambda bqueasy: bqueasy.char1 == r_list.rcode), first=True)
        if not bqueasy:
            continue


        if bqueasy.logi2:

            for ratecode in db_session.query(Ratecode).filter(
                         (Ratecode.code == r_list.rcode)).order_by(Ratecode._recid).all():
                dynarate_list = Dynarate_list()
                dynarate_list_list.append(dynarate_list)

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

    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
    global_occ = None != dynarate_list and htparam.finteger == 1

    if global_occ:

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
            dynarate_list_list.remove(dynarate_list)

    else:

        for dynarate_list in query(dynarate_list_list):

            t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.kurzbez == dynarate_list.rmtype), first=True)

            if cat_flag:

                temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.typ), first=True)

                if not temp_list:
                    dynarate_list_list.remove(dynarate_list)
            else:

                temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.zikatnr), first=True)

                if not temp_list:
                    dynarate_list_list.remove(dynarate_list)

    dynarate_list = query(dynarate_list_list, first=True)

    if dynarate_list:

        for dynarate_list in query(dynarate_list_list):

            s_list = query(s_list_list, filters=(lambda s_list: s_list.static_code == dynarate_list.rcode), first=True)

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.static_code = dynarate_list.rcode

        for s_list in query(s_list_list):

            if cat_flag:

                for ratecode in db_session.query(Ratecode).filter(
                             (Ratecode.code == s_list.static_code) & (Ratecode.startperiode <= tdate) & (Ratecode.endperiode >= fdate) & (Ratecode.erwachs > 0)).order_by(Ratecode._recid).all():

                    t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == ratecode.zikatnr), first=True)

                    temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.zikatnr == t_zimkateg.typ), first=True)

                    if temp_list:
                        bratecode = Bratecode()
                        bratecode_list.append(bratecode)

                        buffer_copy(ratecode, bratecode)
            else:

                for ratecode in db_session.query(Ratecode).filter(
                             (Ratecode.code == s_list.static_code) & (Ratecode.startperiode <= tdate) & (Ratecode.endperiode >= fdate) & (Ratecode.erwachs > 0)).order_by(Ratecode._recid).all():

                    temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.zikatnr == ratecode.zikatnr), first=True)

                    if temp_list:
                        bratecode = Bratecode()
                        bratecode_list.append(bratecode)

                        buffer_copy(ratecode, bratecode)

    for t_qsy171 in query(t_qsy171_list, filters=(lambda t_qsy171: t_qsy171.char1 == "")):
        w_day = wd_array[get_weekday(t_qsy171.date1) - 1]

        for r_list in query(r_list_list):
            bqueasy = query(bqueasy_list, (lambda bqueasy: bqueasy.char1 == r_list.rcode), first=True)
            if not bqueasy:
                continue


            if cat_flag:

                t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.typ == t_qsy171.number1), first=True)
            else:

                t_zimkateg = query(t_zimkateg_list, filters=(lambda t_zimkateg: t_zimkateg.zikatnr == t_qsy171.number1), first=True)
            tmp_date = (ankunft - ci_date).days

            if bqueasy.number3 > tmp_date:
                pass

            elif bqueasy.deci3 > 0 and bqueasy.deci3 < tmp_date:
                pass

            elif not bqueasy.logi2:

                if pushpax:

                    for ratecode in db_session.query(Ratecode).filter(
                                 (Ratecode.code == r_list.rcode) & (Ratecode.zikatnr == t_zimkateg.zikatnr) & (Ratecode.startperiode <= t_qsy171.date1) & (Ratecode.endperiode >= t_qsy171.date1) & (Ratecode.erwachs > 0)).order_by(Ratecode.erwachs.desc()).yield_per(100):
                        m = ratecode.erwachs
                        j = ratecode.kind1


                        break
                for loopi in range(n,m + 1) :

                    ratecode = get_cache (Ratecode, {"code": [(eq, r_list.rcode)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"startperiode": [(le, t_qsy171.date1)],"endperiode": [(ge, t_qsy171.date1)],"wday": [(eq, w_day)],"kind1": [(eq, child)],"erwachs": [(eq, loopi)]})

                    if not ratecode:

                        ratecode = get_cache (Ratecode, {"code": [(eq, r_list.rcode)],"zikatnr": [(eq, t_zimkateg.zikatnr)],"startperiode": [(le, t_qsy171.date1)],"endperiode": [(ge, t_qsy171.date1)],"wday": [(eq, 0)],"kind1": [(eq, child)],"erwachs": [(eq, loopi)]})

                    if ratecode:

                        t_arrangement = query(t_arrangement_list, filters=(lambda t_arrangement: t_arrangement.argtnr == ratecode.argtnr), first=True)

                        if t_arrangement:

                            artikel = get_cache (Artikel, {"artnr": [(eq, t_arrangement.argt_artikelnr)]})

                            if artikel:
                                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, t_qsy171.date1, artikel.service_code, artikel.mwst_code))
                        counter = counter + 1
                        rate_list = Rate_list()
                        rate_list_list.append(rate_list)

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

                        t_qsy18 = query(t_qsy18_list, filters=(lambda t_qsy18: t_qsy18.number1 == ratecode.marknr), first=True)

                        if t_qsy18:

                            t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung: t_waehrung.wabkurz == t_qsy18.char3), first=True)

                            if t_waehrung:

                                q_curr = query(q_curr_list, filters=(lambda q_curr: q_curr.char1 == t_waehrung.wabkurz and q_curr.number1 == becode), first=True)

                                if q_curr:
                                    rate_list.currency = q_curr.char2
                                else:
                                    rate_list.currency = "IDR"
                            else:
                                rate_list.currency = "IDR"

                        if cat_flag:

                            t_qsy152 = query(t_qsy152_list, filters=(lambda t_qsy152: t_qsy152.number1 == t_qsy171.number1), first=True)

                            if t_qsy152:
                                rate_list.bezeich = t_qsy152.char1
                        else:
                            rate_list.bezeich = t_zimkateg.kurzbez

            elif bqueasy.logi2:
                curr_scode = ""
                occ_room = 0


                occ_room = count_availability(t_qsy171.date1, t_qsy171.number1)

                if not global_occ:

                    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)

                    if not dynarate_list:

                        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode and dynarate_list.rmType == t_zimkateg.kurzbez), first=True)
                else:

                    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode), first=True)

                    if not dynarate_list:

                        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and dynarate_list.fr_room <= occ_room and dynarate_list.to_room >= occ_room and dynarate_list.dynacode == r_list.rcode), first=True)

                if dynarate_list:

                    if not global_occ:

                        t_qsy145 = query(t_qsy145_list, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == t_zimkateg.zikatnr and t_qsy145.deci1 == dynarate_list.w_day and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                        if not t_qsy145:

                            t_qsy145 = query(t_qsy145_list, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == t_zimkateg.zikatnr and t_qsy145.deci1 == 0 and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)
                    else:

                        t_qsy145 = query(t_qsy145_list, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == 0 and t_qsy145.deci1 == dynarate_list.w_day and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                        if not t_qsy145:

                            t_qsy145 = query(t_qsy145_list, filters=(lambda t_qsy145: t_qsy145.char1 == r_list.rcode and t_qsy145.char2 == dynarate_list.rcode and t_qsy145.number1 == 0 and t_qsy145.deci1 == 0 and t_qsy145.deci2 == dynarate_list.counter and t_qsy145.date1 == t_qsy171.date1), first=True)

                    if t_qsy145:
                        curr_scode = t_qsy145.char3
                    else:
                        curr_scode = dynarate_list.rcode

                    if pushpax:

                        for bratecode in query(bratecode_list, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.erwachs > 0), sort_by=[("erwachs",True)]):
                            m = bratecode.erwachs
                            j = bratecode.kind1


                            break
                    for loopi in range(n,m + 1) :

                        bratecode = query(bratecode_list, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.erwachs == loopi and bratecode.kind1 == child and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.wday == w_day), first=True)

                        if not bratecode:

                            bratecode = query(bratecode_list, filters=(lambda bratecode: bratecode.code.lower()  == (curr_scode).lower()  and bratecode.zikatnr == t_zimkateg.zikatnr and bratecode.erwachs == loopi and bratecode.kind1 == child and bratecode.startperiode <= t_qsy171.date1 and bratecode.endperiode >= t_qsy171.date1 and bratecode.wday == 0), first=True)

                        if bratecode:

                            t_arrangement = query(t_arrangement_list, filters=(lambda t_arrangement: t_arrangement.argtnr == bratecode.argtnr), first=True)

                            if t_arrangement:

                                artikel = get_cache (Artikel, {"artnr": [(eq, t_arrangement.argt_artikelnr)]})

                                if artikel:
                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, t_qsy171.date1, artikel.service_code, artikel.mwst_code))
                            counter = counter + 1
                            rate_list = Rate_list()
                            rate_list_list.append(rate_list)

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

                            t_qsy18 = query(t_qsy18_list, filters=(lambda t_qsy18: t_qsy18.number1 == bratecode.marknr), first=True)

                            t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung: t_waehrung.wabkurz == t_qsy18.char3), first=True)

                            if t_waehrung:

                                q_curr = query(q_curr_list, filters=(lambda q_curr: q_curr.char1 == t_waehrung.wabkurz and q_curr.number1 == becode), first=True)

                                if q_curr:
                                    rate_list.currency = q_curr.char2
                                else:
                                    rate_list.currency = "IDR"
                            else:
                                rate_list.currency = "IDR"

                            if cat_flag:

                                t_qsy152 = query(t_qsy152_list, filters=(lambda t_qsy152: t_qsy152.number1 == t_qsy171.number1), first=True)
                                rate_list.bezeich = t_qsy152.char1
                            else:
                                rate_list.bezeich = t_zimkateg.kurzbez

    for rate_list in query(rate_list_list, filters=(lambda rate_list: rate_list.startperiode >= fdate and rate_list.endperiode <= tdate)):

        qsy170 = get_cache (Queasy, {"char1": [(eq, rate_list.rcode)],"number1": [(eq, rate_list.zikatnr)],"date1": [(eq, rate_list.startperiode)],"number2": [(eq, rate_list.pax)],"number3": [(eq, rate_list.child)],"betriebsnr": [(eq, becode)]})

        if qsy170:

            qsy = get_cache (Queasy, {"_recid": [(eq, qsy170._recid)]})

            if qsy:
                qsy.logi3 = True
                qsy.deci1 =  to_decimal(rate_list.rmrate)
                qsy.char2 = rate_list.scode


                pass
                pass

        elif not qsy170:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            t_queasy.key = 170
            t_queasy.date1 = rate_list.startperiode
            t_queasy.number1 = rate_list.zikatnr
            t_queasy.number2 = rate_list.pax
            t_queasy.number3 = rate_list.child
            t_queasy.deci1 =  to_decimal(rate_list.rmrate)
            t_queasy.char1 = rate_list.rcode
            t_queasy.char2 = rate_list.scode
            t_queasy.char3 = rate_list.currency
            t_queasy.logi1 = False
            t_queasy.logi2 = False
            t_queasy.logi3 = True
            t_queasy.betriebsnr = becode

    for t_queasy in query(t_queasy_list):
        bqsy170 = Queasy()
        db_session.add(bqsy170)

        buffer_copy(t_queasy, bqsy170)

    return generate_output()