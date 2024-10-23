from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from sqlalchemy import func
import re
from functions.ratecode_rate import ratecode_rate
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Paramtext, Kontline, Htparam, Zkstat, Zinrstat, Outorder, Genstat, Res_line, Guest, Zimmer, Reservation, Queasy, Guestseg, Reslin_queasy, Waehrung, Arrangement, Guest_pr, Katpreis, Artikel, Argt_line, Zimkateg

segm1_list_list, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":str, "bezeich1":str})
argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":str, "bezeich":str})

def cr_anfcastbl(pvilanguage:int, vhp_limited:bool, dlist:str, op_type:int, printer_nr:int, call_from:int, txt_file:str, monthdayselect:int, roompaxselect:int, nationselect:str, all_segm:bool, all_argt:bool, all_zikat:bool, from_month:str, show_rmrev:bool, incl_tent:bool, incl_wait:bool, incl_glob:bool, segm1_list_list:[Segm1_list], argt_list_list:[Argt_list], zikat_list_list:[Zikat_list]):
    tt_month_str_list = []
    room_list_list = []
    rev_list_list = []
    sum_list_list = []
    segm_list_list = []
    lvcarea:str = "annual-fcast"
    rmsharer:bool = False
    week_list:List[str] = [" Jan ", " Feb ", " Mar ", " Apr ", " May ", " Jun ", " Jul ", " Aug ", " Sep ", " Oct ", " Nov ", " Dec "]
    wlist:str = ""
    month_str:List[str] = create_empty_list(12,"")
    rm_serv:bool = False
    foreign_rate:bool = False
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    out_type:str = ""
    dis_type:str = ""
    rm_occ:str = ""
    pax_occ:str = ""
    avl_rm:str = ""
    occ_proz:str = ""
    i:int = 0
    j:int = 0
    datum:date = None
    ci_date:date = None
    curr_day:int = 0
    tot_room:int = 0
    inactive:int = 0
    mm:int = 0
    yy:int = 0
    diff_one:int = 0
    ok:bool = False
    pax:int = 0
    rev_array:List[decimal] = create_empty_list(12,to_decimal("0"))
    curr_date:date = None
    date1:date = None
    contcode:str = ""
    ct:str = ""
    room_ooo:List[decimal] = create_empty_list(12,to_decimal("0"))
    paramtext = kontline = htparam = zkstat = zinrstat = outorder = genstat = res_line = guest = zimmer = reservation = queasy = guestseg = reslin_queasy = waehrung = arrangement = guest_pr = katpreis = artikel = argt_line = zimkateg = None

    segm1_list = argt_list = zikat_list = room_list = sum_list = segm_list = rev_list = tt_month_str = kbuff = r1_list = r2_list = r3_list = r4_list = r5_list = r6_list = r7_list = r8_list = None

    room_list_list, Room_list = create_model("Room_list", {"nr":int, "tag":int, "bezeich":str, "room":[int,12], "pax":[int,12], "coom":[str,12], "rstat":int})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "summe":[int,12]})
    segm_list_list, Segm_list = create_model("Segm_list", {"segmentcode":int, "bezeich":str, "bezeich1":str, "segm":[int,12]})
    rev_list_list, Rev_list = create_model("Rev_list", {"bezeich":str, "str1":[str,6]})
    tt_month_str_list, Tt_month_str = create_model("Tt_month_str", {"i_counter":int, "month_str":str})

    Kbuff = create_buffer("Kbuff",Kontline)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list
        return {"tt-month-str": tt_month_str_list, "room-list": room_list_list, "rev-list": rev_list_list, "sum-list": sum_list_list, "segm-list": segm_list_list, "segm1-list": segm1_list_list, "argt-list": argt_list_list, "zikat-list": zikat_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        rate:decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def assign_it(j:int, datum:date, from_date:date):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_rmrev:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")

        if datum == res_line.abreise:
            pass
        else:

            if res_line.zipreis > 0:
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, j, from_date))
            rev_array[j - 1] = rev_array[j - 1] + net_lodg


    def create_browse11():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        from_date:date = None
        to_date:date = None
        datum1:date = None
        datum2:date = None
        abreise1:date = None
        cur_date:date = None
        anz:List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        tmp_list:List[int] = create_empty_list(12,0)
        tmp_i:List[int] = create_empty_list(12, 0)
        last_resnr:int = 0
        i:int = 0
        j:int = 0
        do_it:bool = False
        lodging:decimal = to_decimal("0.0")
        datum3:date = None
        ooo_room:int = 0
        d2:date = None
        R1_list = Room_list
        r1_list_list = room_list_list
        R2_list = Room_list
        r2_list_list = room_list_list
        R3_list = Room_list
        r3_list_list = room_list_list
        R4_list = Room_list
        r4_list_list = room_list_list
        R5_list = Room_list
        r5_list_list = room_list_list
        R6_list = Room_list
        r6_list_list = room_list_list
        R7_list = Room_list
        r7_list_list = room_list_list
        R8_list = Room_list
        r8_list_list = room_list_list
        room_list_list.clear()
        for i in range(1,12 + 1) :
            rev_array[i - 1] = 0
        for i in range(1,31 + 1) :
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.tag = i
            room_list.bezeich = " " + to_string(i, ">9 ")

            if incl_tent or incl_wait:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.tag = i
                room_list.rstat = 1
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 32
        room_list.bezeich = "==============="


        for i in range(1,12 + 1) :
            room_list.coom[i - 1] = "======="
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 33
        room_list.bezeich = translateExtended (" Room Occupied", lvcarea, "")


        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 34
        room_list.bezeich = translateExtended (" Saleable Rooms", lvcarea, "")


        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 35
        room_list.bezeich = " Occupancy (%)"


        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 36
        room_list.bezeich = translateExtended ("Person Occupied", lvcarea, "")

        if incl_tent:
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.tag = 37
            room_list.bezeich = translateExtended ("Tentative-Occ %", lvcarea, "")

            r5_list = query(r5_list_list, filters=(lambda r5_list: r5_list.tag == 37), first=True)

        r1_list = query(r1_list_list, filters=(lambda r1_list: r1_list.tag == 33), first=True)

        r2_list = query(r2_list_list, filters=(lambda r2_list: r2_list.tag == 34), first=True)

        r3_list = query(r3_list_list, filters=(lambda r3_list: r3_list.tag == 35), first=True)

        r4_list = query(r4_list_list, filters=(lambda r4_list: r4_list.tag == 36), first=True)
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 38
        room_list.bezeich = translateExtended ("SaleRoom w/ OOO", lvcarea, "")


        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.tag = 39
        room_list.bezeich = translateExtended ("Occ(%) w/ OOO", lvcarea, "")

        r6_list = query(r6_list_list, filters=(lambda r6_list: r6_list.tag == 38), first=True)

        r7_list = query(r7_list_list, filters=(lambda r7_list: r7_list.tag == 39), first=True)

        r8_list = query(r8_list_list, filters=(lambda r8_list: r8_list.r7_list.tag == 39), first=True)
        mm = to_int(substring(from_month, 0, 2)) + diff_one
        yy = to_int(substring(from_month, 2, 4))

        if diff_one == 1 and mm == 13:
            mm = 1
            yy = yy + 1

        elif diff_one == -1 and mm == 0:
            mm = 12
            yy = yy - 1
        curr_date = date_mdy(mm, 1, yy)
        from_month = to_string(get_month(curr_date) , "99") + to_string(get_year(curr_date) , "9999")
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        j = mm - 1
        for i in range(1,12 + 1) :
            j = j + 1

            if j > 12:
                j = j - 12
            tmp_list[i - 1] = anz[j - 1]

            if j == 2:

                if mm <= 2:

                    if (yy % 4) == 0:
                        tmp_list[i - 1] = 29
                else:

                    if ((yy + 1) % 4) == 0:
                        tmp_list[i - 1] = 29
        curr_date = date_mdy(mm, 1, yy)
        to_date = date_mdy(mm, 1, yy + timedelta(days=1)) - timedelta(days=1)

        if curr_date >= ci_date:
            from_date = curr_date
        else:
            from_date = ci_date

        if to_date < (ci_date - timedelta(days=1)):
            datum2 = to_date
        else:
            datum2 = ci_date - timedelta(days=1)

        if curr_date < ci_date:

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= curr_date) & (Zkstat.datum <= datum2)).order_by(Zkstat._recid).all():
                datum = zkstat.datum
                j = get_month(datum) - mm + 1

                if j <= 0:
                    j = j + 12
                tmp_i[j - 1] = 1

                if get_month(zkstat.datum) == get_month(datum2):
                    tmp_i[j - 1] = 2

                r2_list = query(r2_list_list, filters=(lambda r2_list: r2_list.tag == 34), first=True)

                if r2_list:
                    r2_list.room[j - 1] = r2_list.room[j - 1] + zkstat.anz100
        for i in range(1,12 + 1) :

            if tmp_i[i - 1] == 0:
                r2_list.room[i - 1] = tot_room * tmp_list[i - 1]

            if tmp_i[i - 1] == 2:
                r2_list.room[i - 1] = r2_list.room[i - 1] + (tot_room * (tmp_list[i - 1] - get_day(datum2)))

        if curr_date < ci_date:

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= curr_date) & (Zinrstat.datum <= datum2) & (func.lower(Zinrstat.zinr) == ("ooo").lower())).order_by(Zinrstat._recid).all():
                datum = zinrstat.datum
                j = get_month(datum) - mm + 1

                if j <= 0:
                    j = j + 12
                tmp_i[j - 1] = 1

                if get_month(zinrstat.datum) == get_month(datum3):
                    tmp_i[j - 1] = 2

                r6_list = query(r6_list_list, filters=(lambda r6_list: r6_list.tag == 38), first=True)

                if r6_list:
                    r6_list.room[j - 1] = (r6_list.room[j - 1] + zinrstat.zimmeranz)
        else:

            for outorder in db_session.query(Outorder).filter(
                     (not_ (Outorder.gespstart > to_date)) & (not_ (Outorder.gespende <= from_date))).order_by(Outorder._recid).all():
                ooo_room = ooo_room + 1

            r6_list = query(r6_list_list, filters=(lambda r6_list: r6_list.tag == 38), first=True)

            if r6_list:
                r6_list.room[j - 1] = (r6_list.room[j - 1] + ooo_room)

        if curr_date < ci_date:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= curr_date) & (Genstat.datum <= datum2) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat._recid).all():
                do_it = True
                rmsharer = (genstat.resstatus == 13)

                if vhp_limited:
                    do_it = True

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8 and genstat.logis == 0:
                    do_it = False

                if do_it and not all_segm:

                    segm1_list = query(segm1_list_list, filters=(lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                    do_it = None ! == segm1_list

                if do_it and not all_argt:

                    argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                    do_it = None ! == argt_list

                if do_it and not all_zikat:

                    zikat_list = query(zikat_list_list, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                    do_it = None ! == zikat_list

                if do_it:
                    datum = genstat.datum
                    j = get_month(datum) - mm + 1

                    if j <= 0:
                        j = j + 12

                    room_list = query(room_list_list, filters=(lambda room_list: room_list.tag == get_day(datum)), first=True)

                    if roompaxselect == 0:

                        if nationselect == "":

                            if not rmsharer:
                                room_list.room[j - 1] = room_list.room[j - 1] + 1
                                room_list.pax[j - 1] = room_list.pax[j - 1] + genstat.erwachs + genstat.kind1 +\
                                    genstat.kind2 + genstat.gratis + genstat.kind3

                            if show_rmrev:
                                rev_array[j - 1] = rev_array[j - 1] + genstat.logis
                        else:

                            if not rmsharer:
                                room_list.room[j - 1] = room_list.room[j - 1] + 1
                                room_list.pax[j - 1] = room_list.pax[j - 1] + genstat.erwachs +\
                                    genstat.kind1 + genstat.kind2 + genstat.gratis + genstat.kind3


                    else:

                        if nationselect == "":

                            if not rmsharer:
                                room_list.pax[j - 1] = room_list.pax[j - 1] + genstat.erwachs + genstat.kind1 +\
                                        genstat.kind2 + genstat.gratis + genstat.kind3
                                room_list.room[j - 1] = room_list.room[j - 1] + genstat.erwachs + genstat.kind1 +\
                                        genstat.kind2 + genstat.gratis + genstat.kind3

                            if show_rmrev:
                                rev_array[j - 1] = rev_array[j - 1] + genstat.logis
                        else:

                            if not rmsharer:
                                room_list.pax[j - 1] = room_list.pax[j - 1] + genstat.erwachs + genstat.kind1 +\
                                        genstat.kind2 + genstat.gratis + genstat.kind3
                                room_list.room[j - 1] = room_list.room[j - 1] + genstat.erwachs + genstat.kind1 +\
                                    genstat.kind2 + genstat.gratis + genstat.kind3


        last_resnr = -1

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                     ((Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)) & (not_ (Res_line.ankunft > to_date)) & (not_ (Res_line.abreise <= from_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.active_flag <= 1)).order_by(Res_line.resnr).all():

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrmember)).first()

                if nationselect != "":

                    if not guest or nationselect != guest.nation1:
                        continue

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.zinr == res_line.zinr)).first()

                if last_resnr != res_line.resnr:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()
                    last_resnr = res_line.resnr
                do_it = True

                if not incl_tent and res_line.resstatus == 3:
                    do_it = False

                if not incl_wait and res_line.resstatus == 4:
                    do_it = False

                if do_it and zimmer:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 14) & (Queasy.char1 == res_line.zinr) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False

                if do_it and not all_segm:

                    segm1_list = query(segm1_list_list, filters=(lambda segm1_list: segm1_list.segm == reservation.segmentcode and segm1_list.selected), first=True)
                    do_it = None ! == segm1_list

                if do_it and not all_argt:

                    argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argt == res_line.arrangement and argt_list.selected), first=True)
                    do_it = None ! == argt_list

                if do_it and not all_zikat:

                    zikat_list = query(zikat_list_list, filters=(lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                    do_it = None ! == zikat_list

                if do_it and (res_line.kontignr < 0):

                    if all_segm:
                        do_it = True
                    else:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == reservation.gastnr)).first()

                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

                        if not guestseg:

                            guestseg = db_session.query(Guestseg).filter(
                                     (Guestseg.gastnr == guest.gastnr)).first()

                        if guestseg:

                            segm1_list = query(segm1_list_list, filters=(lambda segm1_list: segm1_list.segm == guestseg.segmentcode and segm1_list.selected), first=True)
                            do_it = not None ! == segm1_list

                if do_it:

                    if res_line.ankunft >= from_date:
                        datum1 = res_line.ankunft
                    else:
                        datum1 = from_date

                    if res_line.abreise <= to_date:
                        datum2 = res_line.abreise - timedelta(days=1)
                    else:
                        datum2 = to_date
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                        j = get_month(datum) - mm + 1

                        if j <= 0:
                            j = j + 12

                        if res_line.resstatus != 3 and res_line.resstatus != 4:

                            room_list = query(room_list_list, filters=(lambda room_list: room_list.tag == get_day(datum) and room_list.rstat == 0), first=True)
                        else:

                            room_list = query(room_list_list, filters=(lambda room_list: room_list.tag == get_day(datum) and room_list.rstat == 1), first=True)

                        if roompaxselect == 0 and res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list.room[j - 1] = room_list.room[j - 1] + res_line.zimmeranz
                            room_list.pax[j - 1] = room_list.pax[j - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                            assign_it(j, datum, from_date)

                        elif roompaxselect != 0:
                            room_list.room[j - 1] = room_list.room[j - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                            room_list.pax[j - 1] = room_list.pax[j - 1] + (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] + res_line.gratis) * res_line.zimmeranz
                            assign_it(j, datum, from_date)

        if incl_glob:
            for datum in date_range(from_date,to_date) :
                j = get_month(datum) - mm + 1

                if j <= 0:
                    j = j + 12

                room_list = query(room_list_list, filters=(lambda room_list: room_list.tag == get_day(datum)), first=True)

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                    guest = db_session.query(Guest).filter(
                             (Guest.gastnr == kontline.gastnr)).first()

                    if nationselect != "":

                        if not guest or nationselect != guest.nation1:
                            continue
                    do_it = True

                    if do_it and not all_argt:

                        argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argt == kontline.arrangement and argt_list.selected), first=True)
                        do_it = None ! == argt_list

                    if do_it and not all_zikat:

                        zikat_list = query(zikat_list_list, filters=(lambda zikat_list: zikat_list.zikatnr == kontline.zikatnr and zikat_list.selected), first=True)
                        do_it = None ! == zikat_list

                    if do_it and not all_segm:

                        guest = db_session.query(Guest).filter(
                                 (Guest.gastnr == kontline.gastnr)).first()

                        guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

                        if not guestseg:

                            guestseg = db_session.query(Guestseg).filter(
                                     (Guestseg.gastnr == guest.gastnr)).first()

                        if guestseg:

                            segm1_list = query(segm1_list_list, filters=(lambda segm1_list: segm1_list.segm == guestseg.segmentcode and segm1_list.selected), first=True)
                            do_it = None ! == segm1_list

                    if do_it:

                        if roompaxselect == 0:
                            room_list.room[j - 1] = room_list.room[j - 1] + kontline.zimmeranz

                        elif roompaxselect != 0:
                            room_list.room[j - 1] = room_list.room[j - 1] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz
                            room_list.pax[j - 1] = room_list.pax[j - 1] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    room_list.room[j - 1] = room_list.room[j - 1] - res_line.zimmeranz

                    kbuff = db_session.query(Kbuff).filter(
                             (Kbuff.gastnr == res_line.gastnr) & (Kbuff.ankunft == datum) & (Kbuff.zikatnr == res_line.zikatnr) & (Kbuff.betriebsnr == 1)).first()

                    if kbuff:
                        room_list.pax[j - 1] = room_list.pax[j - 1] - (kbuff.erwachs + kbuff.kind1) * res_line.zimmeranz
                    else:
                        room_list.pax[j - 1] = room_list.pax[j - 1] - res_line.erwachs * res_line.zimmeranz

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.tag <= 31)):
            for i in range(1,12 + 1) :

                if room_list.room[i - 1] != 0 or room_list.tag <= 28:
                    room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>,>>9")

                if roompaxselect == 0:
                    r1_list.room[i - 1] = r1_list.room[i - 1] + room_list.room[i - 1]
                r4_list.room[i - 1] = r4_list.room[i - 1] + room_list.pax[i - 1]

                if incl_tent and room_list.rstat == 1:
                    r5_list.room[i - 1] = r5_list.room[i - 1] + room_list.room[i - 1]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.tag >= 29 and room_list.tag <= 31)):
            for i in range(1,12 + 1) :

                if room_list.room[i - 1] == 0 and room_list.tag <= tmp_list[i - 1]:
                    room_list.coom[i - 1] = " 0"
        for i in range(1,12 + 1) :

            if roompaxselect == 0:
                r1_list.coom[i - 1] = to_string(r1_list.room[i - 1], "->>,>>9")

                if r2_list.room[i - 1] != 0:
                    r2_list.room[i - 1] = r2_list.room[i - 1]
                    r2_list.coom[i - 1] = to_string(r2_list.room[i - 1], "->>,>>9")
                    r3_list.coom[i - 1] = to_string(r1_list.room[i - 1] / r2_list.room[i - 1] * 100, "->>9.99")

                    if incl_tent:
                        r5_list.coom[i - 1] = to_string(r5_list.room[i - 1] / r2_list.room[i - 1] * 100, "->>9.99")
                    r6_list.coom[i - 1] = to_string(r2_list.room[i - 1] - r6_list.room[i - 1], "->>,>>9")
                    room_ooo[i - 1] = r1_list.room[i - 1] / (r2_list.room[i - 1] - r6_list.room[i - 1]) * 100
                    r7_list.coom[i - 1] = to_string(room_ooo[i - 1], "->>9.99")
            r4_list.coom[i - 1] = to_string(r4_list.room[i - 1], "->>,>>9")


    def calculate_zipreis(bill_date:date, roomrate:decimal):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        rm_rate:decimal = to_decimal("0.0")
        add_it:bool = False
        qty:int = 0
        qty2:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
        child1:int = 0
        fix_rate:bool = False
        post_date:date = None
        curr_zikatnr:int = 0
        w_day:int = 0
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
        w1 = None
        publish_rate:decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate)

        W1 =  create_buffer("W1",Waehrung)
        qty2 = res_line.zimmeranz

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnr)).first()

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)
            roomrate = cal_lodging(bill_date, roomrate)

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == res_line.gastnr)).first()

        if guest_pr:
            contcode = guest_pr.code
            ct = res_line.zimmer_wunsch

            if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
                ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
                contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)
            post_date = bill_date

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 18) & (Queasy.number1 == res_line.reserve_int)).first()

            if queasy and queasy.logi3:
                post_date = res_line.ankunft
            ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
            kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

            if res_line.l_zuordnung[0] != 0:
                curr_zikatnr = res_line.l_zuordnung[0]
            else:
                curr_zikatnr = res_line.zikatnr
            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, post_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
            roomrate =  to_decimal(rm_rate)
            roomrate = cal_lodging(bill_date, roomrate)

            return generate_inner_output()
        else:
            w_day = wd_array[get_weekday(bill_date - 1) - 1]

            katpreis = db_session.query(Katpreis).filter(
                     (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= (bill_date - timedelta(days=1))) & (Katpreis.endperiode >= (bill_date - timedelta(days=1))) & (Katpreis.betriebsnr == w_day)).first()

            if not katpreis:

                katpreis = db_session.query(Katpreis).filter(
                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= (bill_date - timedelta(days=1))) & (Katpreis.endperiode >= (bill_date - timedelta(days=1))) & (Katpreis.betriebsnr == 0)).first()

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(bill_date) - 1]

            katpreis = db_session.query(Katpreis).filter(
                     (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

            if not katpreis:

                katpreis = db_session.query(Katpreis).filter(
                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)
                roomrate = cal_lodging(bill_date, roomrate)
            roomrate = cal_lodging(bill_date, roomrate)

        return generate_inner_output()


    def cal_lodging(bill_date:date, zipreis:decimal):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        rate:decimal = to_decimal("0.0")
        lodg_betrag:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        vat2:decimal = to_decimal("0.0")
        fact:decimal = 1
        frate:decimal = to_decimal("0.0")
        argt_betrag:decimal = to_decimal("0.0")
        ex_rate:decimal = 1
        qty2:int = 0

        def generate_inner_output():
            return (zipreis)


        if zipreis == 0:

            return generate_inner_output()
        rate =  to_decimal(zipreis)
        qty2 = res_line.zimmeranz

        if res_line.reserve_dec != 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()
        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        vat =  to_decimal(vat) + to_decimal(vat2)


        lodg_betrag =  to_decimal(rate) * to_decimal(frate)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
            argt_betrag, ex_rate = argt_betrag(bill_date)
            lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

        if not rm_serv:
            lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)
        zipreis =  to_decimal(lodg_betrag)

        return generate_inner_output()


    def argt_betrag(bill_date:date):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        betrag = to_decimal("0.0")
        ex_rate = 1
        add_it:bool = False
        marknr:int = 0
        argt_defined:bool = False
        qty:int = 0
        exrate1:decimal = 1
        ex2:decimal = 1
        w1 = None

        def generate_inner_output():
            return (betrag, ex_rate)

        W1 =  create_buffer("W1",Waehrung)

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = res_line.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = res_line.kind1

        elif argt_line.vt_percnt == 2:
            qty = res_line.kind2

        if qty == 0:

            return generate_inner_output()

        if argt_line.fakt_modus == 1:
            add_it = True

        elif argt_line.fakt_modus == 2:

            if res_line.ankunft == bill_date:
                add_it = True

        elif argt_line.fakt_modus == 3:

            if (res_line.ankunft + 1) == bill_date:
                add_it = True

        elif argt_line.fakt_modus == 4 and get_day(bill_date) == 1:
            add_it = True

        elif argt_line.fakt_modus == 5 and get_day(bill_date + 1) == 1:
            add_it = True

        elif argt_line.fakt_modus == 6:

            if (res_line.ankunft + (argt_line.intervall - 1)) >= bill_date:
                add_it = True

        if not add_it:

            return generate_inner_output()
        marknr = res_line.reserve_int

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            argt_defined = True
            betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
            ex_rate = get_exrate1()

            return generate_inner_output()

        if guest_pr and marknr != 0 and not argt_defined:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == marknr) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                ex_rate = get_exrate2(marknr)

                return generate_inner_output()
        betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)
        ex_rate = get_exrate3()

        return generate_inner_output()


    def get_exrate1():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        ex_rate = 1

        def generate_inner_output():
            return (ex_rate)


        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

        elif res_line.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        elif res_line.adrflag or not foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 152)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def get_exrate2(marknr:int):

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        ex_rate = 1

        def generate_inner_output():
            return (ex_rate)


        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

            return generate_inner_output()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 18) & (Queasy.number1 == marknr)).first()

        if not queasy or (queasy and queasy.char3 == ""):

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (func.lower(Queasy.char1) == (contcode).lower())).first()

        if queasy.key == 18:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == queasy.char3)).first()
        else:

            if queasy.number1 != 0:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == queasy.number1)).first()

            elif queasy.logi1 or not foreign_rate:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 152)).first()

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.wabkurz == htparam.fchar)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 144)).first()

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def get_exrate3():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        ex_rate = 1
        local_nr:int = 0
        foreign_nr:int = 0

        def generate_inner_output():
            return (ex_rate)


        if arrangement.betriebsnr != 0:

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == arrangement.betriebsnr)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                return generate_inner_output()

        if foreign_rate:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 144)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 152)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def create_rev():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, j, ci_date, curr_day, tot_room, inactive, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        i:int = 0
        mm:int = 0
        yy:int = 0
        datum:date = None
        datum1:str = ""
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        rev_list_list.clear()
        curr_day = mm - 1
        rev_list = Rev_list()
        rev_list_list.append(rev_list)

        bezeich = "Period"
        for i in range(1,6 + 1) :
            curr_day = curr_day + 1

            if curr_day == 13:
                curr_day = 1
            rev_list.str1[i - 1] = " " + to_string(week_list[curr_day - 1], "x(5)")
        rev_list = Rev_list()
        rev_list_list.append(rev_list)

        bezeich = "Room Revenue"
        for i in range(1,6 + 1) :
            rev_list.str[i - 1] = to_string(rev_array[i - 1], "->,>>>,>>>,>>9")


        rev_list = Rev_list()
        rev_list_list.append(rev_list)

        bezeich = "Period"
        for i in range(1,6 + 1) :
            curr_day = curr_day + 1

            if curr_day == 13:
                curr_day = 1
            rev_list.str1[i - 1] = " " + to_string(week_list[curr_day - 1], "x(5)")
        rev_list = Rev_list()
        rev_list_list.append(rev_list)

        bezeich = "Room Revenue"
        for i in range(1,6 + 1) :
            rev_list.str1[i - 1] = to_string(rev_array[i + 6 - 1], "->,>>>,>>>,>>9")


    def sum_rooms():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list


        tot_room = 0
        inactive = 0

        for zimkateg in db_session.query(Zimkateg).filter(
                 (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():

                if zimmer.sleeping:
                    tot_room = tot_room + 1
                else:
                    inactive = inactive + 1


    def create_label11():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, j, datum, ci_date, curr_day, tot_room, inactive, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list

        datum1:str = ""
        mm:int = 0
        yy:int = 0
        i:int = 0
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        dlist = " "
        for i in range(1,12 + 1) :
            curr_day = mm
            datum = date_mdy(mm, 1, yy)
            datum1 = substring(to_string(datum) , 0, 5)
            dlist = dlist + " " + datum1
            month_str[i - 1] = datum1 + " " + translateExtended (week_list[curr_day - 1], lvcarea, "")
            mm = mm + 1

            if mm == 13:
                mm = 1
                yy = yy + 1


    def clear_shared():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list


        room_list_list.clear()
        segm_list_list.clear()
        rev_list_list.clear()
        sum_list_list.clear()


    def clear_shared1():

        nonlocal tt_month_str_list, room_list_list, rev_list_list, sum_list_list, segm_list_list, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, paramtext, kontline, htparam, zkstat, zinrstat, outorder, genstat, res_line, guest, zimmer, reservation, queasy, guestseg, reslin_queasy, waehrung, arrangement, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_list
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal segm1_list_list, argt_list_list, zikat_list_list, room_list_list, sum_list_list, segm_list_list, rev_list_list, tt_month_str_list


        room_list_list.clear()
        segm_list_list.clear()
        rev_list_list.clear()
        sum_list_list.clear()

        for segm1_list in query(segm1_list_list):
            segm1_list_list.remove(segm1_list)
        zikat_list_list.clear()
        argt_list_list.clear()

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()

    if paramtext:
        htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()

    if paramtext:
        htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()

    if paramtext:
        htl_tel = paramtext.ptexte
    out_type = translateExtended ("Output By : Rooms", lvcarea, "")
    dis_type = translateExtended ("Display : Daily Basis", lvcarea, "")
    rm_occ = translateExtended ("Room Occupied", lvcarea, "")
    pax_occ = translateExtended ("Person Occupied", lvcarea, "")
    avl_rm = translateExtended (" Saleable Rooms", lvcarea, "")
    occ_proz = translateExtended ("Occupancy (%)", lvcarea, "")
    sum_rooms()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 128)).first()
    rm_serv = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if op_type == 0:
        clear_shared()
        create_label11()
        create_browse11()

        if show_rmrev:
            create_rev()
    for i in range(1,12 + 1) :
        tt_month_str = Tt_month_str()
        tt_month_str_list.append(tt_month_str)

        tt_month_str.i_counter = i
        tt_month_str.month_str = month_str[i - 1]

    return generate_output()