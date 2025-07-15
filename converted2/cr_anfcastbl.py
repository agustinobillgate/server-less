#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
import re
from functions.ratecode_rate import ratecode_rate
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Paramtext, Kontline, Htparam, Zkstat, Zinrstat, Zimmer, Outorder, Genstat, Res_line, Guest, Reservation, Arrangement, Bill_line, Queasy, Guestseg, Reslin_queasy, Waehrung, Guest_pr, Katpreis, Artikel, Argt_line, Zimkateg

segm1_list_data, Segm1_list = create_model("Segm1_list", {"selected":bool, "segm":int, "bezeich":string, "bezeich1":string})
argt_list_data, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":string, "bezeich":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def cr_anfcastbl(pvilanguage:int, vhp_limited:bool, dlist:string, op_type:int, printer_nr:int, call_from:int, txt_file:string, monthdayselect:int, roompaxselect:int, nationselect:string, all_segm:bool, all_argt:bool, all_zikat:bool, from_month:string, show_rmrev:bool, incl_tent:bool, incl_wait:bool, incl_glob:bool, segm1_list_data:[Segm1_list], argt_list_data:[Argt_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Paramtext, Kontline, Htparam, Zkstat, Zinrstat, Genstat, Res_line, Guest, Reservation, Arrangement, Queasy, Guestseg, Reslin_queasy, Waehrung, Guest_pr, Katpreis, Artikel, Argt_line, Zimkateg])

    tt_month_str_data = []
    room_list_data = []
    rev_list_data = []
    sum_list_data = []
    segm_list_data = []
    lvcarea:string = "annual-fcast"
    rmsharer:bool = False
    week_list:List[string] = [" Jan ", " Feb ", " Mar ", " Apr ", " May ", " Jun ", " Jul ", " Aug ", " Sep ", " Oct ", " Nov ", " Dec "]
    wlist:string = ""
    month_str:List[string] = create_empty_list(12,"")
    rm_serv:bool = False
    foreign_rate:bool = False
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    out_type:string = ""
    dis_type:string = ""
    rm_occ:string = ""
    pax_occ:string = ""
    avl_rm:string = ""
    occ_proz:string = ""
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
    rev_array:List[Decimal] = create_empty_list(12,to_decimal("0"))
    curr_date:date = None
    date1:date = None
    contcode:string = ""
    ct:string = ""
    room_ooo:List[Decimal] = create_empty_list(12,to_decimal("0"))
    tmp_room:List[int] = create_empty_list(12,0)
    paramtext = kontline = htparam = zkstat = zinrstat = zimmer = outorder = genstat = res_line = guest = reservation = arrangement = bill_line = queasy = guestseg = reslin_queasy = waehrung = guest_pr = katpreis = artikel = argt_line = zimkateg = None

    segm1_list = argt_list = zikat_list = room_list = sum_list = segm_list = rev_list = tt_month_str = kbuff = r1_list = r2_list = r3_list = r4_list = r5_list = r6_list = r7_list = r8_list = None

    room_list_data, Room_list = create_model("Room_list", {"nr":int, "tag":int, "bezeich":string, "room":[int,12], "pax":[int,12], "coom":[string,12], "rstat":int})
    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "summe":[int,12]})
    segm_list_data, Segm_list = create_model("Segm_list", {"segmentcode":int, "bezeich":string, "bezeich1":string, "segm":[int,12]})
    rev_list_data, Rev_list = create_model("Rev_list", {"bezeich":string, "str1":[string,6]})
    tt_month_str_data, Tt_month_str = create_model("Tt_month_str", {"i_counter":int, "month_str":string})

    Kbuff = create_buffer("Kbuff",Kontline)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        return {"tt-month-str": tt_month_str_data, "room-list": room_list_data, "rev-list": rev_list_data, "sum-list": sum_list_data, "segm-list": segm_list_data, "segm1-list": segm1_list_data, "argt-list": argt_list_data, "zikat-list": zikat_list_data}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def assign_it(j:int, datum:date, from_date:date):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")

        if datum == res_line.abreise:
            pass
        else:

            if res_line.zipreis > 0:
                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, j, from_date))
            rev_array[j - 1] = rev_array[j - 1] + net_lodg


    def create_browse11():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

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
        lodging:Decimal = to_decimal("0.0")
        loop_date:date = None
        datum3:date = None
        ooo_room:int = 0
        d2:date = None
        tmp_yy:int = 0
        R1_list = Room_list
        r1_list_data = room_list_data
        R2_list = Room_list
        r2_list_data = room_list_data
        R3_list = Room_list
        r3_list_data = room_list_data
        R4_list = Room_list
        r4_list_data = room_list_data
        R5_list = Room_list
        r5_list_data = room_list_data
        R6_list = Room_list
        r6_list_data = room_list_data
        R7_list = Room_list
        r7_list_data = room_list_data
        R8_list = Room_list
        r8_list_data = room_list_data
        room_list_data.clear()
        for i in range(1,12 + 1) :
            rev_array[i - 1] = 0
        for i in range(1,31 + 1) :
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.tag = i
            room_list.bezeich = " " + to_string(i, ">9 ")

            if incl_tent or incl_wait:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.tag = i
                room_list.rstat = 1
        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 32
        room_list.bezeich = "==============="


        for i in range(1,12 + 1) :
            room_list.coom[i - 1] = "======="
        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 33
        room_list.bezeich = translateExtended (" Room Occupied", lvcarea, "")


        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 34
        room_list.bezeich = translateExtended (" Saleable Rooms", lvcarea, "")


        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 35
        room_list.bezeich = " Occupancy (%)"


        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 36
        room_list.bezeich = translateExtended ("Person Occupied", lvcarea, "")

        if incl_tent:
            room_list = Room_list()
            room_list_data.append(room_list)

            room_list.tag = 37
            room_list.bezeich = translateExtended ("Tentative-Occ %", lvcarea, "")

            r5_list = query(r5_list_data, filters=(lambda r5_list: r5_list.tag == 37), first=True)

        r1_list = query(r1_list_data, filters=(lambda r1_list: r1_list.tag == 33), first=True)

        r2_list = query(r2_list_data, filters=(lambda r2_list: r2_list.tag == 34), first=True)

        r3_list = query(r3_list_data, filters=(lambda r3_list: r3_list.tag == 35), first=True)

        r4_list = query(r4_list_data, filters=(lambda r4_list: r4_list.tag == 36), first=True)
        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 38
        room_list.bezeich = translateExtended ("SaleRoom w/ OOO", lvcarea, "")


        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.tag = 39
        room_list.bezeich = translateExtended ("Occ(%) w/ OOO", lvcarea, "")

        r6_list = query(r6_list_data, filters=(lambda r6_list: r6_list.tag == 38), first=True)

        r7_list = query(r7_list_data, filters=(lambda r7_list: r7_list.tag == 39), first=True)

        r8_list = query(r8_list_data, filters=(lambda r8_list: r8_list.tag == 39), first=True)
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
        tmp_yy = yy + 1
        curr_date = date_mdy(mm, 1, yy)
        to_date = date_mdy(mm, 1, tmp_yy) - timedelta(days=1)

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

                r2_list = query(r2_list_data, filters=(lambda r2_list: r2_list.tag == 34), first=True)

                if r2_list:
                    r2_list.room[j - 1] = r2_list.room[j - 1] + zkstat.anz100
        for i in range(1,12 + 1) :

            if tmp_i[i - 1] == 0:
                r2_list.room[i - 1] = tot_room * tmp_list[i - 1]

            if tmp_i[i - 1] == 2:
                r2_list.room[i - 1] = r2_list.room[i - 1] + (tot_room * (tmp_list[i - 1] - get_day(datum2)))

        if curr_date < ci_date:

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= curr_date) & (Zinrstat.datum <= datum2) & (Zinrstat.zinr == ("ooo").lower())).order_by(Zinrstat._recid).all():
                datum = zinrstat.datum
                j = get_month(datum) - mm + 1

                if j <= 0:
                    j = j + 12
                tmp_i[j - 1] = 1

                if get_month(zinrstat.datum) == get_month(datum3):
                    tmp_i[j - 1] = 2

                r6_list = query(r6_list_data, filters=(lambda r6_list: r6_list.tag == 38), first=True)

                if r6_list:
                    r6_list.room[j - 1] = (r6_list.room[j - 1] + zinrstat.zimmeranz)
            for loop_date in date_range(from_date,to_date) :
                ooo_room = 0

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= loop_date) & (Outorder.gespende >= loop_date) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    ooo_room = ooo_room + 1
                j = get_month(loop_date) - mm + 1

                if j <= 0:
                    j = j + 12
                tmp_i[j - 1] = 1

                r6_list = query(r6_list_data, filters=(lambda r6_list: r6_list.tag == 38), first=True)

                if r6_list:
                    r6_list.room[j - 1] = (r6_list.room[j - 1] + ooo_room)
        else:
            for loop_date in date_range(from_date,to_date) :
                ooo_room = 0

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= loop_date) & (Outorder.gespende >= loop_date) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True


                    ooo_room = ooo_room + 1
                j = get_month(loop_date) - mm + 1

                if j <= 0:
                    j = j + 12
                tmp_i[j - 1] = 1

                r6_list = query(r6_list_data, filters=(lambda r6_list: r6_list.tag == 38), first=True)

                if r6_list:
                    r6_list.room[j - 1] = (r6_list.room[j - 1] + ooo_room)

        if curr_date < ci_date:

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= curr_date) & (Genstat.datum <= datum2) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():
                do_it = True
                rmsharer = (genstat.resstatus == 13)

                if vhp_limited:
                    do_it = True

                if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8 and genstat.logis == 0:
                    do_it = False

                if do_it and not all_segm:

                    segm1_list = query(segm1_list_data, filters=(lambda segm1_list: segm1_list.segm == genstat.segmentcode and segm1_list.selected), first=True)
                    do_it = None != segm1_list

                if do_it and not all_argt:

                    argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                    do_it = None != argt_list

                if do_it and not all_zikat:

                    zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                    do_it = None != zikat_list

                if do_it:
                    datum = genstat.datum
                    j = get_month(datum) - mm + 1

                    if j <= 0:
                        j = j + 12

                    room_list = query(room_list_data, filters=(lambda room_list: room_list.tag == get_day(datum)), first=True)

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
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= to_date) & (Res_line.abreise >= from_date))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if nationselect != "":

                    if not guest or nationselect != guest.nation1:
                        continue

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if last_resnr != res_line.resnr:

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                    last_resnr = res_line.resnr
                do_it = True

                if not incl_tent and res_line.resstatus == 3:
                    do_it = False

                if not incl_wait and res_line.resstatus == 4:
                    do_it = False

                if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                    bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                    do_it = None != bill_line

                if do_it and zimmer:

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False

                if do_it and not all_segm:

                    segm1_list = query(segm1_list_data, filters=(lambda segm1_list: segm1_list.segm == reservation.segmentcode and segm1_list.selected), first=True)
                    do_it = None != segm1_list

                if do_it and not all_argt:

                    argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == res_line.arrangement and argt_list.selected), first=True)
                    do_it = None != argt_list

                if do_it and not all_zikat:

                    zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                    do_it = None != zikat_list

                if do_it and (res_line.kontignr < 0):

                    if all_segm:
                        do_it = True
                    else:

                        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

                        if not guestseg:

                            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

                        if guestseg:

                            segm1_list = query(segm1_list_data, filters=(lambda segm1_list: segm1_list.segm == guestseg.segmentcode and segm1_list.selected), first=True)
                            do_it = not None != segm1_list

                if do_it:

                    if res_line.ankunft Gt from_date:
                        datum1 = res_line.ankunft
                    else:
                        datum1 = from_date

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise


                    else:

                        if res_line.abreise < to_date:
                            datum2 = res_line.abreise - timedelta(days=1)
                        else:
                            datum2 = to_date
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3
                        j = get_month(datum) - mm + 1

                        if j <= 0:
                            j = j + 12

                        if res_line.resstatus != 3 and res_line.resstatus != 4:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.tag == get_day(datum) and room_list.rstat == 0), first=True)
                        else:

                            room_list = query(room_list_data, filters=(lambda room_list: room_list.tag == get_day(datum) and room_list.rstat == 1), first=True)

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

                room_list = query(room_list_data, filters=(lambda room_list: room_list.tag == get_day(datum)), first=True)

                for kontline in db_session.query(Kontline).filter(
                         (Kontline.betriebsnr == 1) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():

                    guest = get_cache (Guest, {"gastnr": [(eq, kontline.gastnr)]})

                    if nationselect != "":

                        if not guest or nationselect != guest.nation1:
                            continue
                    do_it = True

                    if do_it and not all_argt:

                        argt_list = query(argt_list_data, filters=(lambda argt_list: argt_list.argt == kontline.arrangement and argt_list.selected), first=True)
                        do_it = None != argt_list

                    if do_it and not all_zikat:

                        zikat_list = query(zikat_list_data, filters=(lambda zikat_list: zikat_list.zikatnr == kontline.zikatnr and zikat_list.selected), first=True)
                        do_it = None != zikat_list

                    if do_it and not all_segm:

                        guest = get_cache (Guest, {"gastnr": [(eq, kontline.gastnr)]})

                        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

                        if not guestseg:

                            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})

                        if guestseg:

                            segm1_list = query(segm1_list_data, filters=(lambda segm1_list: segm1_list.segm == guestseg.segmentcode and segm1_list.selected), first=True)
                            do_it = None != segm1_list

                    if do_it:

                        if roompaxselect == 0:
                            room_list.room[j - 1] = room_list.room[j - 1] + kontline.zimmeranz

                        elif roompaxselect != 0:
                            room_list.room[j - 1] = room_list.room[j - 1] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz
                            room_list.pax[j - 1] = room_list.pax[j - 1] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft <= datum) & (Res_line.abreise > datum) & (Res_line.kontignr < 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                    room_list.room[j - 1] = room_list.room[j - 1] - res_line.zimmeranz

                    kbuff = get_cache (Kontline, {"gastnr": [(eq, res_line.gastnr)],"ankunft": [(eq, datum)],"zikatnr": [(eq, res_line.zikatnr)],"betriebsnr": [(eq, 1)]})

                    if kbuff:
                        room_list.pax[j - 1] = room_list.pax[j - 1] - (kbuff.erwachs + kbuff.kind1) * res_line.zimmeranz
                    else:
                        room_list.pax[j - 1] = room_list.pax[j - 1] - res_line.erwachs * res_line.zimmeranz

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.tag <= 31)):
            for i in range(1,12 + 1) :

                if room_list.room[i - 1] != 0 or room_list.tag <= 28:
                    room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>,>>9")

                if roompaxselect == 0:
                    r1_list.room[i - 1] = r1_list.room[i - 1] + room_list.room[i - 1]
                r4_list.room[i - 1] = r4_list.room[i - 1] + room_list.pax[i - 1]

                if incl_tent and room_list.rstat == 1:
                    r5_list.room[i - 1] = r5_list.room[i - 1] + room_list.room[i - 1]

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.tag >= 29 and room_list.tag <= 31)):
            for i in range(1,12 + 1) :

                if room_list.room[i - 1] == 0 and room_list.tag <= tmp_list[i - 1]:
                    room_list.coom[i - 1] = " 0"
        for i in range(1,12 + 1) :

            if roompaxselect == 0:
                r1_list.coom[i - 1] = to_string(r1_list.room[i - 1], "->>,>>9")

                if r2_list.room[i - 1] != 0 and r2_list.room[i - 1] != None:
                    r2_list.room[i - 1] = r2_list.room[i - 1]
                    r2_list.coom[i - 1] = to_string(r2_list.room[i - 1], "->>,>>9")

                    if r2_list.room[i - 1] != 0 and r2_list.room[i - 1] != None:
                        r3_list.coom[i - 1] = to_string(r1_list.room[i - 1] / r2_list.room[i - 1] * 100, "->>9.99")

                    if incl_tent:

                        if r2_list.room[i - 1] != 0 and r2_list.room[i - 1] != None:
                            r5_list.coom[i - 1] = to_string(r5_list.room[i - 1] / r2_list.room[i - 1] * 100, "->>9.99")

                    if r6_list.room[i - 1] != 0 and r6_list.room[i - 1] != None:

                        if (r2_list.room[i - 1] - r6_list.room[i - 1]) != 0 and (r2_list.room[i - 1] - r6_list.room[i - 1]) != None:
                            r6_list.coom[i - 1] = to_string(r2_list.room[i - 1] - r6_list.room[i - 1], "->>,>>9")
                            room_ooo[i - 1] = r1_list.room[i - 1] / (r2_list.room[i - 1] - r6_list.room[i - 1]) * 100
                            r7_list.coom[i - 1] = to_string(room_ooo[i - 1], "->>9.99")
                        else:
                            r6_list.coom[i - 1] = to_string(r2_list.room[i - 1] - r6_list.room[i - 1], "->>,>>9")
                            room_ooo[i - 1] = 0
                            r7_list.coom[i - 1] = to_string(room_ooo[i - 1], "->>9.99")
            r4_list.coom[i - 1] = to_string(r4_list.room[i - 1], "->>,>>9")


    def calculate_zipreis(bill_date:date, roomrate:Decimal):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        rm_rate:Decimal = to_decimal("0.0")
        add_it:bool = False
        qty:int = 0
        qty2:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
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
        publish_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate)

        W1 =  create_buffer("W1",Waehrung)
        qty2 = res_line.zimmeranz

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)
            roomrate = cal_lodging(bill_date, roomrate)

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        if guest_pr:
            contcode = guest_pr.code
            ct = res_line.zimmer_wunsch

            if matches(ct,r"*$CODE$*"):
                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                contcode = substring(ct, 0, get_index(ct, ";") - 1)
            post_date = bill_date

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

            if queasy and queasy.logi3:
                post_date = res_line.ankunft
            ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
            kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

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

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, 0)]})

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(bill_date) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)
                roomrate = cal_lodging(bill_date, roomrate)
            roomrate = cal_lodging(bill_date, roomrate)

        return generate_inner_output()


    def cal_lodging(bill_date:date, zipreis:Decimal):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        rate:Decimal = to_decimal("0.0")
        lodg_betrag:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = 1
        frate:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        ex_rate:Decimal = 1
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

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
        service, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, bill_date))
        vat =  to_decimal(vat) + to_decimal(vat2)


        lodg_betrag =  to_decimal(rate) * to_decimal(frate)

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
            argt_betrag, ex_rate = argt_betrag(bill_date)
            lodg_betrag =  to_decimal(lodg_betrag) - to_decimal(argt_betrag) * to_decimal(ex_rate)

        if not rm_serv:
            lodg_betrag =  to_decimal(lodg_betrag) / to_decimal(fact)
        zipreis =  to_decimal(lodg_betrag)

        return generate_inner_output()


    def argt_betrag(bill_date:date):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        betrag = to_decimal("0.0")
        ex_rate = 1
        add_it:bool = False
        marknr:int = 0
        argt_defined:bool = False
        qty:int = 0
        exrate1:Decimal = 1
        ex2:Decimal = 1
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

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:
            argt_defined = True
            betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
            ex_rate = get_exrate1()

            return generate_inner_output()

        if guest_pr and marknr != 0 and not argt_defined:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, marknr)],"number2": [(eq, argt_line.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

            if reslin_queasy:
                betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                ex_rate = get_exrate2(marknr)

                return generate_inner_output()
        betrag =  to_decimal(argt_line.betrag) * to_decimal(qty)
        ex_rate = get_exrate3()

        return generate_inner_output()


    def get_exrate1():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        ex_rate = 1

        def generate_inner_output():
            return (ex_rate)


        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

        elif res_line.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        elif res_line.adrflag or not foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def get_exrate2(marknr:int):

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        ex_rate = 1

        def generate_inner_output():
            return (ex_rate)


        if reservation.insurance and res_line.reserve_dec != 0:
            ex_rate =  to_decimal(res_line.reserve_dec)

            return generate_inner_output()

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

        if not queasy or (queasy and queasy.char3 == ""):

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

        if queasy.key == 18:

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
        else:

            if queasy.number1 != 0:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

            elif queasy.logi1 or not foreign_rate:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def get_exrate3():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        ex_rate = 1
        local_nr:int = 0
        foreign_nr:int = 0

        def generate_inner_output():
            return (ex_rate)


        if arrangement.betriebsnr != 0:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                return generate_inner_output()

        if foreign_rate:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                ex_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        return generate_inner_output()


    def create_rev():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, j, ci_date, curr_day, tot_room, inactive, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        i:int = 0
        mm:int = 0
        yy:int = 0
        datum:date = None
        datum1:string = ""
        mm = to_int(substring(from_month, 0, 2))
        yy = to_int(substring(from_month, 2, 4))
        rev_list_data.clear()
        curr_day = mm - 1
        rev_list = Rev_list()
        rev_list_data.append(rev_list)

        bezeich = "Period"
        for i in range(1,6 + 1) :
            curr_day = curr_day + 1

            if curr_day == 13:
                curr_day = 1
            rev_list.str1[i - 1] = " " + to_string(week_list[curr_day - 1], "x(5)")
        rev_list = Rev_list()
        rev_list_data.append(rev_list)

        bezeich = "Room Revenue"
        for i in range(1,6 + 1) :
            rev_list.str1[i - 1] = to_string(rev_array[i - 1], "->,>>>,>>>,>>9")


        rev_list = Rev_list()
        rev_list_data.append(rev_list)

        bezeich = "Period"
        for i in range(1,6 + 1) :
            curr_day = curr_day + 1

            if curr_day == 13:
                curr_day = 1
            rev_list.str1[i - 1] = " " + to_string(week_list[curr_day - 1], "x(5)")
        rev_list = Rev_list()
        rev_list_data.append(rev_list)

        bezeich = "Room Revenue"
        for i in range(1,6 + 1) :
            rev_list.str1[i - 1] = to_string(rev_array[i + 6 - 1], "->,>>>,>>>,>>9")


    def sum_rooms():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data


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

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, j, datum, ci_date, curr_day, tot_room, inactive, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data

        datum1:string = ""
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

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data


        room_list_data.clear()
        segm_list_data.clear()
        rev_list_data.clear()
        sum_list_data.clear()


    def clear_shared1():

        nonlocal tt_month_str_data, room_list_data, rev_list_data, sum_list_data, segm_list_data, lvcarea, rmsharer, week_list, wlist, month_str, rm_serv, foreign_rate, htl_name, htl_adr, htl_tel, out_type, dis_type, rm_occ, pax_occ, avl_rm, occ_proz, i, j, datum, ci_date, curr_day, tot_room, inactive, mm, yy, diff_one, ok, pax, rev_array, curr_date, date1, contcode, ct, room_ooo, tmp_room, paramtext, kontline, htparam, zkstat, zinrstat, zimmer, outorder, genstat, res_line, guest, reservation, arrangement, bill_line, queasy, guestseg, reslin_queasy, waehrung, guest_pr, katpreis, artikel, argt_line, zimkateg
        nonlocal pvilanguage, vhp_limited, dlist, op_type, printer_nr, call_from, txt_file, monthdayselect, roompaxselect, nationselect, all_segm, all_argt, all_zikat, from_month, show_rmrev, incl_tent, incl_wait, incl_glob, segm1_list_data
        nonlocal kbuff


        nonlocal segm1_list, argt_list, zikat_list, room_list, sum_list, segm_list, rev_list, tt_month_str, kbuff, r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list, r8_list
        nonlocal room_list_data, sum_list_data, segm_list_data, rev_list_data, tt_month_str_data


        room_list_data.clear()
        segm_list_data.clear()
        rev_list_data.clear()
        sum_list_data.clear()

        for segm1_list in query(segm1_list_data):
            segm1_list_data.remove(segm1_list)
        zikat_list_data.clear()
        argt_list_data.clear()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})

    if paramtext:
        htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})

    if paramtext:
        htl_tel = paramtext.ptexte
    out_type = translateExtended ("Output By : Rooms", lvcarea, "")
    dis_type = translateExtended ("Display : Daily Basis", lvcarea, "")
    rm_occ = translateExtended ("Room Occupied", lvcarea, "")
    pax_occ = translateExtended ("Person Occupied", lvcarea, "")
    avl_rm = translateExtended (" Saleable Rooms", lvcarea, "")
    occ_proz = translateExtended ("Occupancy (%)", lvcarea, "")
    sum_rooms()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if op_type == 0:
        clear_shared()
        create_label11()
        create_browse11()

        if show_rmrev:
            create_rev()
    for i in range(1,12 + 1) :
        tt_month_str = Tt_month_str()
        tt_month_str_data.append(tt_month_str)

        tt_month_str.i_counter = i
        tt_month_str.month_str = month_str[i - 1]

    return generate_output()