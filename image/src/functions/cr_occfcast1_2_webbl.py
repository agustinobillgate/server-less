from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from sqlalchemy import func
from functions.get_room_breakdown import get_room_breakdown
from models import Res_line, Htparam, Waehrung, Kontline, Zimmer, Guest, Zimkateg, Segment, Genstat, Exrate, Fixleist, Artikel, Reservation, Arrangement, Bill_line, Queasy, Reslin_queasy, Guestseg, Zinrstat, Outorder, Zkstat, Umsatz

segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})
outlook_list_list, Outlook_list = create_model("Outlook_list", {"selected":bool, "outlook_nr":int, "bezeich":str})

def cr_occfcast1_2_webbl(segm_list_list:[Segm_list], argt_list_list:[Argt_list], zikat_list_list:[Zikat_list], outlook_list_list:[Outlook_list], pvilanguage:int, op_type:int, flag_i:int, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, exclooo:bool, incl_tent:bool, show_rev:int, vhp_limited:bool, excl_compl:bool, all_outlook:bool, incl_oth:bool):
    room_list_list = []
    lvcarea:str = "occ-fcast1"
    tot_rmrev:decimal = to_decimal("0.0")
    bonus_array:List[bool] = create_empty_list(999, False)
    week_list:List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    tent_pers:int = 0
    datum:date = None
    tot_room:int = 0
    mtd_tot_room:int = 0
    accum_tot_room:int = 0
    actual_tot_room:int = 0
    segm_name:str = ""
    argm_name:str = ""
    room_name:str = ""
    ci_date:date = None
    pax:int = 0
    t_lodg:List[decimal] = create_empty_list(7,to_decimal("0"))
    jml_date:int = 0
    tot_avrg:decimal = to_decimal("0.0")
    t_rmrate:decimal = to_decimal("0.0")
    t_rmrate2:decimal = to_decimal("0.0")
    t_revpar:decimal = to_decimal("0.0")
    t_revpar2:decimal = to_decimal("0.0")
    price_decimal:int = 0
    new_contrate:bool = False
    rm_vat:bool = False
    rm_serv:bool = False
    rm_array:List[int] = create_empty_list(18,0)
    exchg_rate:decimal = to_decimal("0.0")
    sum_comp:decimal = to_decimal("0.0")
    post_it:bool = False
    fcost:decimal = to_decimal("0.0")
    curr_time:int = 0
    res_line = htparam = waehrung = kontline = zimmer = guest = zimkateg = segment = genstat = exrate = fixleist = artikel = reservation = arrangement = bill_line = queasy = reslin_queasy = guestseg = zinrstat = outorder = zkstat = umsatz = None

    room_list = segm_list = argt_list = zikat_list = outlook_list = print_list = print_list2 = print_list3 = rline1 = active_rm_list = dayuse_list = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":str, "room":[decimal,17], "coom":[str,17], "k_pax":int, "t_pax":int, "lodg":[decimal,7], "avrglodg":decimal, "avrglodg2":decimal, "avrgrmrev":decimal, "avrgrmrev2":decimal, "others":[decimal,8], "ly_fcast":str, "ly_actual":str, "ly_avlodge":str, "room_exccomp":int, "room_comp":int, "fixleist":decimal, "fixleist2":decimal, "rmrate":decimal, "rmrate2":decimal, "revpar":decimal, "revpar2":decimal, "avrglodg_inclcomp":decimal, "avrglodg_exclcomp":decimal, "rmocc_exclcomp":decimal})
    print_list_list, Print_list = create_model("Print_list", {"code_name":str})
    print_list2_list, Print_list2 = create_model("Print_list2", {"argm":str})
    print_list3_list, Print_list3 = create_model("Print_list3", {"room":str})
    active_rm_list_list, Active_rm_list = create_model("Active_rm_list", {"datum":date, "zimmeranz":int})
    dayuse_list_list, Dayuse_list = create_model("Dayuse_list", {"datum":date, "zimmeranz":int, "pax":int})

    Rline1 = create_buffer("Rline1",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list
        return {"room-list": room_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        rate:decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def create_browse():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        curr_i:int = 0
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        dayuse_flag:bool = False
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:decimal = to_decimal("0.0")
        rmsharer:bool = False
        othrev:decimal = to_decimal("0.0")
        tavg_rmrev:decimal = to_decimal("0.0")
        tavg_rmrev2:decimal = to_decimal("0.0")
        troom_exccomp:int = 0
        rsvstat:str = ""
        avrg_lodging:decimal = to_decimal("0.0")
        avrg_rmrate:decimal = to_decimal("0.0")
        avrg_lodging2:decimal = to_decimal("0.0")
        avrg_rmrate2:decimal = to_decimal("0.0")
        anzahl_dayuse:int = 0
        kline = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_fixcost:decimal = to_decimal("0.0")
        tot_fixcost2:decimal = to_decimal("0.0")
        sum_breakfast:decimal = to_decimal("0.0")
        sum_lunch:decimal = to_decimal("0.0")
        sum_dinner:decimal = to_decimal("0.0")
        sum_other:decimal = to_decimal("0.0")
        sum_breakfast_usd:decimal = to_decimal("0.0")
        sum_lunch_usd:decimal = to_decimal("0.0")
        sum_dinner_usd:decimal = to_decimal("0.0")
        sum_other_usd:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        rmrate:decimal = to_decimal("0.0")
        room_exccomp:int = 0
        bfast_art:int = 0
        curr_zinr:str = ""
        pax:int = 0
        curr_date1:date = None
        t_avrglodg_inclcomp:decimal = to_decimal("0.0")
        t_avrglodg_exclcomp:decimal = to_decimal("0.0")
        t_rmocc_exclcomp:decimal = to_decimal("0.0")
        t_room_comp:int = 0
        tmax:int = 0
        tmin:int = 0
        counter:int = 0
        S_list = Segm_list
        s_list_list = segm_list_list
        A_list = Argt_list
        a_list_list = argt_list_list
        Z_list = Zikat_list
        z_list_list = zikat_list_list
        Kline =  create_buffer("Kline",Kontline)
        O_list = Outlook_list
        o_list_list = outlook_list_list

        if not htparam or not(htparam.paramnr == 125):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 125)).first()
        bfast_art = htparam.finteger
        room_exccomp = 0
        for i in range(1,18 + 1) :
            rm_array[i - 1] = 0
        for i in range(1,4 + 1) :
            t_lodg[i - 1] = 0
        tent_pers = 0
        room_list_list.clear()
        actual_tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                actual_tot_room = actual_tot_room + 1
            else:

                if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                    z_list = db_session.query(Z_list).filter(
                        (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()

                if z_list:
                    actual_tot_room = actual_tot_room + 1
        create_active_room_list()
        datum = curr_date - timedelta(days=1)
        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)
            wd = get_weekday(datum) - 1

            if wd == 0:
                wd = 7
            rsvstat = rsv_closeout(datum)
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.wd = wd
            room_list.datum = datum
            room_list.bezeich = " " + week_list[wd - 1] + " " + to_string(datum) + rsvstat

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                allot_doit = True

                if kontline.zikatnr != 0 and not all_zikat:

                    if not z_list or not(z_list.zikatnr == kontline.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == kontline.zikatnr) &  (Z_list.selected)).first()
                    allot_doit = None != z_list

                if allot_doit and (datum >= (ci_date + timedelta(days=kontline.ruecktage))):
                    room_list.room[13] = room_list.room[13] + kontline.zimmeranz
                    rm_array[13] = rm_array[13] + kontline.zimmeranz
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.bezeich = " TOTAL"
        datum1 = curr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        genstat_obj_list = []
        for genstat, guest, zimkateg, waehrung, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                (Genstat.res_date[inc_value(1)] >= datum1) &  (Genstat.res_date[inc_value(1)] <= d2) &  (Genstat.resstatus != 13) &  (Genstat.segmentcode != 0) &  (Genstat.res_logic[inc_value(1)]) &  (Genstat.zinr != " ")).order_by(Genstat.res_date[inc_value(1)], Genstat.zinr, Genstat.datum).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            if curr_zinr != genstat.zinr:
                do_it = True

                if do_it and not all_segm:

                    if not s_list or not(s_list.segm == genstat.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == genstat.segmentcode) &  (S_list.selected)).first()
                    do_it = None != s_list

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == genstat.argt and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == genstat.argt) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == genstat.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == genstat.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if do_it:
                    pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    if not room_list or not(room_list.datum == genstat.res_date[1]):
                        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == genstat.res_date[1]), first=True)
                    room_list.room[4] = room_list.room[4] + 1
                    room_list.room[5] = room_list.room[5] + pax
                    rm_array[4] = rm_array[4] + 1
                    rm_array[5] = rm_array[5] + pax


            curr_zinr = genstat.zinr

        for genstat in db_session.query(Genstat).filter(
                (Genstat.datum >= datum1) &  (Genstat.datum <= d2) &  (Genstat.res_logic[inc_value(1)]) &  (Genstat.zinr != "")).order_by(Genstat._recid).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                if not segment or not(segment.segmentcode == genstat.segmentcode):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it and not all_segm:

                if not s_list or not(s_list.segm == genstat.segmentcode and s_list.selected):
                    s_list = db_session.query(S_list).filter(
                        (S_list.segm == genstat.segmentcode) &  (S_list.selected)).first()
                do_it = None != s_list

            if do_it and not all_argt:

                if not a_list or not(a_list.argt == genstat.argt and a_list.selected):
                    a_list = db_session.query(A_list).filter(
                        (A_list.argt == genstat.argt) &  (A_list.selected)).first()
                do_it = None != a_list

            if do_it and not all_zikat:

                if not z_list or not(z_list.zikatnr == genstat.zikatnr and z_list.selected):
                    z_list = db_session.query(Z_list).filter(
                        (Z_list.zikatnr == genstat.zikatnr) &  (Z_list.selected)).first()
                do_it = None != z_list

            if excl_compl and do_it:

                if not segment or not(segment.segmentcode == genstat.segmentcode and (segment.betriebsnr == 1 or segment.betriebsnr == 2)):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == genstat.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                if segment:
                    do_it = False


                else:

                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1]:
                        do_it = False

            if do_it and not all_outlook:

                if not zimmer or not(zimmer.zinr == genstat.zinr):
                    zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == genstat.zinr)).first()

                if zimmer:

                    if not o_list or not(o_list.SELECTED  and o_list.outlook_nr == zimmer.typ):
                        o_list = db_session.query(O_list).filter(
                            (O_list.SELECTED) &  (O_list.outlook_nr == zimmer.typ)).first()
                    do_it = None != o_list

            if not htparam or not(htparam.paramnr == 144):
                htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 144)).first()

            if not waehrung or not(waehrung.wabkurz == htparam.fchar):
                waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:

                if not exrate or not(exrate.datum == genstat.datum and exrate.artnr == waehrung.waehrungsnr):
                    exrate = db_session.query(Exrate).filter(
                        (Exrate.datum == genstat.datum) &  (Exrate.artnr == waehrung.waehrungsnr)).first()

                if exrate:
                    exchg_rate =  to_decimal(exrate.betrag)

            if do_it:

                if not room_list or not(room_list.datum == genstat.datum):
                    room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == genstat.datum), first=True)

                if genstat.res_date[0] == genstat.datum and genstat.resstatus != 13:
                    room_list.room[2] = room_list.room[2] + 1
                    room_list.room[3] = room_list.room[3] + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis
                    rm_array[2] = rm_array[2] + 1
                    rm_array[3] = rm_array[3] + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.gratis

                if not rmsharer:
                    room_list.room[6] = room_list.room[6] + 1
                    rm_array[6] = rm_array[6] + 1

                    if genstat.gratis == 0:
                        room_list.room_exccomp = room_list.room_exccomp + 1
                        room_exccomp = room_exccomp + 1

                    if genstat.gratis != 0:
                        room_list.room_comp = room_list.room_comp + 1
                        t_room_comp = t_room_comp + 1

                if show_rev == 1:
                    room_list.lodg[3] = room_list.lodg[3] + genstat.logis
                    t_lodg[3] = t_lodg[3] + genstat.logis
                    room_list.lodg[4] = room_list.lodg[4] + genstat.logis
                    t_lodg[4] = t_lodg[4] + genstat.logis
                    room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(genstat.zipreis)

                elif show_rev == 2:
                    room_list.lodg[3] = room_list.lodg[3] + genstat.logis
                    t_lodg[3] = t_lodg[3] + genstat.logis
                    room_list.lodg[4] = room_list.lodg[4] + genstat.logis
                    t_lodg[4] = t_lodg[4] + genstat.logis
                    room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                    t_lodg[5] = t_lodg[5] + (genstat.logis / exchg_rate)
                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                    t_lodg[6] = t_lodg[6] + (genstat.logis / exchg_rate)
                    room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(genstat.zipreis)
                    room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)


                else:
                    room_list.lodg[3] = 0
                    t_lodg[3] = 0
                    room_list.lodg[4] = 0
                    t_lodg[4] = 0
                    room_list.lodg[5] = 0
                    t_lodg[5] = 0
                    room_list.lodg[6] = 0
                    t_lodg[6] = 0
                    room_list.rmrate =  to_decimal("0")
                    room_list.rmrate2 =  to_decimal("0")


                room_list.room[7] = room_list.room[7] + genstat.erwachs + genstat.kind1 +\
                        genstat.kind2 + genstat.gratis + genstat.kind3
                rm_array[7] = rm_array[7] + genstat.erwachs + genstat.kind1 +\
                        genstat.kind2 + genstat.gratis + genstat.kind3


                room_list.other[0] = room_list.other[0] + genstat.res_deci[1]
                room_list.other[1] = room_list.other[1] + genstat.res_deci[2]
                room_list.other[2] = room_list.other[2] + genstat.res_deci[3]
                room_list.other[3] = room_list.other[3] + genstat.res_deci[4] + genstat.res_deci[5]
                room_list.other[4] = room_list.other[0] / exchg_rate
                room_list.other[5] = room_list.other[1] / exchg_rate
                room_list.other[6] = room_list.other[2] / exchg_rate
                room_list.other[7] = room_list.other[3] / exchg_rate

                if genstat.res_date[0] == genstat.res_date[1] and not rmsharer and genstat.res_logic[1]:

                    if not dayuse_list or not(dayuse_list.datum == genstat.datum):
                        dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == genstat.datum), first=True)

                    if not dayuse_list:
                        dayuse_list = Dayuse_list()
                        dayuse_list_list.append(dayuse_list)

                        dayuse_list.datum = genstat.datum


                    dayuse_list.zimmeranz = dayuse_list.zimmeranz + 1

                for fixleist in db_session.query(Fixleist).filter(
                        (Fixleist.resnr == genstat.resnr) &  (Fixleist.reslinnr == genstat.res_int[0])).order_by(Fixleist._recid).all():

                    if not res_line or not(res_line.resnr == genstat.resnr and res_line.reslinnr == genstat.res_int[0]):
                        res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()
                    post_it = check_fixleist_posted(genstat.datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                    service =  to_decimal("0")
                    vat =  to_decimal("0")
                    fcost =  to_decimal("0")

                    if post_it:

                        if not artikel or not(artikel.artnr == fixleist.artnr and artikel.departement == fixleist.departement):
                            artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()

                        if artikel:
                            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))
                        fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                        fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

                        if show_rev == 1:
                            room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                            tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)

                        elif show_rev == 2:
                            room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                            room_list.fixleist2 =  to_decimal(room_list.fixleist2) + to_decimal((fcost) / to_decimal(exchg_rate) )
                            tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)
                            tot_fixcost2 =  to_decimal(tot_fixcost2) + to_decimal((fcost) / to_decimal(exchg_rate) )

        if not htparam or not(htparam.paramnr == 144):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        if not waehrung or not(waehrung.wabkurz == htparam.fchar):
            waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")
        d2 = d2 + timedelta(days=1)

        if to_date >= ci_date:

            for res_line in db_session.query(Res_line).filter(
                    (((Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.active_flag <= 1) &  (not_ (Res_line.ankunft > to_date)) &  (not_ (Res_line.abreise < d2)))) |  (((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date))) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                if not reservation or not(reservation.resnr == res_line.resnr):
                    reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()
                curr_i = 0
                dayuse_flag = False

                if not vhp_limited:
                    do_it = True
                else:

                    if not segment or not(segment.segmentcode == reservation.segmentcode):
                        segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:
                    dayuse_flag = True

                    if not arrangement or not(arrangement.arrangement == res_line.arrangement):
                        arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.arrangement == res_line.arrangement)).first()

                    if not bill_line or not(bill_line.departement == 0 and bill_line.artnr == arrangement.argt_artikelnr and bill_line.bill_datum == ci_date and bill_line.massnr == res_line.resnr and bill_line.billin_nr == res_line.reslinnr):
                        bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                    do_it = None != bill_line

                if do_it and not all_segm:

                    if not s_list or not(s_list.segm == reservation.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == reservation.segmentcode) &  (S_list.selected)).first()
                    do_it = None != s_list

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == res_line.arrangement and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == res_line.arrangement) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == res_line.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == res_line.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if not zimmer or not(zimmer.zinr == res_line.zinr):
                    zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if do_it and zimmer:

                    if not queasy or not(queasy.key == 14 and queasy.char1 == res_line.zinr and queasy.date1 <= datum and queasy.date2 >= datum):
                        queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                    if zimmer.sleeping:

                        if queasy and queasy.number3 == res_line.gastnr:
                            do_it = False
                    else:

                        if queasy and queasy.number3 != res_line.gastnr:
                            pass
                        else:
                            do_it = False
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    if not s_list or not(s_list.segm == reservation.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == reservation.segmentcode) &  (S_list.selected)).first()
                    kont_doit = None != s_list

                if excl_compl and do_it:

                    if not segment or not(segment.segmentcode == reservation.segmentcode and (segment.betriebsnr == 1 or segment.betriebsnr == 2)):
                        segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == reservation.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                    if segment:
                        do_it = False


                    else:

                        if res_line.zipreis == 0 and res_line.gratis != 0:
                            do_it = False

                if do_it and not all_outlook:

                    if not zimmer or not(zimmer.zinr == res_line.zinr):
                        zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == res_line.zinr)).first()

                    if zimmer:

                        if not o_list or not(o_list.SELECTED  and o_list.outlook_nr == zimmer.typ):
                            o_list = db_session.query(O_list).filter(
                                (O_list.SELECTED) &  (O_list.outlook_nr == zimmer.typ)).first()
                        do_it = None != o_list

                if do_it:

                    if dayuse_flag:

                        if not dayuse_list or not(dayuse_list.datum == datum):
                            dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == datum), first=True)

                        if not dayuse_list:
                            dayuse_list = Dayuse_list()
                            dayuse_list_list.append(dayuse_list)

                            dayuse_list.datum = res_line.ankunft

                        if not res_line.zimmerfix:
                            dayuse_list.zimmeranz = dayuse_list.zimmeranz + 1
                        dayuse_list.pax = dayuse_list.pax + res_line.erwachs + res_line.kind1
                    datum1 = d2

                    if res_line.ankunft > datum1:
                        datum1 = res_line.ankunft
                    datum2 = to_date

                    if res_line.abreise < datum2:
                        datum2 = res_line.abreise
                    for datum in date_range(datum1,datum2) :
                        pax = res_line.erwachs
                        net_lodg =  to_decimal("0")
                        curr_i = curr_i + 1

                        if res_line.zipreis != 0:

                            if not reslin_queasy or not(reslin_queasy.key.lower()  == ("arrangement").lower()  and reslin_queasy.resnr == res_line.resnr and reslin_queasy.reslinnr == res_line.reslinnr and reslin_queasy.date1 <= datum and reslin_queasy.date2 >= datum):
                                reslin_queasy = db_session.query(Reslin_queasy).filter(
                                    (func.lower(Reslin_queasy.key) == ("arrangement").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                            if reslin_queasy and reslin_queasy.number3 != 0:
                                pax = reslin_queasy.number3

                        if not room_list or not(room_list.datum == datum):
                            room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)
                        consider_it = True

                        if res_line.zimmerfix:

                            if not rline1 or not(rline1.resnr == res_line.resnr and rline1.reslinnr != res_line.reslinnr and rline1.resstatus == 8 and rline1.abreise >= datum):
                                rline1 = db_session.query(Rline1).filter(
                                    (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise >= datum)).first()

                            if rline1:
                                consider_it = False

                        if datum == res_line.abreise:
                            pass
                        else:
                            net_lodg =  to_decimal("0")
                            tot_breakfast =  to_decimal("0")
                            tot_lunch =  to_decimal("0")
                            tot_dinner =  to_decimal("0")
                            tot_other =  to_decimal("0")

                            if (show_rev == 1 or show_rev == 2) and res_line.zipreis > 0:

                                if incl_tent == False:

                                    if res_line.resstatus != 3:
                                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                                else:
                                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                            room_list.other[0] = room_list.other[0] + tot_breakfast
                            room_list.other[1] = room_list.other[1] + tot_lunch
                            room_list.other[2] = room_list.other[2] + tot_dinner
                            room_list.other[3] = room_list.other[3] + tot_other
                            room_list.other[4] = room_list.other[0] / exchg_rate
                            room_list.other[5] = room_list.other[1] / exchg_rate
                            room_list.other[6] = room_list.other[2] / exchg_rate
                            room_list.other[7] = room_list.other[3] / exchg_rate

                            for fixleist in db_session.query(Fixleist).filter(
                                    (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                                service =  to_decimal("0")
                                vat =  to_decimal("0")
                                fcost =  to_decimal("0")

                                if post_it:

                                    if not artikel or not(artikel.artnr == fixleist.artnr and artikel.departement == fixleist.departement):
                                        artikel = db_session.query(Artikel).filter(
                                            (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()

                                    if artikel:
                                        service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))
                                    fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                                    fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

                                    if show_rev == 1:
                                        room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                                        tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)

                                    elif show_rev == 2:
                                        room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                                        room_list.fixleist2 =  to_decimal(room_list.fixleist2) + to_decimal((fcost) / to_decimal(exchg_rate) )
                                        tot_fixcost2 =  to_decimal(tot_fixcost2) + to_decimal((fcost) / to_decimal(exchg_rate) )
                                        tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)

                        if datum == res_line.ankunft and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and consider_it:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                room_list.room[2] = room_list.room[2] + res_line.zimmeranz
                                room_list.lodg[1] = room_list.lodg[1] + net_lodg
                                rm_array[2] = rm_array[2] + res_line.zimmeranz
                                t_lodg[1] = t_lodg[1] + net_lodg

                                if (res_line.kontignr < 0) and kont_doit:
                                    room_list.room[15] = room_list.room[15] - res_line.zimmeranz
                                    rm_array[15] = rm_array[15] - res_line.zimmeranz
                            room_list.room[3] = room_list.room[3] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[3] = rm_array[3] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                            if (res_line.kontignr < 0) and kont_doit:

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    room_list.room[15] = room_list.room[15] - res_line.zimmeranz
                                    rm_array[15] = rm_array[15] - res_line.zimmeranz


                                room_list.room[16] = room_list.room[16] -\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                rm_array[16] = rm_array[16] -\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz

                                if not kontline or not(kontline.gastnr == res_line.gastnr and kontline.ankunft == datum and kontline.zikatnr == res_line.zikatnr and kontline.betriebsnr == 1 and kontline.kontstat == 1):
                                    kontline = db_session.query(Kontline).filter(
                                        (Kontline.gastnr == res_line.gastnr) &  (Kontline.ankunft == datum) &  (Kontline.zikatnr == res_line.zikatnr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

                                if kontline:
                                    room_list.k_pax = room_list.k_pax +\
                                            (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz -\
                                            (kontline.erwachs + kontline.kind1) *\
                                            res_line.zimmeranz
                                    rm_array[17] = rm_array[17] +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz -\
                                        (kontline.erwachs + kontline.kind1) *\
                                        res_line.zimmeranz

                            if res_line.ankunft <= res_line.abreise or dayuse_flag:

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                                    room_list.room[6] = room_list.room[6] + res_line.zimmeranz
                                    room_list.lodg[3] = room_list.lodg[3] + net_lodg
                                    room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                                    t_lodg[3] = t_lodg[3] + net_lodg
                                    t_lodg[5] = t_lodg[5] + (net_lodg / exchg_rate)
                                    rm_array[6] = rm_array[6] + res_line.zimmeranz

                                    if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                        room_list.room_comp = room_list.room_comp + res_line.zimmeranz
                                        t_room_comp = t_room_comp + res_line.zimmeranz
                                    else:
                                        room_list.lodg[4] = room_list.lodg[4] + net_lodg
                                        t_lodg[4] = t_lodg[4] + net_lodg
                                        room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(tot_rmrev)
                                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                                    room_list.room_exccomp = room_list.room[6] - room_list.room_comp
                                    t_lodg[6] = t_lodg[6] + (net_lodg / exchg_rate)
                                    room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                    room_list.room[7] = room_list.room[7] +\
                                            (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz
                                    rm_array[7] = rm_array[7] +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz

                        if datum == res_line.abreise and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and consider_it:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                room_list.room[4] = room_list.room[4] + res_line.zimmeranz
                                room_list.lodg[2] = room_list.lodg[2] + net_lodg
                                t_lodg[2] = t_lodg[2] + net_lodg
                                rm_array[4] = rm_array[4] + res_line.zimmeranz

                                if datum != curr_date:
                                    room_list.lodg[0] = room_list.lodg[0] + net_lodg
                            room_list.room[5] = room_list.room[5] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[5] = rm_array[5] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                        if (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != datum and res_line.abreise != datum):

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                                room_list.room[6] = room_list.room[6] + res_line.zimmeranz
                                room_list.lodg[3] = room_list.lodg[3] + net_lodg
                                room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                                rm_array[6] = rm_array[6] + res_line.zimmeranz
                                t_lodg[3] = t_lodg[3] + net_lodg


                                t_lodg[5] = t_lodg[5] + (net_lodg / exchg_rate)

                                if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                    room_list.room_comp = room_list.room_comp + res_line.zimmeranz
                                    t_room_comp = t_room_comp + res_line.zimmeranz
                                else:
                                    room_list.lodg[4] = room_list.lodg[4] + net_lodg
                                    t_lodg[4] = t_lodg[4] + net_lodg
                                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                                    t_lodg[6] = t_lodg[6] + (net_lodg / exchg_rate)
                                    room_list.room_exccomp = room_list.room[6] - room_list.room_comp
                                    room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(tot_rmrev)
                                    room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)

                                if datum != curr_date:
                                    room_list.lodg[0] = room_list.lodg[0] + net_lodg

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                room_list.room[7] = room_list.room[7] +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                rm_array[7] = rm_array[7] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                            if (res_line.kontignr < 0) and kont_doit:
                                room_list.room[15] = room_list.room[15] - res_line.zimmeranz
                                rm_array[15] = rm_array[15] - res_line.zimmeranz


                                room_list.room[16] = room_list.room[16] -\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                rm_array[16] = rm_array[16] -\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz

                                if not kontline or not(kontline.gastnr == res_line.gastnr and kontline.ankunft == datum and kontline.zikatnr == res_line.zikatnr and kontline.betriebsnr == 1 and kontline.kontstat == 1):
                                    kontline = db_session.query(Kontline).filter(
                                        (Kontline.gastnr == res_line.gastnr) &  (Kontline.ankunft == datum) &  (Kontline.zikatnr == res_line.zikatnr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

                                if kontline:
                                    room_list.k_pax = room_list.k_pax +\
                                            (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                            res_line.gratis) * res_line.zimmeranz -\
                                            (kontline.erwachs + kontline.kind1) *\
                                            res_line.zimmeranz
                                    rm_array[17] = rm_array[17] +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz -\
                                        (kontline.erwachs + kontline.kind1) *\
                                        res_line.zimmeranz

                        if res_line.resstatus == 3 and datum < res_line.abreise:
                            room_list.room[12] = room_list.room[12] + res_line.zimmeranz
                            rm_array[12] = rm_array[12] + res_line.zimmeranz
                            room_list.t_pax = room_list.t_pax + (res_line.erwachs * res_line.zimmeranz)
                            tent_pers = tent_pers + (res_line.erwachs * res_line.zimmeranz)
                            room_list.lodg[3] = room_list.lodg[3] + net_lodg


                            room_list.lodg[5] = room_list.lodg[3] / exchg_rate

                            if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                room_list.room_comp = room_list.room_comp + res_line.zimmeranz
                                t_room_comp = t_room_comp + res_line.zimmeranz
                            else:
                                room_list.lodg[4] = room_list.lodg[4] + net_lodg
                                t_lodg[4] = t_lodg[4] + net_lodg
                                room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                                t_lodg[6] = t_lodg[6] + (net_lodg / exchg_rate)
                                room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(tot_rmrev)
                                room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)

                        if res_line.kontignr > 0 and res_line.active_flag <= 1 and res_line.resstatus <= 6 and res_line.resstatus != 3 and res_line.resstatus != 4 and res_line.abreise > datum:

                            if not kline or not(kline.kontignr == res_line.kontignr and kline.kontstat == 1):
                                kline = db_session.query(Kline).filter(
                                    (Kline.kontignr == res_line.kontignr) &  (Kline.kontstat == 1)).first()

                            if kline:

                                if not kontline or not(kontline.kontcode == kline.kontcode and kontline.ankunft <= datum and kontline.abreise >= datum and kontline.betriebsnr == 0 and kontline.kontstat == 1):
                                    kontline = db_session.query(Kontline).filter(
                                        (Kontline.kontcode == kline.kontcode) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).first()

                                if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                                    room_list.room[13] = room_list.room[13] - res_line.zimmeranz
                                    rm_array[13] = rm_array[13] - res_line.zimmeranz

        for datum in date_range(d2,to_date) :

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == kontline.arrangement and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == kontline.arrangement) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == kontline.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == kontline.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if do_it and not all_segm:

                    if not guest or not(guest.gastnr == kontline.gastnr):
                        guest = db_session.query(Guest).filter(
                            (Guest.gastnr == kontline.gastnr)).first()

                    if not guestseg or not(guestseg.gastnr == guest.gastnr and guestseg.reihenfolge == 1):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        if not guestseg or not(guestseg.gastnr == guest.gastnr):
                            guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        if not s_list or not(s_list.segm == guestseg.segmentcode and s_list.selected):
                            s_list = db_session.query(S_list).filter(
                                (S_list.segm == guestseg.segmentcode) &  (S_list.selected)).first()
                        do_it = None != s_list

                if excl_compl and do_it:

                    if not guest or not(guest.gastnr == kontline.gastnr):
                        guest = db_session.query(Guest).filter(
                            (Guest.gastnr == kontline.gastnr)).first()

                    if not guestseg or not(guestseg.gastnr == guest.gastnr and guestseg.reihenfolge == 1):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        if not guestseg or not(guestseg.gastnr == guest.gastnr):
                            guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        if not segment or not(segment.segmentcode == guestseg.segmentcode and (segment.betriebsnr == 1 or segment.betriebsnr == 2)):
                            segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == guestseg.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                if do_it:

                    if not room_list or not(room_list.datum == datum):
                        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)
                    room_list.room[15] = room_list.room[15] + kontline.zimmeranz
                    room_list.room[16] = room_list.room[16] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz
                    rm_array[15] = rm_array[15] + kontline.zimmeranz
                    rm_array[16] = rm_array[16] + (kontline.erwachs + kontline.kind1) * kontline.zimmeranz

        for room_list in query(room_list_list):

            if room_list.room[15] > 0:
                room_list.room[6] = room_list.room[6] + room_list.room[15]
                room_list.room[7] = room_list.room[7] + room_list.room[16] + room_list.k_pax

            if incl_tent:
                room_list.room[7] = room_list.room[7] + room_list.t_pax

        if rm_array[15] > 0:
            rm_array[6] = rm_array[6] + rm_array[15]
            rm_array[7] = rm_array[7] + rm_array[16] + rm_array[17]

        if incl_tent:
            rm_array[7] = rm_array[7] + tent_pers


        datum = curr_date - timedelta(days=1)
        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)

            if not room_list or not(room_list.datum == datum):
                room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

            queasy_obj_list = []
            for queasy, zimmer in db_session.query(Queasy, Zimmer).join(Zimmer,(Zimmer.zinr == Queasy.char1) &  (Zimmer.sleeping)).filter(
                    (Queasy.key == 14) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy._recid in queasy_obj_list:
                    continue
                else:
                    queasy_obj_list.append(queasy._recid)

                if not guestseg or not(guestseg.gastnr == queasy.number3 and guestseg.reihenfolge == 1):
                    guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == queasy.number3) &  (Guestseg.reihenfolge == 1)).first()

                if not guestseg:

                    if not guestseg or not(guestseg.gastnr == queasy.number3):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == queasy.number3)).first()
                do_it = None != guestseg

                if not all_segm and do_it:

                    if not s_list or not(s_list.segm == guestseg.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == guestseg.segmentcode) &  (S_list.selected)).first()
                    do_it = None != s_list

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == queasy.char2 and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == queasy.char2) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if do_it:
                    room_list.room[6] = room_list.room[6] + 1
                    room_list.room[7] = room_list.room[7] + queasy.number1
                    rm_array[6] = rm_array[6] + 1
                    rm_array[7] = rm_array[7] + queasy.number1
        cal_lastday_occ()
        p_room = 0
        p_pax = 0
        prev_room = 0
        datum = curr_date - timedelta(days=1)


        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)
            anzahl_dayuse = 0


            tot_room = get_active_room(datum)
            accum_tot_room = accum_tot_room + tot_room

            if not dayuse_list or not(dayuse_list.datum == datum):
                dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == datum), first=True)

            if dayuse_list:
                anzahl_dayuse = dayuse_list.zimmeranz

            if not room_list or not(room_list.datum == datum):
                room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

            if tot_room != 0:
                room_list.room[8] = room_list.room[6] / tot_room * 100
                prev_room = prev_room + room_list.room[6]
                room_list.room[9] = prev_room / accum_tot_room * 100
                room_list.rmocc_exclcomp = ( to_decimal(room_list.room[6]) - to_decimal(room_list.room_comp)) / to_decimal(tot_room) * to_decimal("100")

            if (room_list.room[6] - anzahl_dayuse) < tot_room:
                room_list.room[10] = tot_room - room_list.room[6] + anzahl_dayuse
                rm_array[10] = rm_array[10] + tot_room - room_list.room[6] + anzahl_dayuse
            else:
                room_list.room[11] = room_list.room[6] - tot_room - anzahl_dayuse
                rm_array[11] = rm_array[11] + room_list.room[6] - tot_room - anzahl_dayuse

            if i > 1:
                room_list.room[0] = p_room
                room_list.room[1] = p_pax
                rm_array[0] = rm_array[0] + p_room
                rm_array[1] = rm_array[1] + p_pax


            p_room = room_list.room[6]
            p_pax = room_list.room[7]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):

            if room_list.datum < ci_date:

                if not zinrstat or not(zinrstat.zinr.lower()  == ("ooo").lower()  and zinr.datum == room_list.datum):
                    zinrstat = db_session.query(Zinrstat).filter(
                        (func.lower(Zinrstat.zinr) == ("ooo").lower()) &  (Zinrstat.datum == room_list.datum)).first()

                if zinrstat:

                    if not all_zikat:

                        if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                            z_list = db_session.query(Z_list).filter(
                                (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()

                        if z_list:
                            room_list.room[14] = zinrstat.zimmeranz
                            rm_array[14] = rm_array[14] + zinrstat.zimmeranz


                    else:
                        room_list.room[14] = zinrstat.zimmeranz
                        rm_array[14] = rm_array[14] + zinrstat.zimmeranz


            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).filter(
                        (Outorder.gespstart <= room_list.datum) &  (Outorder.gespende >= room_list.datum) &  (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)

                    if not all_zikat:

                        if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                            z_list = db_session.query(Z_list).filter(
                                (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()

                        if z_list:
                            room_list.room[14] = room_list.room[14] + 1
                            rm_array[14] = rm_array[14] + 1


                    else:
                        room_list.room[14] = room_list.room[14] + 1
                        rm_array[14] = rm_array[14] + 1

            if exclooo:
                room_list.room[10] = room_list.room[10] - room_list.room[14]
                rm_array[10] = rm_array[10] - room_list.room[14]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):
            for i in range(1,8 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], ">>>>>>9")
            for i in range(9,10 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], " >>9.99")
            for i in range(11,15 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
            for i in range(16,17 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], ">>>>>>9")
        jml_date = to_date - curr_date + 1
        do_it = True

        if show_rev == 1 or show_rev == 2:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.SELECTED)):
                counter = counter + 1

                if not segment or not(segment.segmentcode == s_list.segm):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == s_list.segm)).first()

                if segment:

                    if tmin == 0 and counter == 1:

                        if segment.betriebsnr == 0:
                            tmin = 0


                        else:
                            tmin = segment.betriebsnr

                    if segment.betriebsnr > tmax:
                        tmax = segment.betriebsnr

                    if segment.betriebsnr < tmin:
                        tmin = segment.betriebsnr

            if tmax <= 2 and tmin >= 1:
                do_it = False


            else:
                do_it = True

        if do_it:

            if incl_oth:

                for room_list in query(room_list_list):
                    othrev = calc_othrev(room_list.datum)

                    if room_list.datum < ci_date:

                        if not htparam or not(htparam.paramnr == 144):
                            htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 144)).first()

                        if not waehrung or not(waehrung.wabkurz == htparam.fchar):
                            waehrung = db_session.query(Waehrung).filter(
                                (Waehrung.wabkurz == htparam.fchar)).first()

                        if waehrung:

                            if not exrate or not(exrate.datum == room_list.datum and exrate.artnr == waehrung.waehrungsnr):
                                exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == room_list.datum) &  (Exrate.artnr == waehrung.waehrungsnr)).first()

                            if exrate:
                                exchg_rate =  to_decimal(exrate.betrag)
                    else:

                        if not htparam or not(htparam.paramnr == 144):
                            htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 144)).first()

                        if not waehrung or not(waehrung.wabkurz == htparam.fchar):
                            waehrung = db_session.query(Waehrung).filter(
                                (Waehrung.wabkurz == htparam.fchar)).first()

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                        else:
                            exchg_rate =  to_decimal("1")
                    room_list.lodg[4] = room_list.lodg[4] + othrev
                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate

                    if room_list.wd != 0:
                        t_lodg[4] = t_lodg[4] + othrev


                    t_lodg[6] = t_lodg[6] + (othrev / exchg_rate)

        for room_list in query(room_list_list):
            tot_avrg =  to_decimal(tot_avrg) + to_decimal(room_list.room[8])

            if (room_list.room[6] - room_list.room[15]) != 0:
                room_list.avrglodg =  to_decimal(room_list.lodg[3]) / to_decimal((room_list.room[6] - room_list.room[15]))
            room_list.avrglodg2 =  to_decimal(room_list.avrglodg) / to_decimal(exchg_rate)

            if (room_list.room_exccomp - room_list.room[15]) != 0:
                room_list.avrgrmrev =  to_decimal(room_list.lodg[4]) / to_decimal((room_list.room[6] - room_list.room[15]) )
                room_list.avrgrmrev2 =  to_decimal(room_list.avrgrmrev) / to_decimal(exchg_rate)

            if room_list.wd != 0:
                troom_exccomp = troom_exccomp + (room_list.room[6] - room_list.room[15])

            if ((to_decimal(room_list.coom[8]) * room_list.avrgrmrev) / 100) != 0:
                room_list.revpar = ( to_decimal(to_decimal(room_list.coom[8])) * to_decimal(room_list.avrgrmrev)) / to_decimal("100")
                room_list.revpar2 =  to_decimal(room_list.revpar) / to_decimal(exchg_rate)


            room_list.avrglodg_inclcomp =  to_decimal(room_list.lodg[4]) / to_decimal(room_list.room[6])
            room_list.avrglodg_exclcomp =  to_decimal(room_list.lodg[4]) / to_decimal((room_list.room[6]) - to_decimal(room_list.room_comp))
        tavg_rmrev =  to_decimal(t_lodg[4]) / to_decimal(troom_exccomp)
        tavg_rmrev2 =  to_decimal(tavg_rmrev) / to_decimal(exchg_rate)
        t_avrglodg_inclcomp =  to_decimal(t_lodg[4]) / to_decimal(rm_array[6])
        t_avrglodg_exclcomp =  to_decimal(t_lodg[4]) / to_decimal((rm_array[6]) - to_decimal(t_room_comp))
        avrg_rate =  to_decimal(tot_avrg) / to_decimal(jml_date)
        mtd_tot_room = get_mtd_active_room()
        mtd_occ =  to_decimal("0")

        if mtd_tot_room != 0:
            mtd_occ =  to_decimal(rm_array[6]) / to_decimal(mtd_tot_room) * to_decimal("100")
            t_rmocc_exclcomp = ( to_decimal(rm_array[6]) - to_decimal(t_room_comp)) / to_decimal(mtd_tot_room) * to_decimal("100")

        if not room_list or not(room_list.wd == 0):
            room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)
        for i in range(1,8 + 1) :
            room_list.room[i - 1] = rm_array[i - 1]
        for i in range(11,17 + 1) :
            room_list.room[i - 1] = rm_array[i - 1]
        for i in range(1,8 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], ">>>>>>9")
        for i in range(11,12 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], ">>>>>>>")
        room_list.room[8] = mtd_occ
        room_list.coom[8] = to_string(mtd_occ, " >>9.99")
        room_list.coom[9] = to_string(avrg_rate, " >>9.99")
        room_list.coom[12] = to_string(rm_array[12], ">>>>>>>")
        room_list.coom[13] = to_string(rm_array[13], ">>>>>>>")
        room_list.coom[14] = to_string(rm_array[14], ">>>>>>>")
        room_list.lodg[1] = t_lodg[1]
        room_list.lodg[2] = t_lodg[2]
        room_list.lodg[3] = t_lodg[3]
        room_list.lodg[4] = t_lodg[4]
        room_list.lodg[5] = t_lodg[5]
        room_list.lodg[6] = t_lodg[6]


        for i in range(16,17 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
        mtd_occ =  to_decimal("0")
        avrg_lodging =  to_decimal("0")
        avrg_rmrate =  to_decimal("0")

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):
            avrg_lodging =  to_decimal(avrg_lodging) + to_decimal(room_list.avrglodg)
            avrg_rmrate =  to_decimal(avrg_rmrate) + to_decimal(room_list.avrgrmrev)
            avrg_lodging2 =  to_decimal(avrg_lodging2) + to_decimal(room_list.avrglodg2)
            avrg_rmrate2 =  to_decimal(avrg_rmrate2) + to_decimal(room_list.avrgrmrev2)
            mtd_occ =  to_decimal(mtd_occ) + to_decimal(room_list.room[8])
            sum_breakfast =  to_decimal(sum_breakfast) + to_decimal(room_list.other[0])
            sum_lunch =  to_decimal(sum_lunch) + to_decimal(room_list.other[1])
            sum_dinner =  to_decimal(sum_dinner) + to_decimal(room_list.other[2])
            sum_other =  to_decimal(sum_other) + to_decimal(room_list.other[3])
            sum_breakfast_usd =  to_decimal(sum_breakfast_usd) + to_decimal(room_list.other[4])
            sum_lunch_usd =  to_decimal(sum_lunch_usd) + to_decimal(room_list.other[5])
            sum_dinner_usd =  to_decimal(sum_dinner_usd) + to_decimal(room_list.other[6])
            sum_other_usd =  to_decimal(sum_other_usd) + to_decimal(room_list.other[7])
            sum_comp =  to_decimal(sum_comp) + to_decimal(room_list.room_comp)
            t_revpar =  to_decimal(t_revpar) + to_decimal(room_list.revpar)
            t_revpar2 =  to_decimal(t_revpar2) + to_decimal(room_list.revpar2)
            t_rmrate =  to_decimal(t_rmrate) + to_decimal(room_list.rmrate)
            t_rmrate2 =  to_decimal(t_rmrate2) + to_decimal(room_list.rmrate2)

        if not room_list or not(room_list.wd == 0):
            room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)

        if tavg_rmrev == None:
            tavg_rmrev =  to_decimal("0")

        if tavg_rmrev2 == None:
            tavg_rmrev2 =  to_decimal("0")
        room_list.avrglodg =  to_decimal(avrg_lodging) / to_decimal((to_date) - to_decimal(curr_date) + to_decimal("1") )
        room_list.avrglodg2 =  to_decimal(avrg_lodging2) / to_decimal((to_date) - to_decimal(curr_date) + to_decimal("1") )
        room_list.avrgrmrev =  to_decimal(tavg_rmrev)
        room_list.avrgrmrev2 =  to_decimal(tavg_rmrev2)
        room_list.other[0] = sum_breakfast
        room_list.other[1] = sum_lunch
        room_list.other[2] = sum_dinner
        room_list.other[3] = sum_other
        room_list.other[4] = sum_breakfast_usd
        room_list.other[5] = sum_lunch_usd
        room_list.other[6] = sum_dinner_usd
        room_list.other[7] = sum_other_usd
        room_list.room_comp = sum_comp
        room_list.rmrate =  to_decimal(t_rmrate)
        room_list.rmrate2 =  to_decimal(t_rmrate2)
        room_list.fixleist =  to_decimal(tot_fixcost)
        room_list.fixleist2 =  to_decimal(tot_fixcost2)
        room_list.avrglodg_inclcomp =  to_decimal(t_avrglodg_inclcomp)
        room_list.avrglodg_exclcomp =  to_decimal(t_avrglodg_exclcomp)
        room_list.rmocc_exclcomp =  to_decimal(t_rmocc_exclcomp)

        if ((to_decimal(room_list.coom[8]) * room_list.avrgrmrev) / 100) != 0:
            room_list.revpar = ( to_decimal(to_decimal(room_list.coom[8])) * to_decimal(room_list.avrgrmrev)) / to_decimal("100")
            room_list.revpar2 =  to_decimal(room_list.revpar) / to_decimal(exchg_rate)

        if room_list.room[6] != 0:
            room_list.avrglodg =  to_decimal(room_list.lodg[3]) / to_decimal(room_list.room[6])


        room_list.avrglodg2 =  to_decimal(room_list.avrglodg) / to_decimal(exchg_rate)


    def segm_code_name():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        a:int = 0
        d:int = 79
        e:int = 0
        r:int = 1
        counter:int = 0
        Bsegm = Segm_list
        bsegm_list = segm_list_list
        segm_name = ""
        print_list_list.clear()

        if all_segm:
            segm_name = "ALL"

        elif not all_segm:

            for bsegm in query(bsegm_list, filters=(lambda bsegm: bsegm.SELECTED)):
                segm_name = segm_name + substring(bsegm.bezeich, 4, len(bsegm.bezeich) - 3) + "; "
            segm_name = substring(segm_name, 0, len(segm_name) - 2)
        a = len(segm_name)
        a = len(segm_name)

        if a > 80:
            for e in range(1,a + 1) :
                counter = counter + 1
                print_list = Print_list()
                print_list_list.append(print_list)

                print_list.code_name = substring(segm_name, e - 1, 80)
                e = (counter * 80) + 1
        else:
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.code_name = substring(segm_name, r - 1, a)

            if substring(code_name, 0, 1) == " ":
                print_list.code_name = substring(code_name, 1, (len(code_name) - 1))


    def argt_code_name():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        a:int = 0
        d:int = 79
        e:int = 0
        r:int = 1
        str_cut:str = ""
        Bargt = Argt_list
        bargt_list = argt_list_list
        argm_name = ""
        print_list2_list.clear()

        if all_argt:
            argm_name = "ALL"

        elif not all_argt:

            for bargt in query(bargt_list, filters=(lambda bargt: bargt.SELECTED)):
                argm_name = argm_name + bargt.bezeich + "; "
            argm_name = substring(argm_name, 0, len(argm_name) - 2)
        a = len(argm_name)
        a = len(argm_name)

        if a > 80:
            print_list2 = Print_list2()
            print_list2_list.append(print_list2)

            argm = substring(argm_name, r + 1 - 1, a)

            if substring(argm, 0, 1) == " ":
                argm = substring(argm, 1, (len(argm) - 1))
        else:
            print_list2 = Print_list2()
            print_list2_list.append(print_list2)

            argm = substring(argm_name, r - 1, a)

            if substring(argm, 0, 1) == " ":
                argm = substring(argm, 1, (len(argm) - 1))


    def room_code_name():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        a:int = 0
        d:int = 79
        e:int = 0
        r:int = 1
        curr_time:int = 0
        Broom = Zikat_list
        broom_list = zikat_list_list
        room_name = ""
        print_list3_list.clear()

        if all_zikat:
            room_name = "ALL"

        elif not all_zikat:
            curr_time = get_current_time_in_seconds()

            for broom in query(broom_list, filters=(lambda broom: broom.SELECTED)):
                room_name = room_name + broom.bezeich + "; "
            room_name = substring(room_name, 0, len(room_name) - 2)
        curr_time = get_current_time_in_seconds()


        a = len(room_name)
        a = len(room_name)

        if a > 80:
            print_list3 = Print_list3()
            print_list3_list.append(print_list3)

            room = substring(room_name, r + 1 - 1, a)

            if substring(room, 0, 1) == " ":
                room = substring(room, 1, (len(room) - 1))
        else:
            print_list3 = Print_list3()
            print_list3_list.append(print_list3)

            room = substring(room_name, r - 1, a)

            if substring(room, 0, 1) == " ":
                room = substring(room, 1, (len(room) - 1))


    def create_browse1():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        p_lodg:decimal = to_decimal("0.0")
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        dayuse_flag:bool = False
        n:int = 0
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:decimal = to_decimal("0.0")
        net_lodg:decimal = to_decimal("0.0")
        fnet_lodg:decimal = to_decimal("0.0")
        curr_i:int = 0
        rsvstat:str = ""
        avrg_lodging:decimal = to_decimal("0.0")
        anzahl_dayuse:int = 0
        kline = None
        tot_breakfast:decimal = to_decimal("0.0")
        tot_lunch:decimal = to_decimal("0.0")
        tot_dinner:decimal = to_decimal("0.0")
        tot_other:decimal = to_decimal("0.0")
        tot_fixcost:decimal = to_decimal("0.0")
        tot_fixcost2:decimal = to_decimal("0.0")
        sum_breakfast:decimal = to_decimal("0.0")
        sum_lunch:decimal = to_decimal("0.0")
        sum_dinner:decimal = to_decimal("0.0")
        sum_other:decimal = to_decimal("0.0")
        sum_breakfast_usd:decimal = to_decimal("0.0")
        sum_lunch_usd:decimal = to_decimal("0.0")
        sum_dinner_usd:decimal = to_decimal("0.0")
        sum_other_usd:decimal = to_decimal("0.0")
        tot_vat:decimal = to_decimal("0.0")
        tot_service:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        tavg_rmrev:decimal = to_decimal("0.0")
        tavg_rmrev2:decimal = to_decimal("0.0")
        troom_exccomp:int = 0
        othrev:decimal = to_decimal("0.0")
        t_avrglodg_inclcomp:decimal = to_decimal("0.0")
        t_avrglodg_exclcomp:decimal = to_decimal("0.0")
        t_rmocc_exclcomp:decimal = to_decimal("0.0")
        t_room_comp:int = 0
        curr_time:int = 0
        tmax:int = 0
        tmin:int = 0
        counter:int = 0
        jml1:int = 0
        jml2:decimal = to_decimal("0.0")
        jml3:decimal = to_decimal("0.0")
        S_list = Segm_list
        s_list_list = segm_list_list
        A_list = Argt_list
        a_list_list = argt_list_list
        Z_list = Zikat_list
        z_list_list = zikat_list_list
        Kline =  create_buffer("Kline",Kontline)
        O_list = Outlook_list
        o_list_list = outlook_list_list
        tent_pers = 0
        for i in range(1,18 + 1) :
            rm_array[i - 1] = 0

            if i < 5:
                t_lodg[i - 1] = 0
        room_list_list.clear()
        tot_room = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                    z_list = db_session.query(Z_list).filter(
                        (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()

                if z_list:
                    tot_room = tot_room + 1
        datum = curr_date - timedelta(days=1)
        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)
            wd = get_weekday(datum) - 1

            if wd == 0:
                wd = 7
            rsvstat = rsv_closeout(datum)
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.wd = wd
            room_list.datum = datum
            room_list.bezeich = " " + week_list[wd - 1] + " " + to_string(datum) + rsvstat

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                allot_doit = True

                if kontline.zikatnr != 0 and not all_zikat:

                    if not z_list or not(z_list.zikatnr == kontline.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == kontline.zikatnr) &  (Z_list.selected)).first()
                    allot_doit = None != z_list

                if allot_doit and (datum >= (ci_date + timedelta(days=kontline.ruecktage))):
                    room_list.room[13] = room_list.room[13] + kontline.zimmeranz
                    rm_array[13] = rm_array[13] + kontline.zimmeranz
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.bezeich = " TOTAL"

        res_line_obj_list = []
        for res_line, waehrung in db_session.query(Res_line, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).filter(
                ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (not_ (Res_line.ankunft > to_date)) &  (not_ (Res_line.abreise < curr_date))) |  (((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.abreise == ci_date))) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.gastnr, Res_line.resnr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if not reservation or not(reservation.resnr == res_line.resnr):
                reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()
            curr_i = 0
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if not vhp_limited:
                do_it = True
            else:

                if not segment or not(segment.segmentcode == reservation.segmentcode):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode)).first()
                do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:
                dayuse_flag = True

                if not arrangement or not(arrangement.arrangement == res_line.arrangement):
                    arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.arrangement == res_line.arrangement)).first()

                if not bill_line or not(bill_line.departement == 0 and bill_line.artnr == arrangement.argt_artikelnr and bill_line.bill_datum == ci_date and bill_line.massnr == res_line.resnr and bill_line.billin_nr == res_line.reslinnr):
                    bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            if do_it and not all_segm:

                if not s_list or not(s_list.segm == reservation.segmentcode and s_list.selected):
                    s_list = db_session.query(S_list).filter(
                        (S_list.segm == reservation.segmentcode) &  (S_list.selected)).first()
                do_it = None != s_list

            if do_it and not all_argt:

                if not a_list or not(a_list.argt == res_line.arrangement and a_list.selected):
                    a_list = db_session.query(A_list).filter(
                        (A_list.argt == res_line.arrangement) &  (A_list.selected)).first()
                do_it = None != a_list

            if do_it and not all_zikat:

                if not z_list or not(z_list.zikatnr == res_line.zikatnr and z_list.selected):
                    z_list = db_session.query(Z_list).filter(
                        (Z_list.zikatnr == res_line.zikatnr) &  (Z_list.selected)).first()
                do_it = None != z_list
            kont_doit = True

            if do_it and (not all_segm) and (res_line.kontignr < 0):

                if not s_list or not(s_list.segm == reservation.segmentcode and s_list.selected):
                    s_list = db_session.query(S_list).filter(
                        (S_list.segm == reservation.segmentcode) &  (S_list.selected)).first()
                kont_doit = None != s_list

            if not zimmer or not(zimmer.zinr == res_line.zinr):
                zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if do_it and zimmer:

                if not queasy or not(queasy.key == 14 and queasy.char1 == res_line.zinr and queasy.date1 <= datum and queasy.date2 >= datum):
                    queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if excl_compl and do_it:

                if not segment or not(segment.segmentcode == reservation.segmentcode and (segment.betriebsnr == 1 or segment.betriebsnr == 2)):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == reservation.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                if segment:
                    do_it = False


                else:

                    if res_line.zipreis == 0 and res_line.gratis != 0:
                        do_it = False

            if do_it and not all_outlook:

                if not zimmer or not(zimmer.zinr == res_line.zinr):
                    zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()

                if zimmer:

                    if not o_list or not(o_list.SELECTED  and o_list.outlook_nr == zimmer.typ):
                        o_list = db_session.query(O_list).filter(
                            (O_list.SELECTED) &  (O_list.outlook_nr == zimmer.typ)).first()
                    do_it = None != o_list

            if do_it:

                if dayuse_flag:

                    if not dayuse_list or not(dayuse_list.datum == ci_date):
                        dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == ci_date), first=True)

                    if not dayuse_list:
                        dayuse_list = Dayuse_list()
                        dayuse_list_list.append(dayuse_list)

                        dayuse_list.datum = res_line.ankunft

                    if not res_line.zimmerfix:
                        dayuse_list.zimmeranz = dayuse_list.zimmeranz + 1
                    dayuse_list.pax = dayuse_list.pax + res_line.erwachs + res_line.kind1
                datum1 = curr_date

                if res_line.ankunft > datum1:
                    datum1 = res_line.ankunft
                datum2 = to_date

                if res_line.abreise < datum2:
                    datum2 = res_line.abreise
                for datum in date_range(datum1,datum2) :
                    pax = res_line.erwachs
                    curr_i = curr_i + 1
                    net_lodg =  to_decimal("0")

                    if res_line.zipreis != 0:

                        if not reslin_queasy or not(reslin_queasy.key.lower()  == ("arrangement").lower()  and reslin_queasy.resnr == res_line.resnr and reslin_queasy.reslinnr == res_line.reslinnr and reslin_queasy.date1 <= datum and reslin_queasy.date2 >= datum):
                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == ("arrangement").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.date1 <= datum) &  (Reslin_queasy.date2 >= datum)).first()

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3

                    if not room_list or not(room_list.datum == datum):
                        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)
                    consider_it = True

                    if res_line.zimmerfix:

                        if not rline1 or not(rline1.resnr == res_line.resnr and rline1.reslinnr != res_line.reslinnr and rline1.resstatus == 8 and rline1.abreise > datum):
                            rline1 = db_session.query(Rline1).filter(
                                (Rline1.resnr == res_line.resnr) &  (Rline1.reslinnr != res_line.reslinnr) &  (Rline1.resstatus == 8) &  (Rline1.abreise > datum)).first()

                        if rline1:
                            consider_it = False

                    if datum == res_line.abreise:
                        pass
                    else:

                        for fixleist in db_session.query(Fixleist).filter(
                                (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                            post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                            service =  to_decimal("0")
                            vat =  to_decimal("0")
                            fcost =  to_decimal("0")

                            if post_it:

                                if not artikel or not(artikel.artnr == fixleist.artnr and artikel.departement == fixleist.departement):
                                    artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == fixleist.artnr) &  (Artikel.departement == fixleist.departement)).first()

                                if artikel:
                                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))
                                fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                                fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

                                if show_rev == 1:
                                    room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                                    tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)

                                elif show_rev == 2:
                                    room_list.fixleist =  to_decimal(room_list.fixleist) + to_decimal(fcost)
                                    room_list.fixleist2 =  to_decimal(room_list.fixleist2) + to_decimal((fcost) / to_decimal(exchg_rate) )
                                    tot_fixcost2 =  to_decimal(tot_fixcost2) + to_decimal((fcost) / to_decimal(exchg_rate) )
                                    tot_fixcost =  to_decimal(tot_fixcost) + to_decimal(fcost)


                        net_lodg =  to_decimal("0")
                        tot_breakfast =  to_decimal("0")
                        tot_lunch =  to_decimal("0")
                        tot_dinner =  to_decimal("0")
                        tot_other =  to_decimal("0")
                        tot_rmrev =  to_decimal("0")

                        if (show_rev == 1 or show_rev == 2) and res_line.zipreis > 0:

                            if incl_tent == False:

                                if res_line.resstatus != 3:
                                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                            else:
                                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                        room_list.other[0] = room_list.other[0] + tot_breakfast
                        room_list.other[1] = room_list.other[1] + tot_lunch
                        room_list.other[2] = room_list.other[2] + tot_dinner
                        room_list.other[3] = room_list.other[3] + tot_other
                        room_list.other[4] = room_list.other[0] / exchg_rate
                        room_list.other[5] = room_list.other[1] / exchg_rate
                        room_list.other[6] = room_list.other[2] / exchg_rate
                        room_list.other[7] = room_list.other[3] / exchg_rate

                    if datum == res_line.ankunft and consider_it and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list.lodg[1] = room_list.lodg[1] + net_lodg
                            room_list.room[2] = room_list.room[2] + res_line.zimmeranz
                            rm_array[2] = rm_array[2] + res_line.zimmeranz
                            t_lodg[1] = t_lodg[1] + net_lodg

                            if (res_line.kontignr < 0) and kont_doit:
                                room_list.room[15] = room_list.room[15] - res_line.zimmeranz
                                rm_array[15] = rm_array[15] - res_line.zimmeranz
                            room_list.room[3] = room_list.room[3] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[3] = rm_array[3] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                        if (res_line.kontignr < 0) and kont_doit:
                            room_list.room[16] = room_list.room[16] -\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[16] = rm_array[16] -\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                            if not kontline or not(kontline.gastnr == res_line.gastnr and kontline.ankunft == datum and kontline.zikatnr == res_line.zikatnr and kontline.betriebsnr == 1 and kontline.kontstat == 1):
                                kontline = db_session.query(Kontline).filter(
                                    (Kontline.gastnr == res_line.gastnr) &  (Kontline.ankunft == datum) &  (Kontline.zikatnr == res_line.zikatnr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

                            if kontline:
                                room_list.k_pax = room_list.k_pax +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz -\
                                        (kontline.erwachs + kontline.kind1) *\
                                        res_line.zimmeranz
                                rm_array[17] = rm_array[17] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz -\
                                    (kontline.erwachs + kontline.kind1) *\
                                    res_line.zimmeranz

                        if res_line.ankunft <= res_line.abreise or dayuse_flag:

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                                room_list.room[6] = room_list.room[6] + res_line.zimmeranz
                                room_list.lodg[3] = room_list.lodg[3] + net_lodg
                                room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                                rm_array[6] = rm_array[6] + res_line.zimmeranz
                                t_lodg[3] = t_lodg[3] + net_lodg


                                t_lodg[5] = t_lodg[5] + (net_lodg / exchg_rate)

                            if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                                room_list.room_comp = room_list.room_comp + res_line.zimmeranz
                                t_room_comp = room_list.room_comp + res_line.zimmeranz
                            else:
                                room_list.lodg[4] = room_list.lodg[4] + net_lodg
                                t_lodg[4] = t_lodg[4] + net_lodg
                                room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                                t_lodg[6] = t_lodg[6] + (net_lodg / exchg_rate)


                            room_list.room_exccomp = room_list.room[6] - room_list.room_comp
                            room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(tot_rmrev)
                            room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)

                            if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                                room_list.room[7] = room_list.room[7] +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz
                                rm_array[7] = rm_array[7] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                    if datum == res_line.abreise and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and consider_it:

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            room_list.room[4] = room_list.room[4] + res_line.zimmeranz
                            room_list.lodg[2] = room_list.lodg[2] + net_lodg
                            rm_array[4] = rm_array[4] + res_line.zimmeranz
                            t_lodg[2] = t_lodg[2] + net_lodg

                        if datum != curr_date:
                            room_list.lodg[0] = room_list.lodg[0] + net_lodg
                        room_list.room[5] = room_list.room[5] +\
                                (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz
                        rm_array[5] = rm_array[5] +\
                                (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz

                    if (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and res_line.resstatus != 4 and consider_it and (res_line.abreise > res_line.ankunft and res_line.ankunft != datum and res_line.abreise != datum):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and (res_line.resstatus != 3 or (res_line.resstatus == 3 and incl_tent)) and not res_line.zimmerfix:
                            room_list.room[6] = room_list.room[6] + res_line.zimmeranz
                            room_list.lodg[3] = room_list.lodg[3] + net_lodg
                            room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                            rm_array[6] = rm_array[6] + res_line.zimmeranz
                            t_lodg[3] = t_lodg[3] + net_lodg


                            t_lodg[5] = t_lodg[5] + (net_lodg / exchg_rate)
                            room_list.room_exccomp = room_list.room[6] - room_list.room_comp

                        if res_line.erwachs == 0 and res_line.gratis > 0 and res_line.zipreis == 0:
                            room_list.room_comp = room_list.room_comp + res_line.zimmeranz
                            t_room_comp = room_list.room_comp + res_line.zimmeranz
                        else:
                            room_list.lodg[4] = room_list.lodg[4] + net_lodg
                            t_lodg[4] = t_lodg[4] + net_lodg
                            room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                            t_lodg[6] = t_lodg[6] + (net_lodg / exchg_rate)


                        room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(tot_rmrev)
                        room_list.rmrate2 =  to_decimal(room_list.rmrate) / to_decimal(exchg_rate)

                        if datum != curr_date:
                            room_list.lodg[0] = room_list.lodg[0] + net_lodg

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3:
                            room_list.room[7] = room_list.room[7] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[7] = rm_array[7] +\
                                (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                res_line.gratis) * res_line.zimmeranz

                        if (res_line.kontignr < 0) and kont_doit:
                            room_list.room[15] = room_list.room[15] - res_line.zimmeranz
                            room_list.room[16] = room_list.room[16] -\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz
                            rm_array[15] = rm_array[15] - res_line.zimmeranz
                            rm_array[16] = rm_array[16] -\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz

                            if not kontline or not(kontline.gastnr == res_line.gastnr and kontline.ankunft == datum and kontline.zikatnr == res_line.zikatnr and kontline.betriebsnr == 1 and kontline.kontstat == 1):
                                kontline = db_session.query(Kontline).filter(
                                    (Kontline.gastnr == res_line.gastnr) &  (Kontline.ankunft == datum) &  (Kontline.zikatnr == res_line.zikatnr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

                            if kontline:
                                room_list.k_pax = room_list.k_pax +\
                                        (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                        res_line.gratis) * res_line.zimmeranz -\
                                        (kontline.erwachs + kontline.kind1) *\
                                        res_line.zimmeranz
                                rm_array[17] = rm_array[17] +\
                                    (pax + res_line.kind1 + res_line.kind2 + res_line.l_zuordnung[3] +\
                                    res_line.gratis) * res_line.zimmeranz -\
                                    (kontline.erwachs + kontline.kind1) *\
                                    res_line.zimmeranz

                    if res_line.resstatus == 3 and datum < res_line.abreise:
                        room_list.room[12] = room_list.room[12] + res_line.zimmeranz
                        rm_array[12] = rm_array[12] + res_line.zimmeranz
                        room_list.t_pax = room_list.t_pax + (res_line.erwachs * res_line.zimmeranz)
                        tent_pers = tent_pers + (res_line.erwachs * res_line.zimmeranz)

                    if res_line.kontignr > 0 and res_line.active_flag <= 1 and res_line.resstatus <= 6 and res_line.resstatus != 3 and res_line.resstatus != 4 and res_line.abreise > datum:

                        if not kline or not(kline.kontignr == res_line.kontignr and kline.kontstat == 1):
                            kline = db_session.query(Kline).filter(
                                (Kline.kontignr == res_line.kontignr) &  (Kline.kontstat == 1)).first()

                        if kline:

                            if not kontline or not(kontline.kontcode == kline.kontcode and kontline.ankunft <= datum and kontline.abreise >= datum and kontline.betriebsnr == 0 and kontline.kontstat == 1):
                                kontline = db_session.query(Kontline).filter(
                                    (Kontline.kontcode == kline.kontcode) &  (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 0) &  (Kontline.kontstat == 1)).first()

                            if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                                room_list.room[13] = room_list.room[13] - res_line.zimmeranz
                                rm_array[13] = rm_array[13] - res_line.zimmeranz


        for datum in date_range(curr_date,to_date) :

            for kontline in db_session.query(Kontline).filter(
                    (Kontline.ankunft <= datum) &  (Kontline.abreise >= datum) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == kontline.arrangement and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == kontline.arrangement) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == kontline.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == kontline.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if do_it and not all_segm:

                    if not guest or not(guest.gastnr == kontline.gastnr):
                        guest = db_session.query(Guest).filter(
                            (Guest.gastnr == kontline.gastnr)).first()

                    if not guestseg or not(guestseg.gastnr == guest.gastnr and guestseg.reihenfolge == 1):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        if not guestseg or not(guestseg.gastnr == guest.gastnr):
                            guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        if not s_list or not(s_list.segm == guestseg.segmentcode and s_list.selected):
                            s_list = db_session.query(S_list).filter(
                                (S_list.segm == guestseg.segmentcode) &  (S_list.selected)).first()
                        do_it = None != s_list

                if excl_compl and do_it:

                    if not guest or not(guest.gastnr == kontline.gastnr):
                        guest = db_session.query(Guest).filter(
                            (Guest.gastnr == kontline.gastnr)).first()

                    if not guestseg or not(guestseg.gastnr == guest.gastnr and guestseg.reihenfolge == 1):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

                    if not guestseg:

                        if not guestseg or not(guestseg.gastnr == guest.gastnr):
                            guestseg = db_session.query(Guestseg).filter(
                                (Guestseg.gastnr == guest.gastnr)).first()

                    if guestseg:

                        if not segment or not(segment.segmentcode == guestseg.segmentcode and (segment.betriebsnr == 1 or segment.betriebsnr == 2)):
                            segment = db_session.query(Segment).filter(
                                (Segment.segmentcode == guestseg.segmentcode) &  ((Segment.betriebsnr == 1) |  (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                if do_it:

                    if not room_list or not(room_list.datum == datum):
                        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)
                    room_list.room[15] = room_list.room[15] + kontline.zimmeranz
                    room_list.room[16] = room_list.room[16] +\
                            (kontline.erwachs + kontline.kind1) *\
                            kontline.zimmeranz
                    rm_array[15] = rm_array[15] + kontline.zimmeranz
                    rm_array[16] = rm_array[16] +\
                            (kontline.erwachs + kontline.kind1) *\
                            kontline.zimmeranz


        curr_time = get_current_time_in_seconds()

        for room_list in query(room_list_list):

            if room_list.room[15] > 0:
                room_list.room[6] = room_list.room[6] + room_list.room[15]
                room_list.room[7] = room_list.room[7] + room_list.room[16] + room_list.k_pax

            if incl_tent:
                room_list.room[7] = room_list.room[7] + room_list.t_pax

        if rm_array[15] > 0:
            rm_array[6] = rm_array[6] + rm_array[15]
            rm_array[7] = rm_array[7] + rm_array[16] + rm_array[17]

        if incl_tent:
            rm_array[7] = rm_array[7] + tent_pers


        datum = curr_date - timedelta(days=1)
        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)

            if not room_list or not(room_list.datum == datum):
                room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

            queasy_obj_list = []
            for queasy, zimmer in db_session.query(Queasy, Zimmer).join(Zimmer,(Zimmer.zinr == Queasy.char1) &  (Zimmer.sleeping)).filter(
                    (Queasy.key == 14) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy._recid in queasy_obj_list:
                    continue
                else:
                    queasy_obj_list.append(queasy._recid)

                if not guestseg or not(guestseg.gastnr == queasy.number3 and guestseg.reihenfolge == 1):
                    guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == queasy.number3) &  (Guestseg.reihenfolge == 1)).first()

                if not guestseg:

                    if not guestseg or not(guestseg.gastnr == queasy.number3):
                        guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == queasy.number3)).first()
                do_it = None != guestseg

                if not all_segm and do_it:

                    if not s_list or not(s_list.segm == guestseg.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == guestseg.segmentcode) &  (S_list.selected)).first()
                    do_it = None != s_list

                if do_it and not all_argt:

                    if not a_list or not(a_list.argt == queasy.char2 and a_list.selected):
                        a_list = db_session.query(A_list).filter(
                            (A_list.argt == queasy.char2) &  (A_list.selected)).first()
                    do_it = None != a_list

                if do_it and not all_zikat:

                    if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                        z_list = db_session.query(Z_list).filter(
                            (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()
                    do_it = None != z_list

                if do_it:
                    room_list.room[6] = room_list.room[6] + 1
                    room_list.room[7] = room_list.room[7] + queasy.number1
                    rm_array[6] = rm_array[6] + 1
                    rm_array[7] = rm_array[7] + queasy.number1


        cal_lastday_occ()
        p_room = 0
        p_pax = 0
        prev_room = 0
        datum = curr_date - timedelta(days=1)


        for i in range(1,(to_date - curr_date + 1)  + 1) :
            datum = datum + timedelta(days=1)
            anzahl_dayuse = 0

            if not dayuse_list or not(dayuse_list.datum == datum):
                dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == datum), first=True)

            if dayuse_list:
                anzahl_dayuse = dayuse_list.zimmeranz

            if not room_list or not(room_list.datum == datum):
                room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)
            room_list.room[8] = room_list.room[6] / tot_room * 100
            prev_room = prev_room + room_list.room[6]
            room_list.room[9] = prev_room / (tot_room * i) * 100
            room_list.rmocc_exclcomp = ( to_decimal(room_list.room[6]) - to_decimal(room_list.room_comp)) / to_decimal(tot_room) * to_decimal("100")

            if (room_list.room[6] - anzahl_dayuse) < tot_room:
                room_list.room[10] = tot_room - room_list.room[6] + anzahl_dayuse
                rm_array[10] = rm_array[10] + tot_room - room_list.room[6] + anzahl_dayuse
            else:
                room_list.room[11] = room_list.room[6] - tot_room - anzahl_dayuse
                rm_array[11] = rm_array[11] + room_list.room[6] - tot_room - anzahl_dayuse

            if i > 1:
                room_list.room[0] = p_room
                room_list.room[1] = p_pax
                rm_array[0] = rm_array[0] + p_room
                rm_array[1] = rm_array[1] + p_pax


            p_room = room_list.room[6]
            p_lodg =  to_decimal(room_list.lodg[3])
            p_pax = room_list.room[7]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):

            if room_list.datum < ci_date:

                if not zinrstat or not(zinrstat.zinr.lower()  == ("ooo").lower()  and zinr.datum == room_list.datum):
                    zinrstat = db_session.query(Zinrstat).filter(
                        (func.lower(Zinrstat.zinr) == ("ooo").lower()) &  (Zinrstat.datum == room_list.datum)).first()

                if zinrstat:
                    room_list.room[14] = zinrstat.zimmeranz
                    rm_array[14] = rm_array[14] + zinrstat.zimmeranz


            else:

                outorder_obj_list = []
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) &  (Zimmer.sleeping)).filter(
                        (Outorder.gespstart <= room_list.datum) &  (Outorder.gespende >= room_list.datum) &  (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder._recid in outorder_obj_list:
                        continue
                    else:
                        outorder_obj_list.append(outorder._recid)

                    if not all_zikat:

                        if not z_list or not(z_list.zikatnr == zimmer.zikatnr and z_list.selected):
                            z_list = db_session.query(Z_list).filter(
                                (Z_list.zikatnr == zimmer.zikatnr) &  (Z_list.selected)).first()

                        if z_list:
                            room_list.room[14] = room_list.room[14] + 1
                            rm_array[14] = rm_array[14] + 1


                    else:
                        room_list.room[14] = room_list.room[14] + 1
                        rm_array[14] = rm_array[14] + 1

                if exclooo:
                    room_list.room[10] = room_list.room[10] - room_list.room[14]
                    rm_array[10] = rm_array[10] - room_list.room[14]

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):
            for i in range(1,8 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
            for i in range(9,10 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>9.99")
            for i in range(11,15 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>>")
            for i in range(16,17 + 1) :
                room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
        jml_date = to_date - curr_date + 1
        do_it = True

        if show_rev == 1 or show_rev == 2:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.SELECTED)):
                counter = counter + 1

                if not segment or not(segment.segmentcode == s_list.segm):
                    segment = db_session.query(Segment).filter(
                        (Segment.segmentcode == s_list.segm)).first()

                if segment:

                    if tmin == 0 and counter == 1:

                        if segment.betriebsnr == 0:
                            tmin = 0


                        else:
                            tmin = segment.betriebsnr

                    if segment.betriebsnr > tmax:
                        tmax = segment.betriebsnr

                    if segment.betriebsnr < tmin:
                        tmin = segment.betriebsnr

            if tmax <= 2 and tmin >= 1:
                do_it = False


            else:
                do_it = True

        if do_it:

            if incl_oth:

                for room_list in query(room_list_list):
                    othrev = calc_othrev(room_list.datum)

                    if room_list.datum < ci_date:

                        if not htparam or not(htparam.paramnr == 144):
                            htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 144)).first()

                        if not waehrung or not(waehrung.wabkurz == htparam.fchar):
                            waehrung = db_session.query(Waehrung).filter(
                                (Waehrung.wabkurz == htparam.fchar)).first()

                        if waehrung:

                            if not exrate or not(exrate.datum == room_list.datum and exrate.artnr == waehrung.waehrungsnr):
                                exrate = db_session.query(Exrate).filter(
                                    (Exrate.datum == room_list.datum) &  (Exrate.artnr == waehrung.waehrungsnr)).first()

                            if exrate:
                                exchg_rate =  to_decimal(exrate.betrag)
                    else:

                        if not htparam or not(htparam.paramnr == 144):
                            htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 144)).first()

                        if not waehrung or not(waehrung.wabkurz == htparam.fchar):
                            waehrung = db_session.query(Waehrung).filter(
                                (Waehrung.wabkurz == htparam.fchar)).first()

                        if waehrung:
                            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                        else:
                            exchg_rate =  to_decimal("1")
                    room_list.lodg[4] = room_list.lodg[4] + othrev
                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate

                    if room_list.wd != 0:
                        t_lodg[4] = t_lodg[4] + othrev


                    t_lodg[6] = t_lodg[6] + (othrev / exchg_rate)

        for room_list in query(room_list_list):
            tot_avrg =  to_decimal(tot_avrg) + to_decimal(room_list.room[8])

            if (room_list.room[6] - room_list.room[15]) != 0:
                room_list.avrglodg =  to_decimal(room_list.lodg[3]) / to_decimal((room_list.room[6] - room_list.room[15]))
            room_list.avrglodg2 =  to_decimal(room_list.avrglodg) / to_decimal(exchg_rate)

            if (room_list.room_exccomp - room_list.room[15]) != 0:
                room_list.avrgrmrev =  to_decimal(room_list.lodg[4]) / to_decimal((room_list.room[6] - room_list.room[15]))
                room_list.avrgrmrev2 =  to_decimal(room_list.avrgrmrev) / to_decimal(exchg_rate)

            if room_list.wd != 0:
                troom_exccomp = troom_exccomp + (room_list.room[6] - room_list.room[15])

            if ((to_decimal(room_list.coom[8]) * room_list.avrgrmrev) / 100) != 0:
                room_list.revpar = ( to_decimal(to_decimal(room_list.coom[8])) * to_decimal(room_list.avrgrmrev)) / to_decimal("100")
                room_list.revpar2 =  to_decimal(room_list.revpar) / to_decimal(exchg_rate)


            room_list.avrglodg_inclcomp =  to_decimal(room_list.lodg[4]) / to_decimal(room_list.room[6])
            room_list.avrglodg_exclcomp =  to_decimal(room_list.lodg[4]) / to_decimal((room_list.room[6]) - to_decimal(room_list.room_comp))

        if troom_exccomp != 0:
            tavg_rmrev =  to_decimal(t_lodg[4]) / to_decimal(troom_exccomp)
        tavg_rmrev2 =  to_decimal(tavg_rmrev) / to_decimal(exchg_rate)
        avrg_rate =  to_decimal(tot_avrg) / to_decimal(jml_date)
        t_avrglodg_inclcomp =  to_decimal(t_lodg[4]) / to_decimal(rm_array[6])
        t_avrglodg_exclcomp =  to_decimal(t_lodg[4]) / to_decimal((rm_array[6]) - to_decimal(t_room_comp))
        mtd_occ =  to_decimal(rm_array[6]) / to_decimal((tot_room) * to_decimal((to_date) - to_decimal(curr_date) + to_decimal(1))) * to_decimal("100")
        t_rmocc_exclcomp = ( to_decimal(rm_array[6]) - to_decimal(t_room_comp)) / to_decimal((tot_room) * to_decimal((to_date) - to_decimal(curr_date) + to_decimal(1))) * to_decimal("100")

        if not room_list or not(room_list.wd == 0):
            room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)
        for i in range(1,8 + 1) :
            room_list.room[i - 1] = rm_array[i - 1]
        for i in range(11,17 + 1) :
            room_list.room[i - 1] = rm_array[i - 1]
        for i in range(1,8 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
        for i in range(11,12 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>>")
        room_list.room[8] = mtd_occ
        room_list.coom[8] = to_string(mtd_occ, " >>9.99")
        room_list.coom[9] = to_string(avrg_rate, "->>9.99")
        room_list.coom[12] = to_string(rm_array[12], "->>>>>>")
        room_list.coom[13] = to_string(rm_array[13], "->>>>>>")
        room_list.coom[14] = to_string(rm_array[14], "->>>>>>")
        room_list.lodg[1] = t_lodg[1]
        room_list.lodg[2] = t_lodg[2]
        room_list.lodg[3] = t_lodg[3]
        room_list.lodg[4] = t_lodg[4]
        room_list.lodg[5] = t_lodg[5]
        room_list.lodg[6] = t_lodg[6]
        room_list.rmocc_exclcomp =  to_decimal(t_rmocc_exclcomp)


        room_list.avrglodg_inclcomp =  to_decimal(t_avrglodg_inclcomp)
        room_list.avrglodg_exclcomp =  to_decimal(t_avrglodg_exclcomp)
        for i in range(16,17 + 1) :
            room_list.coom[i - 1] = to_string(room_list.room[i - 1], "->>>>>9")
        mtd_occ =  to_decimal("0")
        avrg_lodging =  to_decimal("0")

        for room_list in query(room_list_list, filters=(lambda room_list: room_list.wd != 0)):
            avrg_lodging =  to_decimal(avrg_lodging) + to_decimal(room_list.avrglodg)
            mtd_occ =  to_decimal(mtd_occ) + to_decimal(room_list.room[8])
            sum_breakfast =  to_decimal(sum_breakfast) + to_decimal(room_list.other[0])
            sum_lunch =  to_decimal(sum_lunch) + to_decimal(room_list.other[1])
            sum_dinner =  to_decimal(sum_dinner) + to_decimal(room_list.other[2])
            sum_other =  to_decimal(sum_other) + to_decimal(room_list.other[3])


            sum_breakfast_usd =  to_decimal(sum_breakfast_usd) + to_decimal(room_list.other[4])
            sum_lunch_usd =  to_decimal(sum_lunch_usd) + to_decimal(room_list.other[5])
            sum_dinner_usd =  to_decimal(sum_dinner_usd) + to_decimal(room_list.other[6])
            sum_other_usd =  to_decimal(sum_other_usd) + to_decimal(room_list.other[7])
            sum_comp =  to_decimal(sum_comp) + to_decimal(room_list.room_comp)
            t_revpar =  to_decimal(t_revpar) + to_decimal(room_list.revpar)
            t_revpar2 =  to_decimal(t_revpar2) + to_decimal(room_list.revpar2)
            t_rmrate =  to_decimal(t_rmrate) + to_decimal(room_list.rmrate)
            t_rmrate2 =  to_decimal(t_rmrate2) + to_decimal(room_list.rmrate2)

        if not room_list or not(room_list.wd == 0):
            room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)

        if tavg_rmrev == None:
            tavg_rmrev =  to_decimal("0")

        if tavg_rmrev2 == None:
            tavg_rmrev2 =  to_decimal("0")
        room_list.avrglodg =  to_decimal(avrg_lodging) / to_decimal((to_date) - to_decimal(curr_date) + to_decimal("1") )
        room_list.avrgrmrev =  to_decimal(tavg_rmrev)
        room_list.avrgrmrev2 =  to_decimal(tavg_rmrev2)
        room_list.other[0] = sum_breakfast
        room_list.other[1] = sum_lunch
        room_list.other[2] = sum_dinner
        room_list.other[3] = sum_other
        room_list.other[4] = sum_breakfast_usd
        room_list.other[5] = sum_lunch_usd
        room_list.other[6] = sum_dinner_usd
        room_list.other[7] = sum_other_usd
        room_list.room_comp = sum_comp
        room_list.rmrate =  to_decimal(t_rmrate)
        room_list.rmrate2 =  to_decimal(t_rmrate2)
        room_list.fixleist =  to_decimal(tot_fixcost)
        room_list.fixleist2 =  to_decimal(tot_fixcost2)

        if ((to_decimal(room_list.coom[8]) * room_list.avrgrmrev) / 100) != 0:
            room_list.revpar = ( to_decimal(to_decimal(room_list.coom[8])) * to_decimal(room_list.avrgrmrev)) / to_decimal("100")
            room_list.revpar2 =  to_decimal(room_list.revpar) / to_decimal(exchg_rate)

        if room_list.room[6] != 0:
            room_list.avrglodg =  to_decimal(room_list.lodg[3]) / to_decimal(room_list.room[6])
        room_list.avrglodg2 =  to_decimal(room_list.avrglodg) / to_decimal(exchg_rate)


    def cal_lastday_occ():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        do_it:bool = False
        S_list = Segm_list
        s_list_list = segm_list_list

        if not room_list or not(room_list.datum == curr_date):
            room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == curr_date), first=True)

        if curr_date <= ci_date:

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum == curr_date - timedelta(days=1)) &  (Genstat.res_logic[inc_value(1)]) &  (Genstat.zinr != "") &  (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                do_it = True

                if do_it and not all_segm:

                    if not s_list or not(s_list.segm == genstat.segmentcode and s_list.selected):
                        s_list = db_session.query(S_list).filter(
                            (S_list.segm == genstat.segmentcode) &  (S_list.selected)).first()
                    do_it = None != s_list

                if do_it and not all_argt:

                    if not argt_list or not(argt_list.argt == genstat.argt and argt_list.selected):
                        argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                    do_it = None != argt_list

                if do_it and not all_zikat:

                    if not zikat_list or not(zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected):
                        zikat_list = query(zikat_list_list, filters=(lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
                    do_it = None != zikat_list

                if do_it:
                    room_list.room[0] = room_list.room[0] + 1
                    rm_array[0] = rm_array[0] + 1
                    room_list.room[1] = room_list.room[1] + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.kind3 + genstat.gratis
                    rm_array[1] = rm_array[1] + genstat.erwachs + genstat.kind1 +\
                            genstat.kind2 + genstat.kind3 + genstat.gratis


        else:
            room_list.room[0] = room_list.room[6] - room_list.room[2] +\
                    room_list.room[4]
            rm_array[0] = rm_array[0] + room_list.room[0]
            room_list.room[1] = room_list.room[7] - room_list.room[3] +\
                    room_list.room[5]
            rm_array[1] = rm_array[1] + room_list.room[1]


        room_list.lodg[0] = room_list.lodg[3] - room_list.lodg[1] + room_list.lodg[2]


    def rsv_closeout(datum:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        rsvstat = ""
        curr_anz:int = 0
        curr_date:date = None
        start_date:date = None

        def generate_inner_output():
            return (rsvstat)


        if not queasy or not(queasy.key == 37 and queasy.number1 == get_year(datum)):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 37) &  (Queasy.number1 == get_year(datum))).first()

        if not queasy:

            return generate_inner_output()
        start_date = date_mdy(1, 1, get_year(datum))
        curr_anz = 0


        for curr_date in date_range(start_date,datum) :
            curr_anz = curr_anz + 1
        rsvstat = " " + substring(queasy.char3, curr_anz - 1, 1)

        return generate_inner_output()


    def check_bonus():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        j = 1
        for i in range(1,4 + 1) :
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4


    def create_active_room_list():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        end_date:date = None
        actual_date:date = None
        Z_list = Zikat_list
        z_list_list = zikat_list_list

        if to_date < ci_date:
            end_date = to_date
        else:
            end_date = ci_date - timedelta(days=1)

        if all_zikat:

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum >= curr_date) &  (Zkstat.datum <= end_date)).order_by(Zkstat.datum).all():

                if actual_date != zkstat.datum:
                    active_rm_list = Active_rm_list()
                    active_rm_list_list.append(active_rm_list)

                    active_rm_list.datum = zkstat.datum
                    actual_date = zkstat.datum


                active_rm_list.zimmeranz = active_rm_list.zimmeranz + zkstat.anz100

        else:

            for zkstat in db_session.query(Zkstat).filter(
                    (Zkstat.datum >= curr_date) &  (Zkstat.datum <= end_date)).order_by(Zkstat.datum).all():

                if not z_list or not(z_list.zikatnr == zkstat.zikatnr and z_list.selected):
                    z_list = db_session.query(Z_list).filter(
                        (Z_list.zikatnr == zkstat.zikatnr) &  (Z_list.selected)).first()

                if z_list:

                    if actual_date != zkstat.datum:
                        active_rm_list = Active_rm_list()
                        active_rm_list_list.append(active_rm_list)

                        active_rm_list.datum = zkstat.datum
                        actual_date = zkstat.datum


                    active_rm_list.zimmeranz = active_rm_list.zimmeranz + zkstat.anz100

    def get_active_room(curr_datum:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        active_room = 0

        def generate_inner_output():
            return (active_room)


        if curr_datum >= ci_date:
            active_room = actual_tot_room

            return generate_inner_output()

        if not active_rm_list or not(active_rm_list.datum == curr_datum):
            active_rm_list = query(active_rm_list_list, filters=(lambda active_rm_list: active_rm_list.datum == curr_datum), first=True)

        if active_rm_list:
            active_room = active_rm_list.zimmeranz

        return generate_inner_output()


    def get_mtd_active_room():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        mtd_room = 0
        datum:date = None
        anz:int = 0

        def generate_inner_output():
            return (mtd_room)

        for datum in date_range(curr_date,to_date) :
            anz = get_active_room(datum)
            mtd_room = mtd_room + anz

        return generate_inner_output()


    def calc_othrev(datum:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        othrev = to_decimal("0.0")
        i:int = 0
        max_i:int = 0
        art_list:List[int] = create_empty_list(200,0)
        serv_vat:bool = False
        fact:decimal = to_decimal("0.0")
        serv:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")

        def generate_inner_output():
            return (othrev)


        if not htparam or not(htparam.paramnr == 479):
            htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artart == 0) &  (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        for i in range(1,max_i + 1) :

            if not artikel or not(artikel.artnr == art_list[i - 1] and artikel.departement == 0):
                artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == art_list[i - 1]) &  (Artikel.departement == 0)).first()

            if artikel:
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                for umsatz in db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    othrev = othrev + umsatz.betrag / fact

        return generate_inner_output()


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, res_line, htparam, waehrung, kontline, zimmer, guest, zimkateg, segment, genstat, exrate, fixleist, artikel, reservation, arrangement, bill_line, queasy, reslin_queasy, guestseg, zinrstat, outorder, zkstat, umsatz
        nonlocal pvilanguage, op_type, flag_i, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list
        nonlocal room_list_list, segm_list_list, argt_list_list, zikat_list_list, outlook_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = lfakt - res_line.ankunft

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()

    if not htparam or not(htparam.paramnr == 87):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if not htparam or not(htparam.paramnr == 550):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    if not htparam or not(htparam.paramnr == 144):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if not waehrung or not(waehrung.wabkurz == htparam.fchar):
        waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    if not htparam or not(htparam.paramnr == 127):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 127)).first()
    rm_vat = htparam.flogical

    if not htparam or not(htparam.paramnr == 128):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 128)).first()
    rm_serv = htparam.flogical

    if not htparam or not(htparam.paramnr == 491):
        htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    if op_type == 0:

        if curr_date < ci_date:
            create_browse()
        else:
            create_browse1()
        segm_code_name()
        room_code_name()
        argt_code_name()

    return generate_output()