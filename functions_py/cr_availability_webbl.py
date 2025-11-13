#using conversion tools version: 1.0.0.119

#------------------------------------------
# Rd, 31/10/2025
# Ticket:F6D79E
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import not_, and_, or_, func
from datetime import date
import random
from functions.available_rates_cldbl import available_rates_cldbl
from models import Kontline, Res_line, Zimmer, Paramtext, Htparam, Arrangement, Zimkateg, Queasy, Artikel, Fixleist, Reslin_queasy, Reservation, Segment, Outorder, Resplan

def cr_availability_webbl(pvilanguage:int, vhp_limited:bool, op_type:int, printer_nr:int, call_from:int, adult_child_str:string, statsort:int, dispsort:int, curr_date:date, incl_tentative:bool, mi_inactive:bool, show_rate:bool, indgastnr:int, qci_zinr:string):

    prepare_cache ([Zimmer, Paramtext, Htparam, Arrangement, Zimkateg, Queasy, Artikel, Fixleist, Reslin_queasy, Reservation, Outorder, Resplan])

    room_list_data = []
    sum_list_data = []
    lvcarea:string = "availability"
    logid:int = 0
    logstr:string = ""
    cdstr:string = ""
    col_label:List[string] = create_empty_list(31,"")
    curr_day:int = 0
    datum:date = None
    tot_room:int = 0
    i:int = 0
    ci_date:date = None
    co_date:date = None
    from_date:date = None
    to_date:date = None
    last_option:bool = False
    wlist:string = ""
    dlist:string = ""
    j:int = 0
    dd:int = 0
    mm:int = 0
    yyyy:int = 0
    num_day:int = 0
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    res_allot:List[int] = create_empty_list(300,0)
    week_list:List[string] = create_empty_list(7,"")
    rpt_title:string = ""
    curr_time:int = 0
    kontline = res_line = zimmer = paramtext = htparam = arrangement = zimkateg = queasy = artikel = fixleist = reslin_queasy = reservation = segment = outorder = resplan = None

    sum_list = room_avail_list = date_list = room_list = rate_list = created_list = t_kontline = rmcat_list = tmp_resline = tmp_extra = temp_art = qci_zimmer = buff_ratelist = None

    sum_list_data, Sum_list = create_model("Sum_list", {"allot_flag":bool, "bezeich":string, "summe":[int,300]})
    room_avail_list_data, Room_avail_list = create_model("Room_avail_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int,300], "bezeich":string, "room":[int,300], "coom":[string,300]}, {"sleeping": True})
    date_list_data, Date_list = create_model("Date_list", {"datum":date, "counter":int})
    room_list_data, Room_list = create_model("Room_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int,300], "bezeich":string, "room":[int,300], "coom":[string,300], "rmrate":[Decimal,300], "currency":int, "wabkurz":string, "i_counter":int, "rateflag":bool, "adult":int, "child":int, "prcode":[string,300], "rmcat":string, "argt":string, "rcode":string, "segmentcode":string, "dynarate":bool, "expired":bool, "argt_remark":string, "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "marknr":int, "datum":[date,300]}, {"sleeping": True, "frdate": None, "todate": None})
    rate_list_data, Rate_list = create_model("Rate_list", {"ratecode":string, "segmentcode":string, "dynaflag":bool, "expired":bool, "room_type":int, "argtno":int, "statcode":[string,300], "rmrate":[Decimal,300], "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "adult":int, "child":int, "currency":int, "wabkurz":string, "occ_rooms":int, "marknr":int, "i_counter":int}, {"frdate": None, "todate": None})
    created_list_data, Created_list = create_model("Created_list", {"ratecode":string, "marknr":int, "rmcateg":int, "argtno":int, "statcode":[string,300], "rmrate":[Decimal,300]})
    t_kontline_data, T_kontline = create_model_like(Kontline)
    rmcat_list_data, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "sleeping":bool}, {"sleeping": True})
    tmp_resline_data, Tmp_resline = create_model_like(Res_line)
    tmp_extra_data, Tmp_extra = create_model("Tmp_extra", {"art":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int})
    temp_art_data, Temp_art = create_model("Temp_art", {"art_nr":int, "art_nm":string})

    Qci_zimmer = create_buffer("Qci_zimmer",Zimmer)


    db_session = local_storage.db_session

    qci_zinr = qci_zinr.strip()
    adult_child_str = adult_child_str.strip()
    def generate_output():
        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        return {"indgastnr": indgastnr, "room-list": room_list_data, "sum-list": sum_list_data}

    def create_room_list():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        curr_i:int = 0
        i:int = 0

        for room_avail_list in query(room_avail_list_data):
            curr_i = curr_i + 1
            room_list = Room_list()
            room_list_data.append(room_list)

            buffer_copy(room_avail_list, room_list)
            room_list.i_counter = curr_i


    def create_rate_list():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        curr_i:int = 0
        i:int = 0
        looprate:int = 0
        fdate:date = None
        tdate:date = None
        str_argt:string = ""
        room_cat:string = ""
        adult:int = 0
        argt_code:string = ""
        argt_intervall:int = 0
        argt_zuordnung:string = ""
        Buff_ratelist = Rate_list
        buff_ratelist_data = rate_list_data

        fdate = curr_date
        tdate = curr_date + timedelta(days=num_day)

        if tdate > co_date:
            tdate = co_date

        for room_avail_list in query(room_avail_list_data):
            curr_i = curr_i + 1
            room_list = Room_list()
            room_list_data.append(room_list)

            buffer_copy(room_avail_list, room_list)
            room_list.i_counter = curr_i * 100


            curr_time = get_current_time_in_seconds()


            indgastnr, created_list_data, rate_list_data = get_output(available_rates_cldbl(fdate, tdate, room_avail_list.zikatnr, curr_i, adult_child_str, indgastnr, created_list_data))

            for rate_list in query(rate_list_data, sort_by=[("i_counter",False)]):

                # arrangement = get_cache (Arrangement, {"argtnr": [(eq, rate_list.argtno)]})
                arrangement = db_session.query(Arrangement).filter(Arrangement.argtnr == rate_list.argtno).first()

                zimkateg = db_session.query(Zimkateg).filter(Zimkateg.zikatnr == room_avail_list.zikatnr).first()

                if arrangement:
                    argt_code = arrangement.arrangement
                    argt_intervall = arrangement.intervall
                    argt_zuordnung = arrangement.zuordnung

                if not qci_zimmer or (qci_zimmer and qci_zimmer.zikatnr == room_avail_list.zikatnr):
                    room_list = Room_list()
                    room_list_data.append(room_list)

                    buffer_copy(room_avail_list, room_list)
                    room_list.i_counter = rate_list.i_counter
                    room_list.rateflag = True
                    room_list.rcode = rate_list.rateCode
                    room_list.segmentcode = rate_list.segmentcode
                    room_list.dynarate = rate_list.dynaflag
                    room_list.expired = rate_list.expired
                    room_list.marknr = rate_list.marknr
                    room_list.adult = rate_list.adult
                    room_list.child = rate_list.child
                    room_list.minstay = rate_list.minstay
                    room_list.maxstay = rate_list.maxstay
                    room_list.minadvance = rate_list.minadvance
                    room_list.maxadvance = rate_list.maxadvance
                    room_list.frdate = rate_list.frdate
                    room_list.todate = rate_list.todate
                    room_list.currency = rate_list.currency
                    room_list.rmcat = zimkateg.kurzbez
                    room_list.argt = argt_code
                    room_list.bezeich = rate_list.rateCode + "/" +\
                            argt_code + "/" +\
                            to_string(room_list.adult) + "/" +\
                            to_string(room_list.child) + ";"

                    if num_entries(rate_list.wabkurz, ";") >= 2:
                        room_list.wabkurz = entry(0, rate_list.wabkurz, ";")
                        room_list.bezeich = room_list.bezeich + entry(1, rate_list.wabkurz, ";")


                    else:
                        room_list.wabkurz = rate_list.wabkurz

                    if room_list.minstay < argt_intervall:
                        room_list.minstay = argt_intervall

                    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, rate_list.ratecode)]})
                    room_list.argt_remark = queasy.char2 + chr_unicode(10)

                    if room_list.frdate != None:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("Begin Sell Date:", lvcarea, "") + " " + to_string(room_list.frdate) + "; "

                    if room_list.todate != None:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("End Sell Date:", lvcarea, "") + " " + to_string(room_list.todate) + "; "

                    if room_list.minstay > 0:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("Minimum Stay (in nights):", lvcarea, "") + " " + to_string(room_list.minstay) + "; "

                    if room_list.maxstay > 0:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("Maximum Stay (in nights):", lvcarea, "") + " " + to_string(room_list.maxstay) + "; "

                    if room_list.minadvance > 0:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("Min Advance Booking (in days):", lvcarea, "") + " " + to_string(room_list.minadvance) + "; "

                    if room_list.maxadvance > 0:
                        room_list.argt_remark = room_list.argt_remark + translateExtended ("Max Advance Booking (in days):", lvcarea, "") + " " + to_string(room_list.maxadvance) + "; "

                    if argt_zuordnung != "":
                        room_list.argt_remark = room_list.argt_remark + argt_zuordnung + ";"
                    looprate = 0
                    for datum in date_range(fdate,tdate) :
                        looprate = looprate + 1
                        room_list.datum[looprate - 1] = datum
                        room_list.prcode[looprate - 1] = rate_list.statCode[looprate - 1]
                        room_list.rmrate[looprate - 1] = rate_list.rmrate[looprate - 1]

                        if room_list.rmrate[looprate - 1] <= 99999:
                            room_list.coom[looprate - 1] = to_string(room_list.rmrate[looprate - 1], ">,>>>,>>9.99")
                        else:
                            room_list.coom[looprate - 1] = to_string(room_list.rmrate[looprate - 1], " >>>,>>>,>>9")


    def create_tentative():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        datum_t:date = None
        loop_t:int = 0
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = translateExtended ("Tentative", lvcarea, "")
        datum = curr_date
        i = 1
        while i <= (num_day + 1) :

            date_list = query(date_list_data, filters=(lambda date_list: date_list.counter == i), first=True)

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus == 3) & (((Res_line.ankunft <= date_list.datum) & (Res_line.abreise > date_list.datum)) | ((Res_line.ankunft == date_list.datum) & (Res_line.abreise == date_list.datum))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                sum_list.summe[date_list.counter - 1] = sum_list.summe[date_list.counter - 1] + res_line.zimmeranz
            i = i + 1


    def create_tmpextra(art_nr:int, typ_pos:string, pos_from:string, cdate:date, room:string, qty:int):

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data


        tmp_extra = Tmp_extra()
        tmp_extra_data.append(tmp_extra)

        tmp_extra.art = art_nr
        tmp_extra.typ_pos = typ_pos
        tmp_extra.pos_from = pos_from
        tmp_extra.cdate = cdate
        tmp_extra.room = room
        tmp_extra.qty = qty


    def calc_extra(fdate:date):

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        tdate:date = None
        art_nr:int = 0
        int_art:string = ""
        bdate:date = None
        edate:date = None
        eposdate:date = None
        ndate:date = None
        art_qty:int = 0
        art_rem:int = 0
        tot_used:int = 0
        argtnr:int = 0

        bargt = None
        Bargt =  create_buffer("Bargt",Arrangement)
        tdate = fdate + timedelta(days=num_day)

        if tdate > co_date:
            tdate = co_date
        tmp_resline_data.clear()
        tmp_extra_data.clear()
        temp_art_data.clear()

        for res_line in db_session.query(Res_line).filter(
                 (not_ (Res_line.abreise < fdate)) & (not_ (Res_line.ankunft > tdate)) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

            tmp_resline = query(tmp_resline_data, filters=(lambda tmp_resline: tmp_resline.resnr == res_line.resnr and tmp_resline.reslinnr == res_line.reslinnr), first=True)

            if not tmp_resline:
                tmp_resline = Tmp_resline()
                tmp_resline_data.append(tmp_resline)

                buffer_copy(res_line, tmp_resline)

        htparam = get_cache (Htparam, {"paramgruppe": [(eq, 5)],"paramnr": [(eq, 2999)]})

        if htparam:
            for i in range(1,num_entries(htparam.fchar , ";")  + 1) :
                int_art = entry(i - 1, htparam.fchar, ";")

                if int_art != "":

                    artikel = get_cache (Artikel, {"artnr": [(eq, int (int_art))],"departement": [(eq, 0)]})

                    if artikel:
                        temp_art = Temp_art()
                        temp_art_data.append(temp_art)

                        temp_art.art_nr = int (int_art)
                        temp_art.art_nm = artikel.bezeich


                        art_nr = int (int_art)

                        for tmp_resline in query(tmp_resline_data, sort_by=[("resnr",False)]):

                            for fixleist in db_session.query(Fixleist).filter(
                                     (Fixleist.resnr == tmp_resline.resnr) & (Fixleist.reslinnr == tmp_resline.reslinnr) & (Fixleist.artnr == art_nr) & (Fixleist.departement == 0)).order_by(Fixleist._recid).all():

                                if tmp_resline.ankunft == tmp_resline.abreise:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 6:
                                        create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:

                                        if get_day(tmp_resline.ankunft) == 1:
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 5:

                                        if get_day(tmp_resline.ankunft + 1) == 1:
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)
                                else:

                                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 4 or fixleist.sequenz == 5:

                                        if tmp_resline.ankunft < fdate:
                                            bdate = fdate
                                        else:
                                            bdate = tmp_resline.ankunft

                                        if tmp_resline.abreise > tdate:
                                            edate = tdate + timedelta(days=1)

                                        elif tmp_resline.abreise <= tdate:
                                            edate = tmp_resline.abreise

                                    if fixleist.sequenz == 1:
                                        while bdate < edate :
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 2:
                                        create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                                    elif fixleist.sequenz == 4:
                                        while bdate < edate :

                                            if get_day(bdate) == 1:
                                                create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 5:
                                        while bdate < edate :

                                            if get_day(bdate + 1) == 1:
                                                create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + timedelta(days=1)

                                    elif fixleist.sequenz == 6:
                                        eposdate = (fixleist.lfakt + timedelta(days=fixleist.dekade))

                                        if fixleist.lfakt < fdate:
                                            bdate = fdate
                                        else:
                                            bdate = fixleist.lfakt

                                        if eposdate > tdate:
                                            edate = tdate + timedelta(days=1)

                                        elif eposdate <= tdate:

                                            if eposdate > tmp_resline.abreise:
                                                edate = tmp_resline.abreise

                                            elif eposdate <= tmp_resline.abreise:
                                                edate = eposdate
                                        while bdate < edate :
                                            create_tmpextra(art_nr, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)
                                            bdate = bdate + timedelta(days=1)

                            bargt = get_cache (Arrangement, {"arrangement": [(eq, tmp_resline.arrangement)]})

                            if bargt:
                                argtnr = bargt.argtnr

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line")) & (Reslin_queasy.resnr == tmp_resline.resnr) & (Reslin_queasy.reslinnr == tmp_resline.reslinnr) & (Reslin_queasy.number1 == 0) & (Reslin_queasy.number3 == art_nr) & (Reslin_queasy.number2 == argtnr)).order_by(Reslin_queasy._recid).all():

                                if reslin_queasy.date1 < fdate:
                                    bdate = fdate
                                else:
                                    bdate = reslin_queasy.date1

                                if reslin_queasy.date2 > tdate:
                                    edate = tdate + timedelta(days=1)

                                elif reslin_queasy.date2 <= tdate:
                                    edate = reslin_queasy.date2
                                while bdate < edate :
                                    create_tmpextra(art_nr, "argt-line", "0", bdate, tmp_resline.zinr, 1)
                                    bdate = bdate + timedelta(days=1)
        ndate = fdate

        if not incl_tentative:
            sum_list = Sum_list()
            sum_list_data.append(sum_list)

            sum_list.bezeich = ""


            create_tentative()
            tot_used = 0

            for temp_art in query(temp_art_data):

                artikel = get_cache (Artikel, {"artnr": [(eq, temp_art.art_nr)],"departement": [(eq, 0)]})

                if artikel:
                    art_qty = artikel.anzahl
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.bezeich = temp_art.art_nm
                    ndate = fdate
                    for i in range(1,num_day + 1) :

                        for tmp_extra in query(tmp_extra_data, filters=(lambda tmp_extra: tmp_extra.art == temp_art.art_nr and tmp_extra.cdate == ndate and tmp_extra.qty != 0)):
                            tot_used = tot_used + tmp_extra.qty
                        art_rem = art_qty - tot_used
                        sum_list.summe[i - 1] = art_rem
                        ndate = fdate + timedelta(days=i)
                        tot_used = 0


    def count_rmcateg():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        zikatnr:int = 0
        rmcat_list_data.clear()
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:
                tot_room = tot_room + 1

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    zikatnr = zimkateg.zikatnr
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1

        if not mi_inactive:

            return
        zikatnr = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping == False)).order_by(Zimmer.zikatnr).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg.verfuegbarkeit:

                if zikatnr != zimkateg.zikatnr:
                    rmcat_list = Rmcat_list()
                    rmcat_list_data.append(rmcat_list)

                    rmcat_list.zikatnr = zimkateg.zikatnr
                    rmcat_list.anzahl = 1
                    rmcat_list.sleeping = False
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1
                zikatnr = zimkateg.zikatnr


    def create_browse():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, tot_room, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        datum:date = None
        fdate:date = None
        tdate:date = None
        i:int = 0
        anz:int = 0
        do_it:bool = False
        tmp_list:List[int] = create_empty_list(300,0)
        ooo_list:List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        om_list:List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        om_flag:bool = False
        tot_used:int = 0
        art_qty:int = 0
        kline = None
        Kline =  create_buffer("Kline",Kontline)

        for kontline in db_session.query(Kontline).filter(
                 (Kontline.betriebsnr == 0) & 
                #  (Kontline.ankunft <= to_date) & 
                #  (Kontline.abreise >= from_date) & 
                 (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
            
            if kontline.ankunft is None or kontline.abreise is None:
                continue    

            t_kontline = T_kontline()
            t_kontline_data.append(t_kontline)

            buffer_copy(kontline, t_kontline)
        count_rmcateg()
        room_avail_list_data.clear()
        sum_list_data.clear()
        fdate = curr_date
        tdate = curr_date + timedelta(days=num_day)

        if tdate > co_date:
            tdate = co_date
        for i in range(1,num_day + 1) :
            res_allot[i - 1] = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.active_flag <= 1) & (Res_line.kontignr > 0) & not_(Res_line.ankunft > tdate) & not_(Res_line.abreise <= fdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if res_line.ankunft is None or res_line.abreise is None:
                continue

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if res_line.resstatus == 3 and not incl_tentative:
                do_it = False

            if do_it:
                for i in range(1,num_day + 1) :
                    datum = curr_date + timedelta(days=i - 1)

                    if datum >= res_line.ankunft and datum < res_line.abreise:

                        kline = db_session.query(Kline).filter(
                                 (Kline.kontignr == res_line.kontignr) & (Kline.kontstatus == 1)).first()

                        kontline = get_cache (Kontline, {"kontcode": [(eq, kline.kontcode)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

                        if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                            res_allot[i - 1] = res_allot[i - 1] + res_line.zimmeranz

        if not incl_tentative:

            if statsort == 1:
                sum_list = Sum_list()
                sum_list_data.append(sum_list)

                sum_list.bezeich = translateExtended ("Avail before Allotm", lvcarea, "")

                for zimkateg in db_session.query(Zimkateg).filter(
                         (Zimkateg.verfuegbarkeit)).order_by(Zimkateg.typ, Zimkateg.zikatnr).all():

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimkateg.zikatnr and rmcat_list.sleeping), first=True)

                    if rmcat_list:
                        room_avail_list = Room_avail_list()
                        room_avail_list_data.append(room_avail_list)

                        i = 1
                        while i <= (num_day + 1) :
                            room_avail_list.room[i - 1] = rmcat_list.anzahl
                            i = i + 1
                        room_avail_list.i_typ = zimkateg.typ
                        room_avail_list.zikatnr = zimkateg.zikatnr
                        room_avail_list.bezeich = zimkateg.kurzbez +\
                                " - " + to_string(zimkateg.overbooking, ">>9")

                zimkateg_obj_list = {}
                for zimkateg in db_session.query(Zimkateg).filter(
                         ((Zimkateg.zikatnr.in_(list(set([rmcat_list.zikatnr for rmcat_list in rmcat_list_data if ~rmcat_list.sleeping])))))).order_by(Zimkateg.typ, Zimkateg.zikatnr).all():
                    if zimkateg_obj_list.get(zimkateg._recid):
                        continue
                    else:
                        zimkateg_obj_list[zimkateg._recid] = True

                    rmcat_list = query(rmcat_list_data, (lambda rmcat_list: (zimkateg.zikatnr == rmcat_list.zikatnr)), first=True)
                    room_avail_list = Room_avail_list()
                    room_avail_list_data.append(room_avail_list)

                    room_avail_list.sleeping = False
                    i = 1
                    while i <= (num_day + 1) :
                        room_avail_list.room[i - 1] = rmcat_list.anzahl
                        i = i + 1
                    room_avail_list.i_typ = zimkateg.typ
                    room_avail_list.zikatnr = zimkateg.zikatnr
                    room_avail_list.bezeich = zimkateg.kurzbez +\
                            " - " + to_string(zimkateg.overbooking, ">>9")


                    datum = curr_date
                    for i in range(1,num_day + 1) :

                        res_line_obj_list = {}
                        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & not_ (Zimmer.sleeping)).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.zikatnr == room_avail_list.zikatnr) & (Res_line.zinr != "") & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True

                            if not vhp_limited:
                                do_it = True
                            else:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                        datum = datum + timedelta(days=1)

                outorder_obj_list = {}
                outorder = Outorder()
                zimmer = Zimmer()
                for outorder.gespstart, outorder.gespende, outorder.zinr, outorder.betriebsnr, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder.zinr, Outorder.betriebsnr, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                    datum = curr_date

                    room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.zikatnr == zimmer.zikatnr and room_avail_list.sleeping), first=True)

                    if room_avail_list:
                        for i in range(1,num_day + 1) :

                            if datum >= outorder.gespstart and datum <= outorder.gespende:

                                if outorder.betriebsnr == 2:
                                    om_list[i - 1] = om_list[i - 1] + 1
                                    om_flag = True
                                else:
                                    ooo_list[i - 1] = ooo_list[i - 1] + 1
                                    room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                            datum = datum + timedelta(days=1)
                i = 1
                datum = curr_date
                while i <= (num_day + 1) :

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                        room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping and room_avail_list.zikatnr == res_line.zikatnr), first=True)

                        if room_avail_list:
                            do_it = True

                            if res_line.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                                do_it = zimmer.sleeping

                            if res_line.resstatus == 3 and not incl_tentative:
                                do_it = False

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - res_line.zimmeranz

                    for kontline in db_session.query(Kontline).filter(
                             (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                        room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping and room_avail_list.zikatnr == kontline.zikatnr), first=True)

                        if room_avail_list:
                            room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - kontline.zimmeranz
                    i = i + 1
                    datum = datum + timedelta(days=1)

                if mi_inactive:
                    i = 1
                    datum = curr_date
                    while i <= (num_day + 1) :

                        for res_line in db_session.query(Res_line).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "")).order_by(Res_line._recid).all():

                            room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: not room_avail_list.sleeping and room_avail_list.zikatnr == res_line.zikatnr), first=True)

                            if room_avail_list:

                                zimmer = db_session.query(Zimmer).filter(
                                         (Zimmer.zinr == res_line.zinr) & not_ (Zimmer.sleeping)).first()

                                if zimmer:

                                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                    if segment and segment.vip_level == 0:
                                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                        i = i + 1
                        datum = datum + timedelta(days=1)
                from_date = curr_date
                to_date = from_date + timedelta(days=num_day)

                if to_date > co_date:
                    to_date = co_date
                i = 1
                for datum in date_range(from_date,to_date) :

                    for t_kontline in query(t_kontline_data, filters=(lambda t_kontline: t_kontline.betriebsnr == 0 and t_kontline.ankunft <= datum and t_kontline.abreise >= datum and t_kontline.kontstat == 1)):

                        if datum >= (ci_date + timedelta(days=t_kontline.ruecktage)):
                            sum_list.summe[i - 1] = sum_list.summe[i - 1] + t_kontline.zimmeranz

                            room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.zikatnr == t_kontline.zikatnr and room_avail_list.sleeping), first=True)

                            if not room_avail_list:

                                room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping), first=True)

                            if room_avail_list:
                                room_avail_list.allotment[i - 1] = room_avail_list.allotment[i - 1] + t_kontline.zimmeranz
                    i = i + 1

                for room_avail_list in query(room_avail_list_data):
                    for i in range(1,num_day + 1) :
                        room_avail_list.coom[i - 1] = to_string(room_avail_list.room[i - 1], "->>>,>>>,>>9")

            elif statsort == 2:
                create_browse1()
            else:
                sum_list = Sum_list()
                sum_list_data.append(sum_list)

                sum_list.bezeich = translateExtended ("Avail before Allotm", lvcarea, "")

                for zimkateg in db_session.query(Zimkateg).filter(
                         (Zimkateg.verfuegbarkeit)).order_by(Zimkateg.typ, Zimkateg.zikatnr).all():

                    rmcat_list = query(rmcat_list_data, filters=(lambda rmcat_list: rmcat_list.zikatnr == zimkateg.zikatnr and rmcat_list.sleeping), first=True)

                    if rmcat_list:
                        room_avail_list = Room_avail_list()
                        room_avail_list_data.append(room_avail_list)

                        i = 1
                        while i <= (num_day + 1) :
                            room_avail_list.room[i - 1] = rmcat_list.anzahl
                            i = i + 1
                        room_avail_list.i_typ = zimkateg.typ
                        room_avail_list.zikatnr = zimkateg.zikatnr
                        room_avail_list.bezeich = zimkateg.kurzbez +\
                                " - " + to_string(zimkateg.overbooking, ">>9")

                zimkateg_obj_list = {}
                for zimkateg in db_session.query(Zimkateg).filter(
                         ((Zimkateg.zikatnr.in_(list(set([rmcat_list.zikatnr for rmcat_list in rmcat_list_data if ~rmcat_list.sleeping])))))).order_by(Zimkateg.typ, Zimkateg.zikatnr).all():
                    if zimkateg_obj_list.get(zimkateg._recid):
                        continue
                    else:
                        zimkateg_obj_list[zimkateg._recid] = True

                    rmcat_list = query(rmcat_list_data, (lambda rmcat_list: (zimkateg.zikatnr == rmcat_list.zikatnr)), first=True)
                    room_avail_list = Room_avail_list()
                    room_avail_list_data.append(room_avail_list)

                    room_avail_list.sleeping = False
                    i = 1
                    while i <= (num_day + 1) :
                        room_avail_list.room[i - 1] = rmcat_list.anzahl
                        i = i + 1
                    room_avail_list.i_typ = zimkateg.typ
                    room_avail_list.zikatnr = zimkateg.zikatnr
                    room_avail_list.bezeich = zimkateg.kurzbez +\
                            " - " + to_string(zimkateg.overbooking, ">>9")


                    datum = curr_date
                    for i in range(1,num_day + 1) :

                        res_line_obj_list = {}
                        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr) & not_ (Zimmer.sleeping)).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.zikatnr == room_avail_list.zikatnr) & (Res_line.zinr != "") & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True

                            if not vhp_limited:
                                do_it = True
                            else:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                        datum = datum + timedelta(days=1)

                outorder_obj_list = {}
                outorder = Outorder()
                zimmer = Zimmer()
                for outorder.gespstart, outorder.gespende, outorder.zinr, outorder.betriebsnr, outorder._recid, zimmer.zikatnr, zimmer.sleeping, zimmer._recid in db_session.query(Outorder.gespstart, Outorder.gespende, Outorder.zinr, Outorder.betriebsnr, Outorder._recid, Zimmer.zikatnr, Zimmer.sleeping, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
                    datum = curr_date

                    room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.zikatnr == zimmer.zikatnr and room_avail_list.sleeping), first=True)

                    if room_avail_list:
                        for i in range(1,num_day + 1) :

                            if datum >= outorder.gespstart and datum <= outorder.gespende:

                                if outorder.betriebsnr == 2:
                                    om_list[i - 1] = om_list[i - 1] + 1
                                    om_flag = True
                                else:
                                    ooo_list[i - 1] = ooo_list[i - 1] + 1
                                    room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                            datum = datum + timedelta(days=1)
                i = 1
                datum = curr_date
                while i <= (num_day + 1) :

                    for res_line in db_session.query(Res_line).filter(
                             (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

                        room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping and room_avail_list.zikatnr == res_line.zikatnr), first=True)

                        if room_avail_list:
                            do_it = True

                            if res_line.zinr != "":

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                                do_it = zimmer.sleeping

                            if do_it and vhp_limited:

                                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                                do_it = None != segment and segment.vip_level == 0

                            if do_it:
                                room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - res_line.zimmeranz

                    for kontline in db_session.query(Kontline).filter(
                             (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                        room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping and room_avail_list.zikatnr == kontline.zikatnr), first=True)

                        if room_avail_list:
                            room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - kontline.zimmeranz
                    i = i + 1
                    datum = datum + timedelta(days=1)
                for i in range(1,num_day + 1) :
                    sum_list.summe[i - 1] = 0

                    for room_avail_list in query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping)):
                        sum_list.summe[i - 1] = sum_list.summe[i - 1] + room_avail_list.room[i - 1]

                if mi_inactive:
                    i = 1
                    datum = curr_date
                    while i <= (num_day + 1) :

                        for res_line in db_session.query(Res_line).filter(
                                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.zinr != "")).order_by(Res_line._recid).all():

                            room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: not room_avail_list.sleeping and room_avail_list.zikatnr == res_line.zikatnr), first=True)

                            if room_avail_list:

                                zimmer = db_session.query(Zimmer).filter(
                                         (Zimmer.zinr == res_line.zinr) & not_ (Zimmer.sleeping)).first()

                                if zimmer:

                                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                                    if segment and segment.vip_level == 0:
                                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - 1
                        i = i + 1
                        datum = datum + timedelta(days=1)
                create_tentative()
                from_date = curr_date
                to_date = from_date + timedelta(days=num_day)

                if to_date > co_date:
                    to_date = co_date
                i = 1
                for datum in date_range(from_date,to_date) :

                    for t_kontline in query(t_kontline_data, filters=(lambda t_kontline: t_kontline.betriebsnr == 0 and t_kontline.ankunft <= datum and t_kontline.abreise >= datum and t_kontline.kontstat == 1)):

                        if datum >= (ci_date + timedelta(days=t_kontline.ruecktage)):
                            sum_list.summe[i - 1] = sum_list.summe[i - 1] + t_kontline.zimmeranz

                            room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.zikatnr == t_kontline.zikatnr and room_avail_list.sleeping), first=True)

                            if not room_avail_list:

                                room_avail_list = query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.sleeping), first=True)

                            if room_avail_list:
                                room_avail_list.allotment[i - 1] = room_avail_list.allotment[i - 1] + t_kontline.zimmeranz
                    i = i + 1
                for i in range(1,num_day + 1) :

                    if room_avail_list:
                        room_avail_list.allotment[i - 1] = room_avail_list.allotment[i - 1] - res_allot[i - 1]

                for room_avail_list in query(room_avail_list_data):
                    for i in range(1,num_day + 1) :
                        room_avail_list.coom[i - 1] = to_string(room_avail_list.room[i - 1], "->>>,>>>,>>9")


    def create_browse1():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data

        datum1:date = None
        abreise1:date = None
        do_it:bool = False
        tmp_list:List[int] = create_empty_list(300,0)
        avail_list:List[int] = create_empty_list(300,0)
        om_flag:bool = False
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Total Active Rooms", lvcarea, "")
        for i in range(1,num_day + 1) :
            room_avail_list.room[i - 1] = tot_room
            tmp_list[i - 1] = tot_room
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Out-of-order", lvcarea, "")

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

            if zimmer.sleeping:
                datum = curr_date
                for i in range(1,num_day + 1) :

                    if datum >= outorder.gespstart and datum <= outorder.gespende:
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + 1
                        tmp_list[i - 1] = tmp_list[i - 1] - 1
                    datum = datum + timedelta(days=1)
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Occupied", lvcarea, "")
        for i in range(1,num_day + 1) :
            avail_list[i - 1] = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resstatus == 6) & (Res_line.active_flag == 1) & (Res_line.abreise >= curr_date) & (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            if not vhp_limited:
                do_it = True
            else:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                do_it = None != segment and segment.vip_level == 0

            if do_it:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if zimmer.sleeping:
                    datum1 = curr_date + timedelta(days=num_day)

                    if datum1 > co_date:
                        datum1 = co_date
                    abreise1 = res_line.abreise - timedelta(days=1)

                    if abreise1 < datum1:
                        datum1 = abreise1
                    i = 1
                    for datum in date_range(curr_date,datum1) :
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + 1
                        tmp_list[i - 1] = tmp_list[i - 1] - 1
                        i = i + 1
                    i = (res_line.abreise - curr_date + 1).days

                    if i >= 1 and i <= num_day:
                        avail_list[i - 1] = avail_list[i - 1] + 1
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Rentable", lvcarea, "")
        for i in range(1,num_day + 1) :
            room_avail_list.room[i - 1] = tmp_list[i - 1]
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Guaranted", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= (num_day + 1) :

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus == 1) & (Res_line.zikatnr == zimkateg.zikatnr) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz
                i = i + 1
                datum = datum + timedelta(days=1)
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("6 PM", lvcarea, "")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})

        if htparam.finteger != 0:
            room_avail_list.bezeich = to_string(htparam.finteger) + " " + translateExtended ("PM", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= (num_day + 1) :

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus == 2) & (Res_line.zikatnr == zimkateg.zikatnr) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz
                i = i + 1
                datum = datum + timedelta(days=1)
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Oral Confirmed", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= (num_day + 1) :

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus == 5) & (Res_line.zikatnr == zimkateg.zikatnr) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] - res_line.zimmeranz
                i = i + 1
                datum = datum + timedelta(days=1)
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.bezeich = translateExtended ("Global Reservation", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= (num_day + 1) :

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.kontignr > 0) & (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.zikatnr == zimkateg.zikatnr) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                    room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + kontline.zimmeranz
                    tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    do_it = True

                    if res_line.zinr != "":

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                        do_it = zimmer.sleeping

                    if res_line.resstatus == 3 and not incl_tentative:
                        do_it = False

                    if do_it and vhp_limited:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
                        do_it = None != segment and segment.vip_level == 0

                    if do_it:
                        room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - res_line.zimmeranz
                        tmp_list[i - 1] = tmp_list[i - 1] + res_line.zimmeranz
                i = i + 1
                datum = datum + timedelta(days=1)
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.avail_flag = True
        room_avail_list.bezeich = translateExtended ("Total Availability", lvcarea, "")


        for i in range(1,num_day + 1) :
            room_avail_list.room[i - 1] = tmp_list[i - 1]
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.allot_flag = True
        room_avail_list.bezeich = translateExtended ("Allotments", lvcarea, "")


        from_date = curr_date
        to_date = from_date + timedelta(days=num_day)

        if to_date > co_date:
            to_date = co_date
        i = 1
        for datum in date_range(from_date,to_date) :

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.betriebsnr == 0) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                if datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                    room_avail_list.room[i - 1] = room_avail_list.room[i - 1] + kontline.zimmeranz
                    tmp_list[i - 1] = tmp_list[i - 1] - kontline.zimmeranz
            i = i + 1
        for i in range(1,num_day + 1) :
            room_avail_list.room[i - 1] = room_avail_list.room[i - 1] - res_allot[i - 1]
            tmp_list[i - 1] = tmp_list[i - 1] + res_allot[i - 1]
        room_avail_list = Room_avail_list()
        room_avail_list_data.append(room_avail_list)

        room_avail_list.avail_flag = True
        room_avail_list.bezeich = translateExtended ("Avail After Allotm", lvcarea, "")


        for i in range(1,num_day + 1) :
            room_avail_list.room[i - 1] = tmp_list[i - 1]

        for room_avail_list in query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.bezeich != "")):
            for i in range(1,num_day + 1) :
                room_avail_list.coom[i - 1] = to_string(room_avail_list.room[i - 1], "->>>,>>>,>>9")
        datum = curr_date
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = translateExtended ("Tentative", lvcarea, "")

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus == 3) & (((Res_line.ankunft <= datum) & (Res_line.abreise > datum)) | ((Res_line.ankunft == datum) & (Res_line.abreise == datum))) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            i = 1
            while i <= (num_day + 1) :
                sum_list.summe[i - 1] = sum_list.summe[i - 1] + 1
                i = i + 1
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = translateExtended ("Waiting List", lvcarea, "")

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            i = 1
            datum = curr_date
            while i <= (num_day + 1) :

                for resplan in db_session.query(Resplan).filter(
                         (Resplan.datum == datum) & (Resplan.zikatnr == zimkateg.zikatnr)).order_by(Resplan._recid).all():
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + resplan.anzzim[3]
                i = i + 1
                datum = datum + timedelta(days=1)
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = translateExtended ("Exp.Departure", lvcarea, "")
        for i in range(1,num_day + 1) :
            sum_list.summe[i - 1] = avail_list[i - 1]
        om_flag = False
        sum_list = Sum_list()
        sum_list_data.append(sum_list)

        sum_list.bezeich = translateExtended ("Off-Market", lvcarea, "")

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.betriebsnr == 2)).order_by(Outorder._recid).all():
            datum = curr_date
            for i in range(1,num_day + 1) :

                if datum >= outorder.gespstart and datum <= outorder.gespende:
                    sum_list.summe[i - 1] = sum_list.summe[i - 1] + 1
                    om_flag = True
                datum = datum + timedelta(days=1)

        if not om_flag:
            sum_list_data.remove(sum_list)


    def clear_it():

        nonlocal room_list_data, sum_list_data, lvcarea, logid, logstr, cdstr, col_label, curr_day, datum, tot_room, i, ci_date, co_date, from_date, to_date, last_option, wlist, dlist, j, dd, mm, yyyy, num_day, htl_name, htl_adr, htl_tel, res_allot, week_list, rpt_title, curr_time, kontline, res_line, zimmer, paramtext, htparam, arrangement, zimkateg, queasy, artikel, fixleist, reslin_queasy, reservation, segment, outorder, resplan
        nonlocal pvilanguage, vhp_limited, op_type, printer_nr, call_from, adult_child_str, statsort, dispsort, curr_date, incl_tentative, mi_inactive, show_rate, indgastnr, qci_zinr
        nonlocal qci_zimmer


        nonlocal sum_list, room_avail_list, date_list, room_list, rate_list, created_list, t_kontline, rmcat_list, tmp_resline, tmp_extra, temp_art, qci_zimmer, buff_ratelist
        nonlocal sum_list_data, room_avail_list_data, date_list_data, room_list_data, rate_list_data, created_list_data, t_kontline_data, rmcat_list_data, tmp_resline_data, tmp_extra_data, temp_art_data


        sum_list_data.clear()
        room_avail_list_data.clear()

    logid = random.randint(1, 99999)

    if curr_date == None:
        cdstr = "NULL"
    else:
        cdstr = to_string(curr_date)
    logstr = "logid=" + to_string(logid) + "|ACS=" + adult_child_str + "|CD=" + cdstr

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte
    week_list[0] = translateExtended ("Monday ", lvcarea, "")
    week_list[1] = translateExtended ("Tuesday ", lvcarea, "")
    week_list[2] = translateExtended ("Wednesday ", lvcarea, "")
    week_list[3] = translateExtended ("Thursday ", lvcarea, "")
    week_list[4] = translateExtended ("Friday ", lvcarea, "")
    week_list[5] = translateExtended ("Saturday ", lvcarea, "")
    week_list[6] = translateExtended ("Sunday ", lvcarea, "")

    if curr_date == None:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if num_entries(adult_child_str, ",") > 2:
        mm = to_int(substring(entry(2, adult_child_str, ",") , 0, 2))
        dd = to_int(substring(entry(2, adult_child_str, ",") , 2, 2))
        yyyy = to_int(substring(entry(2, adult_child_str, ",") , 4, 4))
        co_date = date_mdy(mm, dd, yyyy) + timedelta(days=1)


        num_day = (co_date - curr_date).days

    if qci_zinr != "":

        qci_zimmer = get_cache (Zimmer, {"zinr": [(eq, qci_zinr)]})
    i = 1
    while i <= (num_day + 1) :
        date_list = Date_list()
        date_list_data.append(date_list)

        date_list.counter = i
        date_list.datum = curr_date + timedelta(days=i - 1)
        i = i + 1

    if op_type == 0:
        create_browse()

        if statsort == 1:
            calc_extra(curr_date)

        if not show_rate:
            create_room_list()
        else:
            create_rate_list()
    elif op_type == 1:
        # design_lnl()
        pass
    elif op_type == 2:
        # print_lnl()
        pass
    elif op_type == 3:
        # print_txt()
        pass
    elif op_type == 4:
        # clear_it()
        pass

    return generate_output()