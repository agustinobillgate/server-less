#using conversion tools version: 1.0.0.88

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servvat import calc_servvat
from sqlalchemy import func
# from functions.get_room_breakdown import get_room_breakdown
from models import Res_line, Kontline, Zimmer, Guest, Zimkateg, Waehrung, Segment, Genstat, Fixleist, Bill_line, Queasy, Reslin_queasy, Argt_line, Outorder, Zkstat, Artikel, Umsatz, Htparam, Arrangement, Exrate, Reservation, Guestseg, Zinrstat
from models import Kontplan, Katpreis, Ratecode, Pricecod, Guest_pr

segm_list_list, Segm_list = create_model("Segm_list", {"selected":bool, "segm":int, "bezeich":str})
argt_list_list, Argt_list = create_model("Argt_list", {"selected":bool, "argtnr":int, "argt":str, "bezeich":str})
zikat_list_list, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "bezeich":str})
outlook_list_list, Outlook_list = create_model("Outlook_list", {"selected":bool, "outlook_nr":int, "bezeich":str})

def cr_occfcast1_2_webbl_test(segm_list_list:[Segm_list], argt_list_list:[Argt_list], zikat_list_list:[Zikat_list], outlook_list_list:[Outlook_list], pvilanguage:int, op_type:int, flag_i:int, curr_date:date, to_date:date, all_segm:bool, all_argt:bool, all_zikat:bool, exclooo:bool, incl_tent:bool, show_rev:int, vhp_limited:bool, excl_compl:bool, all_outlook:bool, incl_oth:bool):

    prepare_cache ([Res_line, Htparam, Waehrung, Kontline, Zimmer, Guest, Segment, Genstat, Exrate, Fixleist, Artikel, Reservation, Arrangement, Queasy, Reslin_queasy, Argt_line, Guestseg, Zinrstat, Zkstat, Umsatz])

    room_list_list = []
    lvcarea:str = "occ-fcast1"
    tot_rmrev:Decimal = to_decimal("0.0")
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
    t_lodg:List[Decimal] = create_empty_list(7,to_decimal("0"))
    jml_date:int = 0
    tot_avrg:Decimal = to_decimal("0.0")
    t_rmrate:Decimal = to_decimal("0.0")
    t_rmrate2:Decimal = to_decimal("0.0")
    t_revpar:Decimal = to_decimal("0.0")
    t_revpar2:Decimal = to_decimal("0.0")
    price:int = 0
    price_decimal:int = 0
    new_contrate:bool = False
    rm_vat:bool = False
    rm_serv:bool = False
    rm_array:List[int] = create_empty_list(18,0)
    exchg_rate:Decimal = to_decimal("0.0")
    sum_comp:Decimal = to_decimal("0.0")
    post_it:bool = False
    fcost:Decimal = to_decimal("0.0")
    curr_time:int = 0
    tmpint:int = 0
    res_line = kontline = zimmer = guest = zimkateg = waehrung = segment = genstat = fixleist = bill_line = queasy = reslin_queasy = argt_line = outorder = zkstat = artikel = umsatz = htparam = arrangement = exrate = reservation = guestseg = zinrstat = None

    room_list = segm_list = argt_list = zikat_list = outlook_list = print_list = print_list2 = print_list3 = rline1 = active_rm_list = dayuse_list = s_list = a_list = z_list = o_list = bsegm = bargt = broom = s_list = a_list = z_list = o_list = s_list = z_list = None

    room_list_list, Room_list = create_model("Room_list", {"wd":int, "datum":date, "bezeich":str, "room":[Decimal,17], "coom":[str,17], "k_pax":int, "t_pax":int, "lodg":[Decimal,7], "avrglodg":Decimal, "avrglodg2":Decimal, "avrgrmrev":Decimal, "avrgrmrev2":Decimal, "others":[Decimal,8], "ly_fcast":str, "ly_actual":str, "ly_avlodge":str, "room_exccomp":int, "room_comp":int, "fixleist":Decimal, "fixleist2":Decimal, "rmrate":Decimal, "rmrate2":Decimal, "revpar":Decimal, "revpar2":Decimal, "avrglodg_inclcomp":Decimal, "avrglodg_exclcomp":Decimal, "rmocc_exclcomp":Decimal})
    print_list_list, Print_list = create_model("Print_list", {"code_name":str})
    print_list2_list, Print_list2 = create_model("Print_list2", {"argm":str})
    print_list3_list, Print_list3 = create_model("Print_list3", {"room":str})
    active_rm_list_list, Active_rm_list = create_model("Active_rm_list", {"datum":date, "zimmeranz":int})
    dayuse_list_list, Dayuse_list = create_model("Dayuse_list", {"datum":date, "zimmeranz":int, "pax":int})
    db_session = local_storage.db_session

    Rline1 = create_buffer("Rline1",Res_line)

    kontline_query = text(f"""
            CREATE TEMP TABLE kontline AS  
            SELECT * FROM kontline  
                WHERE ankunft >= :start_date AND abreise <= :to_date
                and kontstatus=1;
                """)
    db_session.execute(kontline_query, {"start_date": curr_date, "to_date": to_date})

    kontplan_query = text("""
            CREATE TEMPORARY TABLE  kontplan AS
                SELECT *
                FROM kontplan
                WHERE datum BETWEEN :start_date AND :to_date;
        """)
    db_session.execute(kontplan_query, {"start_date": curr_date, "to_date": to_date})

    zinrstat_query = text("""
            CREATE TEMPORARY TABLE  zinrstat AS
                SELECT *
                FROM zinrstat
                WHERE datum BETWEEN :start_date AND :to_date;
        """)
    db_session.execute(zinrstat_query, {"start_date": curr_date, "to_date": to_date})



    resline_query = text("""
        CREATE TEMPORARY TABLE res_line AS
        SELECT 
            *
        FROM res_line
        WHERE resstatus <= 13
                AND resstatus NOT IN (4, 8, 9, 10, 12)
                AND active_flag <= 1
          ;
                   
        """)
    db_session.execute(resline_query, {"start_date": curr_date, "to_date": to_date})
    
    
    param87 = db_session.execute(text("SELECT * FROM htparam WHERE paramnr=87")).mappings().fetchone()
    if param87:
        ci_date = param87["fdate"]

    genstat_query = text("""
            CREATE TEMPORARY TABLE genstat AS
                SELECT 
                    *
                FROM genstat g
                WHERE EXISTS (
                        SELECT 1 FROM res_line rl WHERE rl.resnr = g.resnr
                    );
        """)
    db_session.execute(genstat_query, {"ci_date": ci_date, "to_date": to_date})

    fixleist_query = text(""" 
        CREATE TEMP TABLE fixleist AS 
                SELECT a.* 
                FROM fixleist AS a 
                WHERE EXISTS (
                    SELECT 1 FROM res_line rl WHERE rl.resnr = a.resnr
                ); 
        """)
    db_session.execute(fixleist_query, {})

    guest_query = text("""
            CREATE TEMPORARY TABLE guest AS
                SELECT 
                    *
                FROM guest g
                WHERE EXISTS (
                    SELECT 1 FROM genstat a WHERE a.gastnr = g.gastnr
                );
        """)
    db_session.execute(guest_query, {})

    reslinq_query = text("""
        CREATE TEMP TABLE reslin_queasy AS  
        SELECT * 
        FROM reslin_queasy a  
        WHERE 
             EXISTS (
                SELECT 1 FROM res_line rl WHERE rl.resnr = a.resnr
            );
        """)
    db_session.execute(reslinq_query, {})

    arr_query = text(""" 
        CREATE TEMP TABLE arrangement AS 
        SELECT a.* 
        FROM arrangement AS a 
        WHERE EXISTS (
            SELECT 1 FROM res_line rl 
            WHERE rl.arrangement = a.arrangement 
                     );
        """)
    db_session.execute(arr_query, {})


    set_cache(Segment,[],[["segmentcode"]], True)
    set_cache(Zimmer,[],[["zinr"]], True)
    set_cache(Htparam,[],[["paramnr"]], True)
    set_cache(Arrangement,[],[["arrangement"]], True)

    

    def generate_output():
        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        return {"room-list": room_list_list}

    def create_browse():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:Decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        dayuse_flag:bool = False
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:Decimal = to_decimal("0.0")
        rmsharer:bool = False
        othrev:Decimal = to_decimal("0.0")
        tavg_rmrev:Decimal = to_decimal("0.0")
        tavg_rmrev2:Decimal = to_decimal("0.0")
        troom_exccomp:int = 0
        rsvstat:str = ""
        avrg_lodging:Decimal = to_decimal("0.0")
        avrg_rmrate:Decimal = to_decimal("0.0")
        avrg_lodging2:Decimal = to_decimal("0.0")
        avrg_rmrate2:Decimal = to_decimal("0.0")
        anzahl_dayuse:int = 0
        kline = None
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_fixcost:Decimal = to_decimal("0.0")
        tot_fixcost2:Decimal = to_decimal("0.0")
        sum_breakfast:Decimal = to_decimal("0.0")
        sum_lunch:Decimal = to_decimal("0.0")
        sum_dinner:Decimal = to_decimal("0.0")
        sum_other:Decimal = to_decimal("0.0")
        sum_breakfast_usd:Decimal = to_decimal("0.0")
        sum_lunch_usd:Decimal = to_decimal("0.0")
        sum_dinner_usd:Decimal = to_decimal("0.0")
        sum_other_usd:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        rmrate:Decimal = to_decimal("0.0")
        room_exccomp:int = 0
        bfast_art:int = 0
        curr_zinr:str = ""
        pax:int = 0
        curr_date1:date = None
        t_avrglodg_inclcomp:Decimal = to_decimal("0.0")
        t_avrglodg_exclcomp:Decimal = to_decimal("0.0")
        t_rmocc_exclcomp:Decimal = to_decimal("0.0")
        t_room_comp:int = 0
        tmp_date:date = None
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

        htparam = get_cache (Htparam, {"paramnr": 125}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
        bfast_art = htparam.finteger
        room_exccomp = 0
        for i in range(1,18 + 1) :
            rm_array[i - 1] = 0
        for i in range(1,4 + 1) :
            t_lodg[i - 1] = 0
        tent_pers = 0
        room_list_list.clear()
        actual_tot_room = 0

        zimmer = Zimmer()
        for zimmer.zikatnr, zimmer.typ, zimmer._recid in db_session.query(Zimmer.zikatnr, Zimmer.typ, Zimmer._recid).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                actual_tot_room = actual_tot_room + 1
            else:

                z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

                if z_list:
                    actual_tot_room = actual_tot_room + 1
        create_active_room_list()
        datum = curr_date - timedelta(days=1)
        for i in range(1,tmpint + 1) :
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

            kontline = Kontline()
            for kontline.zikatnr, kontline.zimmeranz, kontline.arrangement, kontline.gastnr, kontline.erwachs, kontline.kind1, kontline._recid in db_session.query(Kontline.zikatnr, Kontline.zimmeranz, Kontline.arrangement, Kontline.gastnr, Kontline.erwachs, Kontline.kind1, Kontline._recid).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                allot_doit = True

                if kontline.zikatnr != 0 and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == kontline.zikatnr and z_list.selected), first=True)
                    allot_doit = None != z_list

                if allot_doit and (datum >= (ci_date + timedelta(days=kontline.ruecktage))):
                    room_list.room[13] = room_list.room[13] + kontline.zimmeranz
                    rm_array[13] = rm_array[13] + kontline.zimmeranz
        datum1 = curr_date

        if to_date < (ci_date - timedelta(days=1)):
            d2 = to_date
        else:
            d2 = ci_date - timedelta(days=1)

        genstat_obj_list = {}
        for genstat, guest, zimkateg, waehrung, segment in db_session.query(Genstat, Guest, Zimkateg, Waehrung, Segment).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Genstat.zikatnr)).join(Waehrung,(Waehrung.waehrungsnr == Genstat.wahrungsnr)).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                 (Genstat.res_date[inc_value(1)] >= datum1) & (Genstat.res_date[inc_value(1)] <= d2) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != " ")).order_by(Genstat.res_date[inc_value(1)], Genstat.zinr, Genstat.datum).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if curr_zinr != genstat.zinr:
                do_it = True

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                if do_it:
                    pax = genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis

                    room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == genstat.res_date[1]), first=True)

                    if room_list:
                        room_list.room[4] = room_list.room[4] + 1
                        room_list.room[5] = room_list.room[5] + pax
                        rm_array[4] = rm_array[4] + 1
                        rm_array[5] = rm_array[5] + pax


            curr_zinr = genstat.zinr

        genstat = Genstat()
        for genstat.zinr, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.res_date, genstat.datum, genstat.resstatus, genstat.res_logic, genstat.logis, genstat.ratelocal, genstat.res_deci, genstat.resnr, genstat.res_int, genstat._recid in db_session.query(Genstat.zinr, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.res_date, Genstat.datum, Genstat.resstatus, Genstat.res_logic, Genstat.logis, Genstat.ratelocal, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat._recid).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= d2) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != "")).order_by(Genstat._recid).all():

            if not vhp_limited:
                do_it = True

            if genstat.res_date[0] < genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                do_it = False

            if do_it:

                segment = get_cache (Segment, {"segmentcode": genstat.segmentcode}, ['vip_level', 'betriebsnr', '_recid'])
                do_it = None != segment and segment.vip_level == 0
            rmsharer = (genstat.resstatus == 13)

            if do_it and not all_segm:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                do_it = None != s_list

            if do_it and not all_argt:

                a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == genstat.argt and a_list.selected), first=True)
                do_it = None != a_list

            if do_it and not all_zikat:

                z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == genstat.zikatnr and z_list.selected), first=True)
                do_it = None != z_list

            if excl_compl and do_it:

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == genstat.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                if segment:
                    do_it = False


                else:

                    if genstat.zipreis == 0 and genstat.gratis != 0 and genstat.resstatus == 6 and genstat.res_logic[1] :
                        do_it = False

            if do_it and not all_outlook:

                zimmer = get_cache (Zimmer, {"zinr": genstat.zinr}, ['zikatnr', 'typ', '_recid'])

                if zimmer:

                    o_list = query(o_list_list, filters=(lambda o_list: o_list.selected  and o_list.outlook_nr == zimmer.typ), first=True)
                    do_it = None != o_list

            htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

            waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

            if waehrung:

                exrate = get_cache (Exrate, {"datum": genstat.datum, "artnr": waehrung.waehrungsnr}, ['betrag', '_recid'])

                if exrate:
                    exchg_rate =  to_decimal(exrate.betrag)

            if do_it:

                room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == genstat.datum), first=True)

                if room_list:

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
                        room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(genstat.ratelocal)

                    elif show_rev == 2:
                        room_list.lodg[3] = room_list.lodg[3] + genstat.logis
                        t_lodg[3] = t_lodg[3] + genstat.logis
                        room_list.lodg[4] = room_list.lodg[4] + genstat.logis
                        t_lodg[4] = t_lodg[4] + genstat.logis
                        room_list.lodg[5] = room_list.lodg[3] / exchg_rate
                        t_lodg[5] = t_lodg[5] + (genstat.logis / exchg_rate)
                        room_list.lodg[6] = room_list.lodg[4] / exchg_rate
                        t_lodg[6] = t_lodg[6] + (genstat.logis / exchg_rate)
                        room_list.rmrate =  to_decimal(room_list.rmrate) + to_decimal(genstat.ratelocal)
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


                    room_list.others[0] = room_list.others[0] + genstat.res_deci[1]
                    room_list.others[1] = room_list.others[1] + genstat.res_deci[2]
                    room_list.others[2] = room_list.others[2] + genstat.res_deci[3]
                    room_list.others[3] = room_list.others[3] + genstat.res_deci[4] + genstat.res_deci[5]
                    room_list.others[4] = room_list.others[0] / exchg_rate
                    room_list.others[5] = room_list.others[1] / exchg_rate
                    room_list.others[6] = room_list.others[2] / exchg_rate
                    room_list.others[7] = room_list.others[3] / exchg_rate

                    if genstat.res_date[0] == genstat.res_date[1] and not rmsharer and genstat.res_logic[1] :

                        dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == genstat.datum), first=True)

                        if not dayuse_list:
                            dayuse_list = Dayuse_list()
                            dayuse_list_list.append(dayuse_list)

                            dayuse_list.datum = genstat.datum


                        dayuse_list.zimmeranz = dayuse_list.zimmeranz + 1

                    fixleist = Fixleist()
                    for fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt, fixleist.betrag, fixleist.number, fixleist._recid in db_session.query(Fixleist.artnr, Fixleist.departement, Fixleist.sequenz, Fixleist.dekade, Fixleist.lfakt, Fixleist.betrag, Fixleist.number, Fixleist._recid).filter(
                             (Fixleist.resnr == genstat.resnr) & (Fixleist.reslinnr == genstat.res_int[0])).order_by(Fixleist._recid).all():

                        res_line = get_cache (Res_line, {"resnr": genstat.resnr, "reslinnr": genstat.res_int[0]}, ['resnr', 'ankunft', 'abreise', 'arrangement', 'reslinnr', 'zikatnr', 'zinr', 'gastnr', 'gratis', 'erwachs', 'kind1', 'zipreis', '_recid', 'kind2', 'resstatus', 'zimmerfix', 'zimmeranz', 'kontignr'])
                        post_it = check_fixleist_posted(genstat.datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                        service =  to_decimal("0")
                        vat =  to_decimal("0")
                        fcost =  to_decimal("0")

                        if post_it:

                            artikel = get_cache (Artikel, {"artnr": fixleist.artnr, "departement": fixleist.departement}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

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

        htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

        waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")
        d2 = d2 + timedelta(days=1)

        if to_date >= ci_date:

            res_line = Res_line()
            for res_line.resnr, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.reslinnr, res_line.zikatnr, res_line.zinr, res_line.gastnr, res_line.gratis, res_line.erwachs, res_line.kind1, res_line.zipreis, res_line._recid, res_line.kind2, res_line.resstatus, res_line.zimmerfix, res_line.zimmeranz, res_line.kontignr in db_session.query(Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.reslinnr, Res_line.zikatnr, Res_line.zinr, Res_line.gastnr, Res_line.gratis, Res_line.erwachs, Res_line.kind1, Res_line.zipreis, Res_line._recid, Res_line.kind2, Res_line.resstatus, Res_line.zimmerfix, Res_line.zimmeranz, Res_line.kontignr).filter(
                     (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= to_date) & (Res_line.abreise >= d2))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():

                reservation = get_cache (Reservation, {"resnr": res_line.resnr}, ['segmentcode', '_recid'])
                curr_i = 0
                dayuse_flag = False

                if not vhp_limited:
                    do_it = True
                else:

                    segment = get_cache (Segment, {"segmentcode": reservation.segmentcode}, ['vip_level', 'betriebsnr', '_recid'])
                    do_it = None != segment and segment.vip_level == 0

                if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:
                    dayuse_flag = True

                    arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argt_artikelnr', 'argtnr', 'options', '_recid'])

                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == ci_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
                    do_it = None != bill_line

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                zimmer = get_cache (Zimmer, {"zinr": res_line.zinr}, ['zikatnr', 'typ', '_recid'])

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
                kont_doit = True

                if do_it and (not all_segm) and (res_line.kontignr < 0):

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                    kont_doit = None != s_list

                if excl_compl and do_it:

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                    if segment:
                        do_it = False


                    else:

                        if res_line.zipreis == 0 and res_line.gratis != 0:
                            do_it = False

                if do_it and not all_outlook:

                    zimmer = get_cache (Zimmer, {"zinr": res_line.zinr}, ['zikatnr', 'typ', '_recid'])

                    if zimmer:

                        o_list = query(o_list_list, filters=(lambda o_list: o_list.selected  and o_list.outlook_nr == zimmer.typ), first=True)
                        do_it = None != o_list

                if do_it:

                    if dayuse_flag:

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

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                     (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                            if reslin_queasy and reslin_queasy.number3 != 0:
                                pax = reslin_queasy.number3

                        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

                        if room_list:
                            consider_it = True

                            if res_line.zimmerfix:

                                rline1 = db_session.query(Rline1).filter(
                                         (Rline1.resnr == res_line.resnr) & (Rline1.reslinnr != res_line.reslinnr) & (Rline1.resstatus == 8) & (Rline1.abreise >= datum)).first()

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
                                tot_rmrev =  to_decimal("0")

                                if (show_rev == 1 or show_rev == 2) and res_line.zipreis > 0:

                                    if incl_tent == False:

                                        if res_line.resstatus != 3:
                                            fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))
                                    else:
                                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, curr_date))

                                if net_lodg == None:
                                    net_lodg =  to_decimal("0")

                                if tot_rmrev == None:
                                    tot_rmrev =  to_decimal("0")


                                room_list.others[0] = room_list.others[0] + tot_breakfast
                                room_list.others[1] = room_list.others[1] + tot_lunch
                                room_list.others[2] = room_list.others[2] + tot_dinner
                                room_list.others[3] = room_list.others[3] + tot_other
                                room_list.others[4] = room_list.others[0] / exchg_rate
                                room_list.others[5] = room_list.others[1] / exchg_rate
                                room_list.others[6] = room_list.others[2] / exchg_rate
                                room_list.others[7] = room_list.others[3] / exchg_rate

                                fixleist = Fixleist()
                                for fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt, fixleist.betrag, fixleist.number, fixleist._recid in db_session.query(Fixleist.artnr, Fixleist.departement, Fixleist.sequenz, Fixleist.dekade, Fixleist.lfakt, Fixleist.betrag, Fixleist.number, Fixleist._recid).filter(
                                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                                    post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")
                                    fcost =  to_decimal("0")

                                    if post_it:

                                        artikel = get_cache (Artikel, {"artnr": fixleist.artnr, "departement": fixleist.departement}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

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

                                arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argt_artikelnr', 'argtnr', 'options', '_recid'])

                                if arrangement:

                                    argt_line = Argt_line()
                                    for argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, argt_line.betriebsnr, argt_line.argtnr, argt_line.betrag, argt_line._recid in db_session.query(Argt_line.argt_artnr, Argt_line.departement, Argt_line.fakt_modus, Argt_line.intervall, Argt_line.betriebsnr, Argt_line.argtnr, Argt_line.betrag, Argt_line._recid).filter(
                                             (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():
                                        post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall)
                                        service =  to_decimal("0")
                                        vat =  to_decimal("0")
                                        fcost =  to_decimal("0")

                                        if post_it:

                                            artikel = get_cache (Artikel, {"artnr": argt_line.argt_artnr, "departement": argt_line.departement}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

                                            if artikel:
                                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                            if argt_line.vt_percnt == 0:

                                                if argt_line.betriebsnr == 0:
                                                    pax = res_line.erwachs
                                                else:
                                                    pax = argt_line.betriebsnr

                                            elif argt_line.vt_percnt == 1:
                                                pax = res_line.kind1

                                            elif argt_line.vt_percnt == 2:
                                                pax = res_line.kind2
                                            else:
                                                pax = 0
                                            price = 0

                                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                                            if reslin_queasy:

                                                reslin_queasy = Reslin_queasy()
                                                for reslin_queasy.number3, reslin_queasy.deci1, reslin_queasy.deci2, reslin_queasy.deci3, reslin_queasy._recid in db_session.query(Reslin_queasy.number3, Reslin_queasy.deci1, Reslin_queasy.deci2, Reslin_queasy.deci3, Reslin_queasy._recid).filter(
                                                         (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():

                                                    if reslin_queasy.deci1 != 0:
                                                        price = reslin_queasy.deci1

                                                    elif reslin_queasy.deci2 != 0:
                                                        price = reslin_queasy.deci2

                                                    elif reslin_queasy.deci3 != 0:
                                                        price = reslin_queasy.deci3

                                                    if price != 0:
                                                        fcost =  to_decimal(price) * to_decimal(pax)
                                                        fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )


                                            if price == 0:
                                                fcost =  to_decimal(argt_line.betrag) * to_decimal(pax)
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

                                    kontline = get_cache (Kontline, {"gastnr": res_line.gastnr, "ankunft": datum, "zikatnr": res_line.zikatnr, "betriebsnr": 1, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

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

                                    kontline = get_cache (Kontline, {"gastnr": res_line.gastnr, "ankunft": datum, "zikatnr": res_line.zikatnr, "betriebsnr": 1, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

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

                                kline = get_cache (Kontline, {"kontignr": res_line.kontignr, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

                                if kline:

                                    kontline = db_session.query(Kontline).filter(
                                             (Kontline.kontcode == kline.kontcode) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).first()

                                    if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                                        room_list.room[13] = room_list.room[13] - res_line.zimmeranz
                                        rm_array[13] = rm_array[13] - res_line.zimmeranz

        for datum in date_range(d2,to_date) :

            kontline = Kontline()
            for kontline.zikatnr, kontline.zimmeranz, kontline.arrangement, kontline.gastnr, kontline.erwachs, kontline.kind1, kontline._recid in db_session.query(Kontline.zikatnr, Kontline.zimmeranz, Kontline.arrangement, Kontline.gastnr, Kontline.erwachs, Kontline.kind1, Kontline._recid).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == kontline.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == kontline.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                if do_it and not all_segm:

                    guest = get_cache (Guest, {"gastnr": kontline.gastnr}, ['gastnr', '_recid'])

                    guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr, "reihenfolge": 1}, ['segmentcode', '_recid'])

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr}, ['segmentcode', '_recid'])

                    if guestseg:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                if excl_compl and do_it:

                    guest = get_cache (Guest, {"gastnr": kontline.gastnr}, ['gastnr', '_recid'])

                    guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr, "reihenfolge": 1}, ['segmentcode', '_recid'])

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr}, ['segmentcode', '_recid'])

                    if guestseg:

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == guestseg.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                if do_it:

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
        for i in range(1,tmpint + 1) :
            datum = datum + timedelta(days=1)

            room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

            queasy_obj_list = {}
            queasy = Queasy()
            zimmer = Zimmer()
            for queasy.number3, queasy.char2, queasy.number1, queasy.char3, queasy._recid, zimmer.zikatnr, zimmer.typ, zimmer._recid in db_session.query(Queasy.number3, Queasy.char2, Queasy.number1, Queasy.char3, Queasy._recid, Zimmer.zikatnr, Zimmer.typ, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Queasy.char1) & (Zimmer.sleeping)).filter(
                     (Queasy.key == 14) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy_obj_list.get(queasy._recid):
                    continue
                else:
                    queasy_obj_list[queasy._recid] = True

                guestseg = get_cache (Guestseg, {"gastnr": queasy.number3, "reihenfolge": 1}, ['segmentcode', '_recid'])

                if not guestseg:

                    guestseg = get_cache (Guestseg, {"gastnr": queasy.number3}, ['segmentcode', '_recid'])
                do_it = None != guestseg

                if not all_segm and do_it:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == queasy.char2 and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)
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


        for i in range(1,tmpint + 1) :
            datum = datum + timedelta(days=1)
            anzahl_dayuse = 0


            tot_room = get_active_room(datum)
            accum_tot_room = accum_tot_room + tot_room

            dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == datum), first=True)

            if dayuse_list:
                anzahl_dayuse = dayuse_list.zimmeranz

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

                zinrstat = get_cache (Zinrstat, {"zinr": "ooo", "datum": room_list.datum}, ['zimmeranz', '_recid'])

                if zinrstat:

                    if not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

                        if z_list:
                            room_list.room[14] = zinrstat.zimmeranz
                            rm_array[14] = rm_array[14] + zinrstat.zimmeranz


                    else:
                        room_list.room[14] = zinrstat.zimmeranz
                        rm_array[14] = rm_array[14] + zinrstat.zimmeranz


            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= room_list.datum) & (Outorder.gespende >= room_list.datum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True

                    if not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

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
        jml_date = (to_date - curr_date).days
        jml_date = jml_date + 1


        do_it = True

        if show_rev == 1 or show_rev == 2:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.selected)):
                counter = counter + 1

                segment = get_cache (Segment, {"segmentcode": s_list.segm}, ['vip_level', 'betriebsnr', '_recid'])

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

                    if room_list.datum != None:

                        if room_list.datum < ci_date:

                            htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

                            waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

                            if waehrung:

                                exrate = get_cache (Exrate, {"datum": room_list.datum, "artnr": waehrung.waehrungsnr}, ['betrag', '_recid'])

                                if exrate:
                                    exchg_rate =  to_decimal(exrate.betrag)
                        else:

                            htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

                            waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

                            if waehrung:
                                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                            else:
                                exchg_rate =  to_decimal("1")
                    room_list.lodg[4] = room_list.lodg[4] + othrev
                    room_list.lodg[6] = room_list.lodg[4] / exchg_rate

                    if room_list.wd != 0:
                        t_lodg[4] = t_lodg[4] + othrev


                    t_lodg[6] = t_lodg[6] + (othrev / exchg_rate)
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.bezeich = " TOTAL"

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
            sum_breakfast =  to_decimal(sum_breakfast) + to_decimal(room_list.others[0])
            sum_lunch =  to_decimal(sum_lunch) + to_decimal(room_list.others[1])
            sum_dinner =  to_decimal(sum_dinner) + to_decimal(room_list.others[2])
            sum_other =  to_decimal(sum_other) + to_decimal(room_list.others[3])
            sum_breakfast_usd =  to_decimal(sum_breakfast_usd) + to_decimal(room_list.others[4])
            sum_lunch_usd =  to_decimal(sum_lunch_usd) + to_decimal(room_list.others[5])
            sum_dinner_usd =  to_decimal(sum_dinner_usd) + to_decimal(room_list.others[6])
            sum_other_usd =  to_decimal(sum_other_usd) + to_decimal(room_list.others[7])
            sum_comp =  to_decimal(sum_comp) + to_decimal(room_list.room_comp)
            t_revpar =  to_decimal(t_revpar) + to_decimal(room_list.revpar)
            t_revpar2 =  to_decimal(t_revpar2) + to_decimal(room_list.revpar2)
            t_rmrate =  to_decimal(t_rmrate) + to_decimal(room_list.rmrate)
            t_rmrate2 =  to_decimal(t_rmrate2) + to_decimal(room_list.rmrate2)

        room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)

        if tavg_rmrev == None:
            tavg_rmrev =  to_decimal("0")

        if tavg_rmrev2 == None:
            tavg_rmrev2 =  to_decimal("0")
        room_list.avrglodg =  to_decimal(avrg_lodging) / to_decimal(tmpint)
        room_list.avrglodg2 =  to_decimal(avrg_lodging2) / to_decimal(tmpint)
        room_list.avrgrmrev =  to_decimal(tavg_rmrev)
        room_list.avrgrmrev2 =  to_decimal(tavg_rmrev2)
        room_list.others[0] = sum_breakfast
        room_list.others[1] = sum_lunch
        room_list.others[2] = sum_dinner
        room_list.others[3] = sum_other
        room_list.others[4] = sum_breakfast_usd
        room_list.others[5] = sum_lunch_usd
        room_list.others[6] = sum_dinner_usd
        room_list.others[7] = sum_other_usd
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

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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

            for bsegm in query(bsegm_list, filters=(lambda bsegm: bsegm.selected)):

                if length(bsegm.bezeich) >= 0:
                    segm_name = segm_name + substring(bsegm.bezeich, 4, length(bsegm.bezeich) - 3) + "; "

            if length(segm_name) >= 0:
                segm_name = substring(segm_name, 0, length(segm_name) - 2)
        a = length(segm_name)
        a = length(segm_name)

        if a > 80:
            for e in range(1,a + 1) :
                counter = counter + 1
                print_list = Print_list()
                print_list_list.append(print_list)


                if length(segm_name) >= 0:
                    print_list.code_name = substring(segm_name, e - 1, 80)
                e = (counter * 80) + 1
        else:
            print_list = Print_list()
            print_list_list.append(print_list)


            if length(segm_name) >= 0:
                print_list.code_name = substring(segm_name, r - 1, a)

            if length(print_list.code_name) > 0:
                print_list.code_name = substring(print_list.code_name, 1, (length(print_list.code_name) - 1))


    def argt_code_name():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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

            for bargt in query(bargt_list, filters=(lambda bargt: bargt.selected)):
                argm_name = argm_name + bargt.bezeich + "; "

            if length(argm_name) > 0:
                argm_name = substring(argm_name, 0, length(argm_name) - 2)
        a = length(argm_name)
        a = length(argm_name)

        if a > 80:
            print_list2 = Print_list2()
            print_list2_list.append(print_list2)


            if a > 0:
                argm = substring(argm_name, r + 1 - 1, a)

            if length(argm) > 0:
                argm = substring(argm, 1, (length(argm) - 1))
        else:
            print_list2 = Print_list2()
            print_list2_list.append(print_list2)


            if a > 0:
                argm = substring(argm_name, r - 1, a)

            if length(argm) > 0:
                argm = substring(argm, 1, (length(argm) - 1))


    def room_code_name():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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

            for broom in query(broom_list, filters=(lambda broom: broom.selected)):
                room_name = room_name + broom.bezeich + "; "

            if length(room_name) > 0:
                room_name = substring(room_name, 0, length(room_name) - 2)
        curr_time = get_current_time_in_seconds()


        a = length(room_name)
        a = length(room_name)

        if a > 80:
            print_list3 = Print_list3()
            print_list3_list.append(print_list3)


            if a > 0:
                room = substring(room_name, r + 1 - 1, a)

            if length(room) > 0:
                room = substring(room, 1, (length(room) - 1))
        else:
            print_list3 = Print_list3()
            print_list3_list.append(print_list3)


            if a > 0:
                room = substring(room_name, r - 1, a)

            if length(room) > 0:
                room = substring(room, 1, (length(room) - 1))


    def create_browse1():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        datum:date = None
        datum1:date = None
        datum2:date = None
        i:int = 0
        wd:int = 0
        p_room:int = 0
        p_lodg:Decimal = to_decimal("0.0")
        prev_room:int = 0
        p_pax:int = 0
        avrg_rate:Decimal = to_decimal("0.0")
        do_it:bool = False
        consider_it:bool = False
        dayuse_flag:bool = False
        n:int = 0
        kont_doit:bool = False
        allot_doit:bool = False
        mtd_occ:Decimal = to_decimal("0.0")
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        curr_i:int = 0
        rsvstat:str = ""
        avrg_lodging:Decimal = to_decimal("0.0")
        anzahl_dayuse:int = 0
        kline = None
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_fixcost:Decimal = to_decimal("0.0")
        tot_fixcost2:Decimal = to_decimal("0.0")
        sum_breakfast:Decimal = to_decimal("0.0")
        sum_lunch:Decimal = to_decimal("0.0")
        sum_dinner:Decimal = to_decimal("0.0")
        sum_other:Decimal = to_decimal("0.0")
        sum_breakfast_usd:Decimal = to_decimal("0.0")
        sum_lunch_usd:Decimal = to_decimal("0.0")
        sum_dinner_usd:Decimal = to_decimal("0.0")
        sum_other_usd:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        tavg_rmrev:Decimal = to_decimal("0.0")
        tavg_rmrev2:Decimal = to_decimal("0.0")
        troom_exccomp:int = 0
        othrev:Decimal = to_decimal("0.0")
        t_avrglodg_inclcomp:Decimal = to_decimal("0.0")
        t_avrglodg_exclcomp:Decimal = to_decimal("0.0")
        t_rmocc_exclcomp:Decimal = to_decimal("0.0")
        t_room_comp:int = 0
        curr_resnr:int = 0
        curr_segm:int = 0
        tmax:int = 0
        tmin:int = 0
        counter:int = 0
        jml1:int = 0
        jml2:Decimal = to_decimal("0.0")
        jml3:Decimal = to_decimal("0.0")
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

        zimmer = Zimmer()
        for zimmer.zikatnr, zimmer.typ, zimmer._recid in db_session.query(Zimmer.zikatnr, Zimmer.typ, Zimmer._recid).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():

            if all_zikat:
                tot_room = tot_room + 1
            else:

                z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

                if z_list:
                    tot_room = tot_room + 1
        datum = curr_date - timedelta(days=1)
        for i in range(1,tmpint + 1) :
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

            kontline = Kontline()
            for kontline.zikatnr, kontline.zimmeranz, kontline.arrangement, kontline.gastnr, kontline.erwachs, kontline.kind1, kontline._recid in db_session.query(Kontline.zikatnr, Kontline.zimmeranz, Kontline.arrangement, Kontline.gastnr, Kontline.erwachs, Kontline.kind1, Kontline._recid).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                allot_doit = True

                if kontline.zikatnr != 0 and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == kontline.zikatnr and z_list.selected), first=True)
                    allot_doit = None != z_list

                if allot_doit and (datum >= (ci_date + timedelta(days=kontline.ruecktage))):
                    room_list.room[13] = room_list.room[13] + kontline.zimmeranz
                    rm_array[13] = rm_array[13] + kontline.zimmeranz
        curr_time = get_current_time_in_seconds()

        res_line = Res_line()
        for res_line.resnr, res_line.ankunft, res_line.abreise, res_line.arrangement, res_line.reslinnr, res_line.zikatnr, res_line.zinr, res_line.gastnr, res_line.gratis, res_line.erwachs, res_line.kind1, res_line.zipreis, res_line._recid, res_line.kind2, res_line.resstatus, res_line.zimmerfix, res_line.zimmeranz, res_line.kontignr in db_session.query(Res_line.resnr, Res_line.ankunft, Res_line.abreise, Res_line.arrangement, Res_line.reslinnr, Res_line.zikatnr, Res_line.zinr, Res_line.gastnr, Res_line.gratis, Res_line.erwachs, Res_line.kind1, Res_line.zipreis, Res_line._recid, Res_line.kind2, Res_line.resstatus, Res_line.zimmerfix, Res_line.zimmeranz, Res_line.kontignr).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.ankunft <= to_date) & (Res_line.abreise >= curr_date)) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == ci_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            curr_i = 0
            tot_breakfast =  to_decimal("0")
            tot_lunch =  to_decimal("0")
            tot_dinner =  to_decimal("0")
            tot_other =  to_decimal("0")
            dayuse_flag = False

            if curr_resnr != res_line.resnr:

                reservation = get_cache (Reservation, {"resnr": res_line.resnr}, ['segmentcode', '_recid'])
                curr_resnr = res_line.resnr
                curr_segm = reservation.segmentcode

            if not vhp_limited:
                do_it = True
            else:

                segment = get_cache (Segment, {"segmentcode": curr_segm}, ['vip_level', 'betriebsnr', '_recid'])
                do_it = None != segment and segment.vip_level == 0

            room_list = query(room_list_list, filters=(lambda room_list: room_list.datum >= res_line.ankunft and room_list.datum <= res_line.abreise), first=True)

            if not room_list:
                do_it = False

            if do_it and res_line.resstatus == 8 and res_line.ankunft == ci_date and res_line.abreise == ci_date:
                dayuse_flag = True

                arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argt_artikelnr', 'argtnr', 'options', '_recid'])

                bill_line = db_session.query(Bill_line).filter(
                         (Bill_line.departement == 0) & (Bill_line.artnr == arrangement.argt_artikelnr) & (Bill_line.bill_datum == ci_date) & (Bill_line.massnr == res_line.resnr) & (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            if do_it and not all_segm:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == reservation.segmentcode and s_list.selected), first=True)
                do_it = None != s_list

            if do_it and not all_argt:

                a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == res_line.arrangement and a_list.selected), first=True)
                do_it = None != a_list

            if do_it and not all_zikat:

                z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == res_line.zikatnr and z_list.selected), first=True)
                do_it = None != z_list
            kont_doit = True

            if do_it and (not all_segm) and (res_line.kontignr < 0):

                s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == curr_segm and s_list.selected), first=True)
                kont_doit = None != s_list

            zimmer = get_cache (Zimmer, {"zinr": res_line.zinr}, ['zikatnr', 'typ', '_recid'])

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

            if excl_compl and do_it:

                segment = db_session.query(Segment).filter(
                         (Segment.segmentcode == curr_segm) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                if segment:
                    do_it = False


                else:

                    if res_line.zipreis == 0 and res_line.gratis != 0:
                        do_it = False

            if do_it and not all_outlook:

                zimmer = get_cache (Zimmer, {"zinr": res_line.zinr}, ['zikatnr', 'typ', '_recid'])

                if zimmer:

                    o_list = query(o_list_list, filters=(lambda o_list: o_list.selected  and o_list.outlook_nr == zimmer.typ), first=True)
                    do_it = None != o_list

            if do_it:

                if dayuse_flag:

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

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                        if reslin_queasy and reslin_queasy.number3 != 0:
                            pax = reslin_queasy.number3

                    room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

                    if room_list:
                        consider_it = True

                        if res_line.zimmerfix:

                            rline1 = db_session.query(Rline1).filter(
                                     (Rline1.resnr == res_line.resnr) & (Rline1.reslinnr != res_line.reslinnr) & (Rline1.resstatus == 8) & (Rline1.abreise > datum)).first()

                            if rline1:
                                consider_it = False

                        if datum == res_line.abreise:
                            pass
                        else:

                            fixleist = Fixleist()
                            for fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt, fixleist.betrag, fixleist.number, fixleist._recid in db_session.query(Fixleist.artnr, Fixleist.departement, Fixleist.sequenz, Fixleist.dekade, Fixleist.lfakt, Fixleist.betrag, Fixleist.number, Fixleist._recid).filter(
                                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
                                service =  to_decimal("0")
                                vat =  to_decimal("0")
                                fcost =  to_decimal("0")

                                if post_it:

                                    artikel = get_cache (Artikel, {"artnr": fixleist.artnr, "departement": fixleist.departement}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

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

                            arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argt_artikelnr', 'argtnr', 'options', '_recid'])

                            if arrangement:

                                argt_line = Argt_line()
                                for argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall, argt_line.betriebsnr, argt_line.argtnr, argt_line.betrag, argt_line._recid in db_session.query(Argt_line.argt_artnr, Argt_line.departement, Argt_line.fakt_modus, Argt_line.intervall, Argt_line.betriebsnr, Argt_line.argtnr, Argt_line.betrag, Argt_line._recid).filter(
                                         (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():
                                    post_it = check_fixargt_posted(argt_line.argt_artnr, argt_line.departement, argt_line.fakt_modus, argt_line.intervall)
                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")
                                    fcost =  to_decimal("0")

                                    if post_it:

                                        artikel = get_cache (Artikel, {"artnr": argt_line.argt_artnr, "departement": argt_line.departement}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

                                        if artikel:
                                            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                        if argt_line.vt_percnt == 0:

                                            if argt_line.betriebsnr == 0:
                                                pax = res_line.erwachs
                                            else:
                                                pax = argt_line.betriebsnr

                                        elif argt_line.vt_percnt == 1:
                                            pax = res_line.kind1

                                        elif argt_line.vt_percnt == 2:
                                            pax = res_line.kind2
                                        else:
                                            pax = 0
                                        price = 0

                                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                                 (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                                        if reslin_queasy:

                                            reslin_queasy = Reslin_queasy()
                                            for reslin_queasy.number3, reslin_queasy.deci1, reslin_queasy.deci2, reslin_queasy.deci3, reslin_queasy._recid in db_session.query(Reslin_queasy.number3, Reslin_queasy.deci1, Reslin_queasy.deci2, Reslin_queasy.deci3, Reslin_queasy._recid).filter(
                                                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():

                                                if reslin_queasy.deci1 != 0:
                                                    price = reslin_queasy.deci1

                                                elif reslin_queasy.deci2 != 0:
                                                    price = reslin_queasy.deci2

                                                elif reslin_queasy.deci3 != 0:
                                                    price = reslin_queasy.deci3

                                                if price != 0:
                                                    fcost =  to_decimal(price) * to_decimal(pax)
                                                    fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )


                                        if price == 0:
                                            fcost =  to_decimal(argt_line.betrag) * to_decimal(pax)
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

                            if net_lodg == None:
                                net_lodg =  to_decimal("0")

                            if tot_rmrev == None:
                                tot_rmrev =  to_decimal("0")


                            room_list.others[0] = room_list.others[0] + tot_breakfast
                            room_list.others[1] = room_list.others[1] + tot_lunch
                            room_list.others[2] = room_list.others[2] + tot_dinner
                            room_list.others[3] = room_list.others[3] + tot_other
                            room_list.others[4] = room_list.others[0] / exchg_rate
                            room_list.others[5] = room_list.others[1] / exchg_rate
                            room_list.others[6] = room_list.others[2] / exchg_rate
                            room_list.others[7] = room_list.others[3] / exchg_rate

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

                                kontline = get_cache (Kontline, {"gastnr": res_line.gastnr, "ankunft": datum, "zikatnr": res_line.zikatnr, "betriebsnr": 1, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

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

                                kontline = get_cache (Kontline, {"gastnr": res_line.gastnr, "ankunft": datum, "zikatnr": res_line.zikatnr, "betriebsnr": 1, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

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

                            kline = get_cache (Kontline, {"kontignr": res_line.kontignr, "kontstatus": 1}, ['zikatnr', 'zimmeranz', 'arrangement', 'gastnr', 'erwachs', 'kind1', '_recid'])

                            if kline:

                                kontline = db_session.query(Kontline).filter(
                                         (Kontline.kontcode == kline.kontcode) & (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 0) & (Kontline.kontstatus == 1)).first()

                                if kontline and datum >= (ci_date + timedelta(days=kontline.ruecktage)):
                                    room_list.room[13] = room_list.room[13] - res_line.zimmeranz
                                    rm_array[13] = rm_array[13] - res_line.zimmeranz


        for datum in date_range(curr_date,to_date) :

            kontline = Kontline()
            for kontline.zikatnr, kontline.zimmeranz, kontline.arrangement, kontline.gastnr, kontline.erwachs, kontline.kind1, kontline._recid in db_session.query(Kontline.zikatnr, Kontline.zimmeranz, Kontline.arrangement, Kontline.gastnr, Kontline.erwachs, Kontline.kind1, Kontline._recid).filter(
                     (Kontline.ankunft <= datum) & (Kontline.abreise >= datum) & (Kontline.betriebsnr == 1) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                do_it = True

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == kontline.arrangement and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == kontline.zikatnr and z_list.selected), first=True)
                    do_it = None != z_list

                if do_it and not all_segm:

                    guest = get_cache (Guest, {"gastnr": kontline.gastnr}, ['gastnr', '_recid'])

                    guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr, "reihenfolge": 1}, ['segmentcode', '_recid'])

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr}, ['segmentcode', '_recid'])

                    if guestseg:

                        s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                        do_it = None != s_list

                if excl_compl and do_it:

                    guest = get_cache (Guest, {"gastnr": kontline.gastnr}, ['gastnr', '_recid'])

                    guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr, "reihenfolge": 1}, ['segmentcode', '_recid'])

                    if not guestseg:

                        guestseg = get_cache (Guestseg, {"gastnr": guest.gastnr}, ['segmentcode', '_recid'])

                    if guestseg:

                        segment = db_session.query(Segment).filter(
                                 (Segment.segmentcode == guestseg.segmentcode) & ((Segment.betriebsnr == 1) | (Segment.betriebsnr == 2))).first()

                        if segment:
                            do_it = False

                if do_it:

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
        room_list = Room_list()
        room_list_list.append(room_list)

        room_list.bezeich = " TOTAL"

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
        for i in range(1,tmpint + 1) :
            datum = datum + timedelta(days=1)

            room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == datum), first=True)

            queasy_obj_list = {}
            queasy = Queasy()
            zimmer = Zimmer()
            for queasy.number3, queasy.char2, queasy.number1, queasy.char3, queasy._recid, zimmer.zikatnr, zimmer.typ, zimmer._recid in db_session.query(Queasy.number3, Queasy.char2, Queasy.number1, Queasy.char3, Queasy._recid, Zimmer.zikatnr, Zimmer.typ, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Queasy.char1) & (Zimmer.sleeping)).filter(
                     (Queasy.key == 14) & (Queasy.date1 <= datum) & (Queasy.date2 >= datum)).order_by(Queasy._recid).all():
                if queasy_obj_list.get(queasy._recid):
                    continue
                else:
                    queasy_obj_list[queasy._recid] = True

                guestseg = get_cache (Guestseg, {"gastnr": queasy.number3, "reihenfolge": 1}, ['segmentcode', '_recid'])

                if not guestseg:

                    guestseg = get_cache (Guestseg, {"gastnr": queasy.number3}, ['segmentcode', '_recid'])
                do_it = None != guestseg

                if not all_segm and do_it:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == guestseg.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    a_list = query(a_list_list, filters=(lambda a_list: a_list.argt == queasy.char2 and a_list.selected), first=True)
                    do_it = None != a_list

                if do_it and not all_zikat:

                    z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)
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


        for i in range(1,tmpint + 1) :
            datum = datum + timedelta(days=1)
            anzahl_dayuse = 0

            dayuse_list = query(dayuse_list_list, filters=(lambda dayuse_list: dayuse_list.datum == datum), first=True)

            if dayuse_list:
                anzahl_dayuse = dayuse_list.zimmeranz

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

                zinrstat = get_cache (Zinrstat, {"zinr": "ooo", "datum": room_list.datum}, ['zimmeranz', '_recid'])

                if zinrstat:
                    room_list.room[14] = zinrstat.zimmeranz
                    rm_array[14] = rm_array[14] + zinrstat.zimmeranz


            else:

                outorder_obj_list = {}
                for outorder, zimmer in db_session.query(Outorder, Zimmer).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).filter(
                         (Outorder.gespstart <= room_list.datum) & (Outorder.gespende >= room_list.datum) & (Outorder.betriebsnr <= 1)).order_by(Outorder._recid).all():
                    if outorder_obj_list.get(outorder._recid):
                        continue
                    else:
                        outorder_obj_list[outorder._recid] = True

                    if not all_zikat:

                        z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zimmer.zikatnr and z_list.selected), first=True)

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
        jml_date = (to_date - curr_date).days
        jml_date = jml_date + 1


        do_it = True

        if show_rev == 1 or show_rev == 2:

            for s_list in query(s_list_list, filters=(lambda s_list: s_list.selected)):
                counter = counter + 1

                segment = get_cache (Segment, {"segmentcode": s_list.segm}, ['vip_level', 'betriebsnr', '_recid'])

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

                    if room_list.datum != None:

                        if room_list.datum < ci_date:

                            htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

                            waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

                            if waehrung:

                                exrate = get_cache (Exrate, {"datum": room_list.datum, "artnr": waehrung.waehrungsnr}, ['betrag', '_recid'])

                                if exrate:
                                    exchg_rate =  to_decimal(exrate.betrag)
                        else:

                            htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

                            waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

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
        mtd_occ =  to_decimal(rm_array[6]) / to_decimal((tot_room) * to_decimal(tmpint)) * to_decimal("100")
        t_rmocc_exclcomp = ( to_decimal(rm_array[6]) - to_decimal(t_room_comp)) / to_decimal((tot_room) * to_decimal(tmpint)) * to_decimal("100")

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
            sum_breakfast =  to_decimal(sum_breakfast) + to_decimal(room_list.others[0])
            sum_lunch =  to_decimal(sum_lunch) + to_decimal(room_list.others[1])
            sum_dinner =  to_decimal(sum_dinner) + to_decimal(room_list.others[2])
            sum_other =  to_decimal(sum_other) + to_decimal(room_list.others[3])


            sum_breakfast_usd =  to_decimal(sum_breakfast_usd) + to_decimal(room_list.others[4])
            sum_lunch_usd =  to_decimal(sum_lunch_usd) + to_decimal(room_list.others[5])
            sum_dinner_usd =  to_decimal(sum_dinner_usd) + to_decimal(room_list.others[6])
            sum_other_usd =  to_decimal(sum_other_usd) + to_decimal(room_list.others[7])
            sum_comp =  to_decimal(sum_comp) + to_decimal(room_list.room_comp)
            t_revpar =  to_decimal(t_revpar) + to_decimal(room_list.revpar)
            t_revpar2 =  to_decimal(t_revpar2) + to_decimal(room_list.revpar2)
            t_rmrate =  to_decimal(t_rmrate) + to_decimal(room_list.rmrate)
            t_rmrate2 =  to_decimal(t_rmrate2) + to_decimal(room_list.rmrate2)

        room_list = query(room_list_list, filters=(lambda room_list: room_list.wd == 0), first=True)

        if tavg_rmrev == None:
            tavg_rmrev =  to_decimal("0")

        if tavg_rmrev2 == None:
            tavg_rmrev2 =  to_decimal("0")
        room_list.avrglodg =  to_decimal(avrg_lodging) / to_decimal(tmpint)
        room_list.avrgrmrev =  to_decimal(tavg_rmrev)
        room_list.avrgrmrev2 =  to_decimal(tavg_rmrev2)
        room_list.others[0] = sum_breakfast
        room_list.others[1] = sum_lunch
        room_list.others[2] = sum_dinner
        room_list.others[3] = sum_other
        room_list.others[4] = sum_breakfast_usd
        room_list.others[5] = sum_lunch_usd
        room_list.others[6] = sum_dinner_usd
        room_list.others[7] = sum_other_usd
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

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        do_it:bool = False
        S_list = Segm_list
        s_list_list = segm_list_list

        room_list = query(room_list_list, filters=(lambda room_list: room_list.datum == curr_date), first=True)

        if curr_date <= ci_date:

            genstat = Genstat()
            for genstat.zinr, genstat.segmentcode, genstat.argt, genstat.zikatnr, genstat.erwachs, genstat.kind1, genstat.kind2, genstat.gratis, genstat.res_date, genstat.datum, genstat.resstatus, genstat.res_logic, genstat.logis, genstat.ratelocal, genstat.res_deci, genstat.resnr, genstat.res_int, genstat._recid in db_session.query(Genstat.zinr, Genstat.segmentcode, Genstat.argt, Genstat.zikatnr, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat.gratis, Genstat.res_date, Genstat.datum, Genstat.resstatus, Genstat.res_logic, Genstat.logis, Genstat.ratelocal, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat._recid).filter(
                     (Genstat.datum == curr_date - timedelta(days=1)) & (Genstat.res_logic[inc_value(1)]) & (Genstat.zinr != "") & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
                do_it = True

                if do_it and not all_segm:

                    s_list = query(s_list_list, filters=(lambda s_list: s_list.segm == genstat.segmentcode and s_list.selected), first=True)
                    do_it = None != s_list

                if do_it and not all_argt:

                    argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argt == genstat.argt and argt_list.selected), first=True)
                    do_it = None != argt_list

                if do_it and not all_zikat:

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

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        rsvstat = ""
        curr_anz:int = 0
        curr_date:date = None
        start_date:date = None

        def generate_inner_output():
            return (rsvstat)


        queasy = get_cache (Queasy, {"key": 37, "number1": get_year(datum)}, ['number3', 'char2', 'number1', 'char3', '_recid'])

        if not queasy:

            return generate_inner_output()
        start_date = date_mdy(1, 1, get_year(datum))
        curr_anz = 0


        for curr_date in date_range(start_date,datum) :
            curr_anz = curr_anz + 1
        rsvstat = " " + substring(queasy.char3, curr_anz - 1, 1)

        return generate_inner_output()


    def check_bonus():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        end_date:date = None
        actual_date:date = None
        Z_list = Zikat_list
        z_list_list = zikat_list_list

        if to_date < ci_date:
            end_date = to_date
        else:
            end_date = ci_date - timedelta(days=1)

        if all_zikat:

            zkstat = Zkstat()
            for zkstat.datum, zkstat.anz100, zkstat.zikatnr, zkstat._recid in db_session.query(Zkstat.datum, Zkstat.anz100, Zkstat.zikatnr, Zkstat._recid).filter(
                     (Zkstat.datum >= curr_date) & (Zkstat.datum <= end_date)).order_by(Zkstat.datum).all():

                if actual_date != zkstat.datum:
                    active_rm_list = Active_rm_list()
                    active_rm_list_list.append(active_rm_list)

                    active_rm_list.datum = zkstat.datum
                    actual_date = zkstat.datum


                active_rm_list.zimmeranz = active_rm_list.zimmeranz + zkstat.anz100

        else:

            zkstat = Zkstat()
            for zkstat.datum, zkstat.anz100, zkstat.zikatnr, zkstat._recid in db_session.query(Zkstat.datum, Zkstat.anz100, Zkstat.zikatnr, Zkstat._recid).filter(
                     (Zkstat.datum >= curr_date) & (Zkstat.datum <= end_date)).order_by(Zkstat.datum).all():

                z_list = query(z_list_list, filters=(lambda z_list: z_list.zikatnr == zkstat.zikatnr and z_list.selected), first=True)

                if z_list:

                    if actual_date != zkstat.datum:
                        active_rm_list = Active_rm_list()
                        active_rm_list_list.append(active_rm_list)

                        active_rm_list.datum = zkstat.datum
                        actual_date = zkstat.datum


                    active_rm_list.zimmeranz = active_rm_list.zimmeranz + zkstat.anz100

    def get_active_room(curr_datum:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        active_room = 0

        def generate_inner_output():
            return (active_room)


        if curr_datum >= ci_date:
            active_room = actual_tot_room

            return generate_inner_output()

        active_rm_list = query(active_rm_list_list, filters=(lambda active_rm_list: active_rm_list.datum == curr_datum), first=True)

        if active_rm_list:
            active_room = active_rm_list.zimmeranz

        return generate_inner_output()


    def get_mtd_active_room():

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        othrev = to_decimal("0.0")
        i:int = 0
        max_i:int = 0
        art_list:List[int] = create_empty_list(200,0)
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (othrev)


        htparam = get_cache (Htparam, {"paramnr": 479}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
        serv_vat = htparam.flogical

        artikel = Artikel()
        for artikel.departement, artikel.artnr, artikel.service_code, artikel.mwst_code, artikel._recid in db_session.query(Artikel.departement, Artikel.artnr, Artikel.service_code, Artikel.mwst_code, Artikel._recid).filter(
                 (Artikel.departement == 0) & (Artikel.artart == 0) & (Artikel.umsatzart == 1)).order_by(Artikel.artnr).all():
            max_i = max_i + 1
            art_list[max_i - 1] = artikel.artnr
        for i in range(1,max_i + 1) :

            artikel = get_cache (Artikel, {"artnr": art_list[i - 1], "departement": 0}, ['departement', 'artnr', 'service_code', 'mwst_code', '_recid'])

            if artikel:
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                umsatz = Umsatz()
                for umsatz.departement, umsatz.artnr, umsatz.datum, umsatz.betrag, umsatz._recid in db_session.query(Umsatz.departement, Umsatz.artnr, Umsatz.datum, Umsatz.betrag, Umsatz._recid).filter(
                         (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum == datum)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                    othrev =  to_decimal(othrev) + to_decimal(umsatz.betrag) / to_decimal(fact)

        return generate_inner_output()


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

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
                delta = (lfakt - res_line.ankunft).days

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


    def check_fixargt_posted(artnr:int, dept:int, fakt_modus:int, intervall:int):

        nonlocal room_list_list, lvcarea, tot_rmrev, bonus_array, week_list, tent_pers, datum, tot_room, mtd_tot_room, accum_tot_room, actual_tot_room, segm_name, argm_name, room_name, ci_date, pax, t_lodg, jml_date, tot_avrg, t_rmrate, t_rmrate2, t_revpar, t_revpar2, price, price_decimal, new_contrate, rm_vat, rm_serv, rm_array, exchg_rate, sum_comp, post_it, fcost, curr_time, tmpint, res_line, kontline, zimmer, guest, zimkateg, waehrung, segment, genstat, fixleist, bill_line, queasy, reslin_queasy, argt_line, outorder, zkstat, artikel, umsatz, htparam, arrangement, exrate, reservation, guestseg, zinrstat
        nonlocal pvilanguage, op_type, flag_i, curr_date, to_date, all_segm, all_argt, all_zikat, exclooo, incl_tent, show_rev, vhp_limited, excl_compl, all_outlook, incl_oth
        nonlocal rline1


        nonlocal room_list, segm_list, argt_list, zikat_list, outlook_list, print_list, print_list2, print_list3, rline1, active_rm_list, dayuse_list, s_list, a_list, z_list, o_list, bsegm, bargt, broom, s_list, a_list, z_list, o_list, s_list, z_list
        nonlocal room_list_list, print_list_list, print_list2_list, print_list3_list, active_rm_list_list, dayuse_list_list

        post_it = False

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

            if curr_date <= (res_line.ankunft + (intervall - 1)):
                post_it = True

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": 87}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": 550}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": 144}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])

    waehrung = get_cache (Waehrung, {"wabkurz": htparam.fchar}, ['waehrungsnr', 'ankauf', 'einheit', '_recid'])

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": 127}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
    rm_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": 128}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
    rm_serv = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": 491}, ['finteger', 'fchar', 'flogical', 'fdate', '_recid'])
    price_decimal = htparam.finteger
    tmpint = (to_date - curr_date).days
    tmpint = tmpint + 1

    if op_type == 0:

        if curr_date < ci_date:
            create_browse()
        else:
            create_browse1()
        segm_code_name()
        room_code_name()
        argt_code_name()

    return generate_output()




def calc_servvat(depart:int, artnr:int, datum:date, service_code:int, mwst_code:int):

    prepare_cache ([Kontplan, Htparam])

    serv_htp = to_decimal("0.0")
    vat_htp = to_decimal("0.0")
    serv_vat:bool = False
    vat:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    kontplan = htparam = None

    db_session = local_storage.db_session

    def sgenerate_output():
        nonlocal serv_htp, vat_htp, serv_vat, vat, service, kontplan, htparam
        nonlocal depart, artnr, datum, service_code, mwst_code

        return {"serv_htp": serv_htp, "vat_htp": vat_htp}


    kontplan = get_cache (Kontplan, {"betriebsnr": depart, "kontignr": artnr, "datum": datum}, ['anzkont', 'anzconf', '_recid'])

    if kontplan:

        if kontplan.anzkont >= 10000000:
            serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000000")
            vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000000")


        else:
            serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000")
            vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000")


    else:

        if service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": service_code}, ['fdecimal', 'flogical', '_recid'])

            if htparam and htparam.fdecimal != 0:
                serv_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = get_cache (Htparam, {"paramnr": 479}, ['fdecimal', 'flogical', '_recid'])
                serv_vat = htparam.flogical

        if mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": mwst_code}, ['fdecimal', 'flogical', '_recid'])

            if htparam and htparam.fdecimal != 0:
                vat_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

            if vat_htp == 1:
                serv_htp =  to_decimal("0")

            elif serv_vat:
                vat_htp =  to_decimal(vat_htp) + to_decimal(vat_htp) * to_decimal(serv_htp)

    return sgenerate_output()



def get_room_breakdown(recid_resline:int, datum:date, curr_i:int, curr_date:date):

    prepare_cache ([Waehrung, Htparam, Res_line, Artikel, Guest_pr, Arrangement, Reslin_queasy, Katpreis, Pricecod, Argt_line])

    lvcarea:str = "occ-fcast1"
    fnet_lodging = to_decimal("0.0")
    lnet_lodging = to_decimal("0.0")
    net_breakfast = to_decimal("0.0")
    net_lunch = to_decimal("0.0")
    net_dinner = to_decimal("0.0")
    net_others = to_decimal("0.0")
    tot_rmrev = to_decimal("0.0")
    nett_vat = to_decimal("0.0")
    nett_service = to_decimal("0.0")
    exrate:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    new_contrate:bool = False
    bonus_array:List[bool] = create_empty_list(999, False)
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    rm_vat:bool = False
    rm_serv:bool = False
    nett_rmrev:Decimal = to_decimal("0.0")
    waehrung = guest = reslin_queasy = queasy = katpreis = pricecod = artikel = argt_line = htparam = res_line = guest_pr = arrangement = None

    waehrung1 = None

    Waehrung1 = create_buffer("Waehrung1",Waehrung)


    db_session = local_storage.db_session

    def rb_generate_output():
        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        return {"fnet_lodging": fnet_lodging, "lnet_lodging": lnet_lodging, "net_breakfast": net_breakfast, "net_lunch": net_lunch, "net_dinner": net_dinner, "net_others": net_others, "tot_rmrev": tot_rmrev, "nett_vat": nett_vat, "nett_service": nett_service}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def calc_lodging2():

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        qty:int = 0
        fixed_rate:bool = False
        it_exist:bool = False
        rmrate:Decimal = to_decimal("0.0")
        gpax:int = 0
        bill_date:date = None
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        restricted_disc:bool = False
        kback_flag:bool = False
        curr_zikatnr:int = 0
        w_day:int = 0
        rack_rate:bool = False
        vat:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat_art:Decimal = to_decimal("0.0")
        service_art:Decimal = to_decimal("0.0")
        wrung = None
        qty1:int = 0
        take_it:bool = False
        post_it:bool = False
        bfast_art:int = 0
        fb_dept:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        contcode:str = ""
        ct:str = ""
        prcode:int = 0
        f_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        fcost:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        nett_lamt:Decimal = to_decimal("0.0")
        gross_lamt:Decimal = to_decimal("0.0")
        tnett_lamt:Decimal = to_decimal("0.0")
        nett_lserv:Decimal = to_decimal("0.0")
        nett_ltax:Decimal = to_decimal("0.0")
        nett_famt:Decimal = to_decimal("0.0")
        nett_fserv:Decimal = to_decimal("0.0")
        nett_ftax:Decimal = to_decimal("0.0")
        price_decimal:int = 0
        argtnr:int = 0
        rguest = None
        tot_fbreakfast:Decimal = to_decimal("0.0")
        tot_flunch:Decimal = to_decimal("0.0")
        tot_fdinner:Decimal = to_decimal("0.0")
        tot_fother:Decimal = to_decimal("0.0")
        tot_lbreakfast:Decimal = to_decimal("0.0")
        tot_llunch:Decimal = to_decimal("0.0")
        tot_ldinner:Decimal = to_decimal("0.0")
        tot_lother:Decimal = to_decimal("0.0")
        tmp_bezeich:str = ""
        Wrung =  create_buffer("Wrung",Waehrung)
        Rguest =  create_buffer("Rguest",Guest)

        htparam = get_cache (Htparam, {"paramnr": 125}, ['finteger', 'flogical', 'fdecimal', '_recid'])

        if htparam:
            bfast_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": 126}, ['finteger', 'flogical', 'fdecimal', '_recid'])

        if htparam:
            fb_dept = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": 227}, ['finteger', 'flogical', 'fdecimal', '_recid'])

        if htparam:
            lunch_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": 228}, ['finteger', 'flogical', 'fdecimal', '_recid'])

        if htparam:
            dinner_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": 229}, ['finteger', 'flogical', 'fdecimal', '_recid'])

        if htparam:
            lundin_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": bfast_art, "departement": fb_dept}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

        if not artikel and bfast_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": lunch_art, "departement": fb_dept}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

        if not artikel and lunch_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": dinner_art, "departement": fb_dept}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

        if not artikel and dinner_art != 0:

            return

        artikel = get_cache (Artikel, {"zwkum": lundin_art, "departement": fb_dept}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

        if not artikel and lundin_art != 0:

            return
        qty1 = res_line.zimmeranz
        rmrate =  to_decimal(res_line.zipreis)
        bill_date = datum

        wrung = get_cache (Waehrung, {"waehrungsnr": res_line.betriebsnr}, ['ankauf', 'einheit', '_recid'])

        if wrung:
            exrate =  to_decimal(wrung.ankauf) / to_decimal(wrung.einheit)
        else:
            exrate =  to_decimal("1")

        if res_line.resstatus == 6 and res_line.reserve_dec > 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:
            frate =  to_decimal(exrate)

        guest_pr = get_cache (Guest_pr, {"gastnr": res_line.gastnr}, ['code', '_recid'])

        arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

        if arrangement:
            service =  to_decimal("0")
            vat =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": arrangement.argt_artikelnr, "departement": 0}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

            if artikel:
                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                fixed_rate = True
                rmrate =  to_decimal(reslin_queasy.deci1)

                if reslin_queasy.number3 != 0:
                    gpax = reslin_queasy.number3

                if reslin_queasy.char1 != "":

                    arrangement = get_cache (Arrangement, {"arrangement": reslin_queasy.char1}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

                    if arrangement:
                        argtnr = arrangement.argtnr

            if not fixed_rate:

                if not it_exist:

                    if guest_pr:

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 18) & (Queasy.number1 == res_line.reserve_int)).first()

                        if queasy and queasy.logi3:
                            bill_date = res_line.ankunft

                        if new_contrate:
                            rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, guest_pr.code, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                        else:
                            rmrate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                            if it_exist:
                                rate_found = True

                            if curr_i != 0:

                                if not it_exist and bonus_array[curr_i - 1] :
                                    rmrate =  to_decimal("0")

                    if not rate_found:
                        w_day = wd_array[get_weekday(bill_date) - 1]

                        if (bill_date == curr_date) or (bill_date == res_line.ankunft):
                            rmrate =  to_decimal(res_line.zipreis)

                            katpreis = db_session.query(Katpreis).filter(
                                     (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                            if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rmrate:
                                rack_rate = True

                        elif rack_rate:

                            katpreis = db_session.query(Katpreis).filter(
                                     (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                            if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                rmrate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                        if curr_i != 0:

                            if bonus_array[curr_i - 1] :
                                rmrate =  to_decimal("0")
            tot_rmrev =  to_decimal(rmrate)


            contcode = ""

            rguest = db_session.query(Rguest).filter(
                     (Rguest.gastnr == res_line.gastnr)).first()

            if res_line.reserve_int != 0:
                if rguest:
                    guest_pr = get_cache (Guest_pr, {"gastnr": rguest.gastnr}, ['code', '_recid'])

            if guest_pr:
                contcode = guest_pr.code
                ct = res_line.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

                if new_contrate:
                    prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, datum))
                else:

                    pricecod = db_session.query(Pricecod).filter(
                             (func.lower(Pricecod.code) == (contcode).lower()) & (Pricecod.marknr == res_line.reserve_int) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == curr_zikatnr) & (datum >= Pricecod.startperiode) & (datum <= Pricecod.endperiode)).first()

                    if pricecod:
                        prcode = pricecod._recid
        gross_lamt =  to_decimal("0")

        if argtnr == 0:
            tmp_bezeich = res_line.arrangement

        arrangement = get_cache (Arrangement, {"arrangement": tmp_bezeich}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

        if arrangement:
            argtnr = arrangement.argtnr
        else:
            argtnr = 0

        arrangement = get_cache (Arrangement, {"argtnr": argtnr}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

        if arrangement:

            argt_line_obj_list = {}
            argt_line = Argt_line()
            artikel = Artikel()
            for argt_line._recid, argt_line.betriebsnr, argt_line.betrag, argt_line.argtnr, artikel.departement, artikel.artnr, artikel.service_code, artikel.mwst_code, artikel.umsatzart, artikel._recid in db_session.query(Argt_line._recid, Argt_line.betriebsnr, Argt_line.betrag, Argt_line.argtnr, Artikel.departement, Artikel.artnr, Artikel.service_code, Artikel.mwst_code, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                if argt_line_obj_list.get(argt_line._recid):
                    continue
                else:
                    argt_line_obj_list[argt_line._recid] = True


                take_it, f_betrag, argt_betrag, qty = get_argtline_rate(datum, contcode, argt_line._recid)
                service_art =  to_decimal("0")
                vat_art =  to_decimal("0")
                service_art, vat_art = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

                if take_it:
                    nett_lamt = ( to_decimal((argt_betrag)) * to_decimal(qty1) )
                    gross_lamt =  to_decimal(gross_lamt) + to_decimal(((argt_betrag)) * to_decimal(qty1) )
                    nett_lamt =  to_decimal(nett_lamt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )
                    tnett_lamt =  to_decimal(tnett_lamt) + to_decimal(nett_lamt)
                    nett_famt = ( to_decimal((argt_betrag)) * to_decimal(frate)) * to_decimal(qty1)
                    nett_famt =  to_decimal(nett_famt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_lbreakfast =  to_decimal(tot_lbreakfast) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fbreakfast =  to_decimal(tot_fbreakfast) + to_decimal(nett_famt)

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_llunch =  to_decimal(tot_llunch) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_flunch =  to_decimal(tot_flunch) + to_decimal(nett_famt)

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_ldinner =  to_decimal(tot_ldinner) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fdinner =  to_decimal(tot_fdinner) + to_decimal(nett_famt)

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_llunch =  to_decimal(tot_llunch) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_flunch =  to_decimal(tot_flunch) + to_decimal(nett_famt)


                    else:
                        tot_lother =  to_decimal(tot_lother) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fother =  to_decimal(tot_fother) + to_decimal(nett_famt)


        rmrate =  to_decimal(rmrate) * to_decimal(qty1)

        htparam = get_cache (Htparam, {"paramnr": 127}, ['finteger', 'flogical', 'fdecimal', '_recid'])
        rm_vat = htparam.flogical

        if rm_vat:
            rmrate =  to_decimal(rmrate) - to_decimal(gross_lamt)
            nett_rmrev =  to_decimal(rmrate) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )
            nett_service =  to_decimal(nett_rmrev) * to_decimal(service)
            nett_vat =  to_decimal(nett_rmrev) * to_decimal(vat)


        else:
            rmrate =  to_decimal(rmrate) - to_decimal(tnett_lamt)
            nett_rmrev =  to_decimal(rmrate)
            nett_service =  to_decimal(rmrate) * to_decimal(service)
            nett_vat =  to_decimal(rmrate) * to_decimal(vat)
            tot_rmrev =  to_decimal(rmrate) + to_decimal(nett_service) + to_decimal(nett_vat)


        net_breakfast =  to_decimal(tot_lbreakfast)
        net_lunch =  to_decimal(tot_llunch)
        net_dinner =  to_decimal(tot_ldinner)
        net_others =  to_decimal(tot_lother)

        if rmrate != 0:
            fnet_lodging, lnet_lodging = get_lodging(argtnr, rmrate, bill_date)

            if rm_vat:
                fnet_lodging =  to_decimal(fnet_lodging) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )
                lnet_lodging =  to_decimal(lnet_lodging) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )


        else:
            lnet_lodging =  to_decimal("0")
            fnet_lodging =  to_decimal("0")


    def get_argtline_rate(curr_date:date, contcode:str, argt_recid:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, waehrung1


        nonlocal waehrung1

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        tmp_betrag:Decimal = to_decimal("0.0")
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        argtline = get_cache (Argt_line, {"_recid": argt_recid}, ['_recid', 'betriebsnr', 'betrag', 'argtnr'])

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = res_line.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = res_line.kind1

        elif argt_line.vt_percnt == 2:
            qty = res_line.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if res_line.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (res_line.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (res_line.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:

                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                    argt_betrag =  to_decimal(res_line.zipreis) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                    f_betrag =  to_decimal(argt_betrag)
                else:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung1 = get_cache (Waehrung, {"waehrungsnr": res_line.betriebsnr}, ['ankauf', 'einheit', '_recid'])

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": argt_line.argtnr}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

            waehrung = get_cache (Waehrung, {"waehrungsnr": arrangement.betriebsnr}, ['ankauf', 'einheit', '_recid'])
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)

            if argt_betrag > 0:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)
            else:
                tmp_betrag =  -1 * to_decimal(argt_betrag)
                argt_betrag = ( to_decimal(res_line.zipreis) * to_decimal((tmp_betrag) / to_decimal(100))) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, waehrung1


        nonlocal waehrung1

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
                delta = (lfakt - res_line.ankunft).days

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


    def get_lodging(argtnr:int, zipreis:Decimal, bill_date:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, guest, reslin_queasy, queasy, katpreis, pricecod, artikel, argt_line, htparam, res_line, guest_pr, arrangement
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        flodg_betrag = to_decimal("0.0")
        llodg_betrag = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        qty:int = 0
        argt_betrag:Decimal = to_decimal("0.0")
        fargt_betrag:Decimal = to_decimal("0.0")
        add_it:bool = False
        marknr:int = 0
        tmp_bez:str = ""

        def generate_inner_output():
            return (flodg_betrag, llodg_betrag)


        if argtnr == 0:
            tmp_bez = res_line.arrangement

        arrangement = get_cache (Arrangement, {"arrangement": tmp_bez}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

        if arrangement:
            argtnr = arrangement.argtnr
        else:
            argtnr = 0

        arrangement = get_cache (Arrangement, {"argtnr": argtnr}, ['argt_artikelnr', 'argtnr', 'betriebsnr', '_recid'])

        if arrangement:
            service =  to_decimal("0")
            vat =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": arrangement.argt_artikelnr, "departement": 0}, ['departement', 'artnr', 'service_code', 'mwst_code', 'umsatzart', '_recid'])

            if artikel:

                htparam = get_cache (Htparam, {"paramnr": artikel.service_code}, ['finteger', 'flogical', 'fdecimal', '_recid'])

                if htparam and htparam.fdecimal != 0:
                    service =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = get_cache (Htparam, {"paramnr": artikel.mwst_code}, ['finteger', 'flogical', 'fdecimal', '_recid'])

                if htparam and htparam.fdecimal != 0:
                    vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = get_cache (Htparam, {"paramnr": 479}, ['finteger', 'flogical', 'fdecimal', '_recid'])

                if htparam.flogical:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
                vat =  to_decimal(round (vat , 2))
        flodg_betrag =  to_decimal(zipreis)
        llodg_betrag =  to_decimal(zipreis) * to_decimal(frate)
        llodg_betrag =  to_decimal(round (llodg_betrag , price_decimal))
        flodg_betrag =  to_decimal(round (flodg_betrag , price_decimal))

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": 491}, ['finteger', 'flogical', 'fdecimal', '_recid'])

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": 550}, ['finteger', 'flogical', 'fdecimal', '_recid'])

    if htparam:

        if htparam.feldtyp == 4:
            new_contrate = htparam.flogical

    res_line = get_cache (Res_line, {"_recid": recid_resline}, ['zimmeranz', 'zipreis', 'betriebsnr', 'reserve_dec', 'gastnr', 'arrangement', 'resnr', 'reslinnr', 'reserve_int', 'ankunft', 'abreise', 'zikatnr', 'erwachs', 'kind1', 'kind2', 'zimmer_wunsch', 'l_zuordnung', '_recid'])

    if res_line:
        calc_lodging2()

    return rb_generate_output()





def ratecode_rate(ebdisc_flag:bool, kbdisc_flag:bool, resnr:int, reslinnr:int, prcode:str, crdate:date, datum:date, ankunft:date, abreise:date, marknr:int, argtno:int, rmcatno:int, adult:int, child1:int, child2:int, res_exrate:Decimal, wahrno:int):

    prepare_cache ([Htparam, Res_line, Reservation, Ratecode, Arrangement, Waehrung, Argt_line, Reslin_queasy, Kontline])

    rate_found = False
    rmrate = to_decimal("0.0")
    early_flag = False
    kback_flag = False
    occ_type:int = 0
    restricted_disc:bool = False
    exrate1:Decimal = 1
    ex2:Decimal = 1
    do_it:bool = False
    add_it:bool = False
    ebdisc_found:bool = False
    kbdisc_found:bool = False
    argt_defined:bool = False
    qty:int = 0
    compno:int = 0
    niteno:int = 0
    book_date:date = None
    ci_date:date = None
    fdatum:date = None
    tdatum:date = None
    ct:str = ""
    orig_prcode:str = ""
    rmocc:Decimal = -1
    avrgrate_option:bool = False
    stay_nites:int = 0
    bonus_nites:int = 0
    bonus:bool = False
    n:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    queasy = ratecode = argt_line = reslin_queasy = zimmer = res_line = kontline = htparam = reservation = arrangement = waehrung = None

    early_discount = kickback_discount = stay_pay = kbuff = ebuff = None

    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":Decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date, "flag":bool}, {"from_date": None, "to_date": None})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":Decimal, "max_days":int, "min_stay":int, "max_occ":int, "flag":bool})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

    Kbuff = Kickback_discount
    kbuff_list = kickback_discount_list

    Ebuff = Early_discount
    ebuff_list = early_discount_list

    db_session = local_storage.db_session

    def rr_generate_output():
        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, queasy, ratecode, argt_line, reslin_queasy, zimmer, res_line, kontline, htparam, reservation, arrangement, waehrung
        nonlocal ebdisc_flag, kbdisc_flag, resnr, reslinnr, prcode, crdate, datum, ankunft, abreise, marknr, argtno, rmcatno, adult, child1, child2, res_exrate, wahrno
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list

        return {"rate_found": rate_found, "rmrate": rmrate, "early_flag": early_flag, "kback_flag": kback_flag}

    def calc_occupancy():

        nonlocal rate_found, rmrate, early_flag, kback_flag, occ_type, restricted_disc, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, compno, niteno, book_date, ci_date, fdatum, tdatum, ct, orig_prcode, rmocc, avrgrate_option, stay_nites, bonus_nites, bonus, n, w_day, wd_array, queasy, ratecode, argt_line, reslin_queasy, zimmer, res_line, kontline, htparam, reservation, arrangement, waehrung
        nonlocal ebdisc_flag, kbdisc_flag, resnr, reslinnr, prcode, crdate, datum, ankunft, abreise, marknr, argtno, rmcatno, adult, child1, child2, res_exrate, wahrno
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list

        zim100:int = 0
        curr_date:date = None
        from_date:date = None
        to_date:date = None
        totocc:Decimal = to_decimal("0.0")
        minocc:Decimal = 1000
        maxocc:Decimal = to_decimal("0.0")

        if rmocc >= 0:

            return

        if ankunft == abreise:
            rmocc =  to_decimal("100")

            return

        if occ_type == 1:
            from_date = datum
            to_date = datum
        else:
            from_date = ankunft
            to_date = abreise - timedelta(days=1)

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            zim100 = zim100 + 1
        for curr_date in date_range(from_date,to_date) :
            rmocc =  to_decimal("0")

            res_line = Res_line()
            for res_line.reslinnr, res_line.zinr, res_line.zimmeranz, res_line.zipreis, res_line.zimmer_wunsch, res_line._recid in db_session.query(Res_line.reslinnr, Res_line.zinr, Res_line.zimmeranz, Res_line.zipreis, Res_line.zimmer_wunsch, Res_line._recid).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (not_ (Res_line.ankunft > curr_date)) & (not_ (Res_line.abreise <= curr_date)) & (Res_line.gastnr > 0) & (Res_line.kontignr >= 0)).order_by(Res_line._recid).all():

                if res_line.resnr != resnr or res_line.reslinnr != reslinnr:

                    if res_line.zinr != "":

                        zimmer = db_session.query(Zimmer).filter(
                                 (Zimmer.zinr == res_line.zinr)).first()

                        if zimmer.sleeping:
                            rmocc =  to_decimal(rmocc) + to_decimal(res_line.zimmeranz)
                    else:
                        rmocc =  to_decimal(rmocc) + to_decimal(res_line.zimmeranz)

            kontline = Kontline()
            for kontline.zimmeranz, kontline._recid in db_session.query(Kontline.zimmeranz, Kontline._recid).filter(
                     (Kontline.betriebsnr == 1) & (Kontline.ankunft <= curr_date) & (Kontline.abreise >= curr_date) & (Kontline.kontstatus == 1)).order_by(Kontline._recid).all():
                rmocc =  to_decimal(rmocc) + to_decimal(kontline.zimmeranz)

            if minocc > rmocc:
                minocc =  to_decimal(rmocc)

            if maxocc < rmocc:
                maxocc =  to_decimal(rmocc)
            totocc =  to_decimal(totocc) + to_decimal(rmocc)

        if occ_type == 0:
            rmocc =  to_decimal(totocc) / to_decimal((1) + to_decimal(to_date) - to_decimal(from_date)) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 1:
            rmocc =  to_decimal(rmocc) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 2:
            rmocc =  to_decimal(minocc) / to_decimal(zim100) * to_decimal("100")

        elif occ_type == 3:
            rmocc =  to_decimal(maxocc) / to_decimal(zim100) * to_decimal("100")


    htparam = get_cache (Htparam, {"paramnr": 933}, ['flogical', 'finteger', 'fdate', '_recid'])

    if htparam.feldtyp == 4:
        avrgrate_option = htparam.flogical
    pass

    if resnr > 0:

        res_line = get_cache (Res_line, {"resnr": resnr, "reslinnr": reslinnr}, ['reslinnr', 'zinr', 'zimmeranz', 'zipreis', 'zimmer_wunsch', '_recid'])
    orig_prcode = prcode

    if substring(prcode, 0, 1) == ("!").lower() :
        prcode = substring(prcode, 1)

    if res_line:
        rmrate =  to_decimal(res_line.zipreis)

        if substring(orig_prcode, 0, 1) != ("!").lower() :
            ct = res_line.zimmer_wunsch

            if matches(ct,r"*$CODE$*"):
                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                prcode = substring(ct, 0, get_index(ct, ";") - 1)

    htparam = get_cache (Htparam, {"paramnr": 549}, ['flogical', 'finteger', 'fdate', '_recid'])
    occ_type = htparam.finteger

    if crdate == None and res_line:
        n = 0

        if matches(res_line.zimmer_wunsch,r"*DATE,*"):
            n = get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            ct = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            crdate = date_mdy(to_int(substring(ct, 4, 2)) , to_int(substring(ct, 6, 2)) , to_int(substring(ct, 0, 4)))
        else:

            reservation = get_cache (Reservation, {"resnr": resnr}, ['resdat', '_recid'])
            crdate = reservation.resdat

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 18) & (Queasy.number1 == marknr)).first()

    if queasy and queasy.logi3:
        datum = ankunft
    w_day = wd_array[get_weekday(datum) - 1]

    if argtno != 0:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult)).first()

        if not ratecode:

            return rr_generate_output()
        rate_found = True
    else:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult)).first()

        if not ratecode:

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == marknr) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult)).first()

        if not ratecode:

            return rr_generate_output()
        rate_found = True

    if (num_entries(ratecode.char1[2], ";") >= 2):

        if not avrgrate_option and res_line:
            bonus = get_output(ratecode_compli(resnr, reslinnr, prcode, rmcatno, datum))

            if bonus:
                rmrate =  to_decimal("0")

                return rr_generate_output()
    rmrate =  to_decimal(ratecode.zipreis) + to_decimal(child1) * to_decimal(ratecode.ch1preis) + to_decimal(child2) * to_decimal(ratecode.ch2preis)

    if rmrate <= 0.1:
        rmrate =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": 87}, ['flogical', 'finteger', 'fdate', '_recid'])
    ci_date = htparam.fdate
    book_date = crdate

    arrangement = get_cache (Arrangement, {"argtnr": argtno}, ['betriebsnr', 'argtnr', '_recid'])

    waehrung = get_cache (Waehrung, {"waehrungsnr": arrangement.betriebsnr}, ['ankauf', 'einheit', '_recid'])

    if waehrung:
        exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if res_exrate != 0:
        ex2 =  to_decimal(ex2) / to_decimal(res_exrate)
    else:

        waehrung = get_cache (Waehrung, {"waehrungsnr": wahrno}, ['ankauf', 'einheit', '_recid'])

        if waehrung:
            ex2 = ( to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit))

    if arrangement:

        argt_line = Argt_line()
        for argt_line.betriebsnr, argt_line.departement, argt_line.argtnr, argt_line.argt_artnr, argt_line.betrag, argt_line._recid in db_session.query(Argt_line.betriebsnr, Argt_line.departement, Argt_line.argtnr, Argt_line.argt_artnr, Argt_line.betrag, Argt_line._recid).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind1) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            add_it = False

            if argt_line.vt_percnt == 0:

                if argt_line.betriebsnr == 0:
                    qty = adult
                else:
                    qty = argt_line.betriebsnr

            elif argt_line.vt_percnt == 1:
                qty = child1

            elif argt_line.vt_percnt == 2:
                qty = child2

            if qty > 0:

                if argt_line.fakt_modus == 1:
                    add_it = True

                elif argt_line.fakt_modus == 2:

                    if ankunft == datum:
                        add_it = True

                elif argt_line.fakt_modus == 3:

                    if (ankunft + 1) == datum:
                        add_it = True

                elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                    add_it = True

                elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                    add_it = True

                elif argt_line.fakt_modus == 6:

                    if (ankunft + (argt_line.intervall - 1)) >= datum:
                        add_it = True

                if add_it:
                    argt_defined = False

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                    if reslin_queasy:
                        argt_defined = True

                        if argt_line.vt_percnt == 0:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                        elif argt_line.vt_percnt == 1:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                        elif argt_line.vt_percnt == 2:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                    if not argt_defined:

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (prcode).lower()) & (Reslin_queasy.number1 == marknr) & (Reslin_queasy.number2 == argtno) & (Reslin_queasy.reslinnr == rmcatno) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum)).first()

                        if reslin_queasy:

                            if argt_line.vt_percnt == 0:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                            elif argt_line.vt_percnt == 1:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                            elif argt_line.vt_percnt == 2:
                                rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                        else:
                            rmrate =  to_decimal(rmrate) + to_decimal((argt_line.betrag) * to_decimal(qty)) * to_decimal(exrate1) / to_decimal(ex2)

    kbdisc_found = False

    if num_entries(ratecode.char1[1], ";") >= 2 and kbdisc_flag:
        for n in range(1,num_entries(ratecode.char1[1], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[1], ";")
            kbuff = Kbuff()
            kbuff_list.append(kbuff)

            kbuff.disc_rate =  to_decimal(to_int(entry(0 , ct , ","))) / to_decimal("100")
            kbuff.max_days = to_int(entry(1, ct, ","))
            kbuff.min_stay = to_int(entry(2, ct, ","))
            kbuff.max_occ = to_int(entry(3, ct, ","))

        for kbuff in query(kbuff_list, sort_by=[("max_occ",False)]):
            add_it = True

            if kbuff.max_days > 0:
                add_it = (ankunft - crdate) <= kbuff.max_days

            if add_it and kbuff.min_stay > 0:
                add_it = (abreise - ankunft) >= kbuff.min_stay

            if add_it and kbuff.max_occ > 0:
                calc_occupancy()
                add_it = rmocc <= kbuff.max_occ

            if add_it:
                kbdisc_found = True
                kbuff.flag = True

                if not restricted_disc:
                    restricted_disc = (kbuff.max_days > 0) or (kbuff.min_stay > 0) or (kbuff.max_occ > 0)
                break
    ebdisc_found = False

    if num_entries(ratecode.char1[0], ";") >= 2 and ebdisc_flag:
        for n in range(1,num_entries(ratecode.char1[0], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[0], ";")
            ebuff = Ebuff()
            ebuff_list.append(ebuff)

            ebuff.disc_rate =  to_decimal(to_int(entry(0 , ct , ","))) / to_decimal("100")
            ebuff.min_days = to_int(entry(1, ct, ","))
            ebuff.min_stay = to_int(entry(2, ct, ","))
            ebuff.max_occ = to_int(entry(3, ct, ","))

            if num_entries(ct, ",") >= 5 and trim(entry(4, ct, ",")) != "":
                ebuff.from_date = date_mdy(to_int(substring(entry(4, ct, ",") , 4, 2)) , to_int(substring(entry(4, ct, ",") , 6, 2)) , to_int(substring(entry(4, ct, ",") , 0, 4)))

            if num_entries(ct, ",") >= 6 and trim(entry(5, ct, ",")) != "":
                ebuff.to_date = date_mdy(to_int(substring(entry(5, ct, ",") , 4, 2)) , to_int(substring(entry(5, ct, ",") , 6, 2)) , to_int(substring(entry(5, ct, ",") , 0, 4)))

        for ebuff in query(ebuff_list, sort_by=[("from_date",False),("to_date",False),("max_occ",False)]):
            add_it = True

            if ebuff.from_date != None:
                add_it = book_date >= ebuff.from_date and book_date <= ebuff.to_date

            if add_it and ebuff.min_days > 0:
                add_it = (ankunft - crdate) >= ebuff.min_days

            if add_it and ebuff.min_stay > 0:
                add_it = (abreise - ankunft) >= ebuff.min_stay

            if add_it and ebuff.max_occ > 0:
                calc_occupancy()
                add_it = rmocc <= ebuff.max_occ

            if add_it:
                ebdisc_found = True
                ebuff.flag = True

                if not restricted_disc:
                    restricted_disc = (ebuff.min_days > 0) or (ebuff.max_occ > 0)
                break

    if kbdisc_found:

        kbuff = query(kbuff_list, filters=(lambda kbuff: kbuff.flag), first=True)
        rmrate =  to_decimal(rmrate) * to_decimal((1) - to_decimal(kbuff.disc_rate) / to_decimal(100))
        kback_flag = True

    if ebdisc_found:

        ebuff = query(ebuff_list, filters=(lambda ebuff: ebuff.flag), first=True)
        rmrate =  to_decimal(rmrate) * to_decimal((1) - to_decimal(ebuff.disc_rate) / to_decimal(100))
        early_flag = True
    early_flag = restricted_disc

    if kbdisc_found or ebdisc_found:

        if rmrate >= 10000:
            rmrate = to_decimal(round(rmrate + 0.49 , 0))
        else:
            rmrate = to_decimal(round(rmrate + 0.0049 , 2))

    if not avrgrate_option:

        return rr_generate_output()

    stay_pay = query(stay_pay_list, first=True)

    if not stay_pay:

        return rr_generate_output()
    stay_nites = (abreise - ankunft).days

    for stay_pay in query(stay_pay_list, filters=(lambda stay_pay: stay_pay.stay_nites >= stay_pay.stay), sort_by=[("stay",True)]):
        bonus_nites = stay_pay.stay - stay_pay.pay
        rmrate =  to_decimal(rmrate) * to_decimal((stay_nites) - to_decimal(bonus_nites)) / to_decimal(stay_nites)

        return rr_generate_output()

    return rr_generate_output()



def ratecode_compli(resnr:int, reslinnr:int, prcode:str, rmcatno:int, datum:date):

    prepare_cache ([Htparam, Res_line, Arrangement, Ratecode])

    bonus = False
    ct:str = ""
    n:int = 0
    compno:int = 0
    niteno:int = 0
    usedcompliment:int = 0
    paidnite:int = 0
    niteofstay:int = 0
    fdatum:date = None
    tdatum:date = None
    argtno:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    ratecode = htparam = res_line = arrangement = None

    stay_pay = None

    stay_pay_list, Stay_pay = create_model("Stay_pay", {"startdate":date, "f_date":date, "t_date":date, "stay":int, "pay":int}, {"startdate": None})

    db_session = local_storage.db_session

    def rcomp_generate_output():
        nonlocal bonus, ct, n, compno, niteno, usedcompliment, paidnite, niteofstay, fdatum, tdatum, argtno, w_day, wd_array, ratecode, htparam, res_line, arrangement
        nonlocal resnr, reslinnr, prcode, rmcatno, datum


        nonlocal stay_pay
        nonlocal stay_pay_list

        return {"bonus": bonus}

    htparam = get_cache (Htparam, {"paramnr": 933}, ['flogical', '_recid'])

    if htparam.feldtyp == 4 and htparam.flogical:

        return rcomp_generate_output()

    res_line = get_cache (Res_line, {"resnr": resnr, "reslinnr": reslinnr}, ['arrangement', 'abreise', 'ankunft', 'zimmer_wunsch', 'reserve_int', 'erwachs', 'kind1', 'kind2', '_recid'])

    arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argtnr', '_recid'])
    niteofstay = (res_line.abreise - res_line.ankunft).days
    argtno = arrangement.argtnr
    w_day = wd_array[get_weekday(datum - 1) - 1]
    ct = res_line.zimmer_wunsch

    if matches(ct,r"*$CODE$*"):
        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
        prcode = substring(ct, 0, get_index(ct, ";") - 1)

    ratecode = db_session.query(Ratecode).filter(
             (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        return rcomp_generate_output()

    if datum > res_line.ankunft and (num_entries(ratecode.char1[2], ";") >= 2):
        for n in range(1,num_entries(ratecode.char1[2], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[2], ";")
            fdatum = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
            tdatum = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))

            if datum > fdatum and datum <= tdatum:
                stay_pay = Stay_pay()
                stay_pay_list.append(stay_pay)

                stay_pay.f_date = fdatum
                stay_pay.t_date = tdatum
                stay_pay.stay = to_int(entry(2, ct, ","))
                stay_pay.pay = to_int(entry(3, ct, ","))

                if res_line.ankunft < fdatum:
                    stay_pay.startdate = fdatum


                else:
                    stay_pay.startdate = res_line.ankunft

                if stay_pay.stay == stay_pay.pay:
                    stay_pay_list.remove(stay_pay)

    stay_pay = query(stay_pay_list, first=True)

    if not stay_pay:

        return rcomp_generate_output()

    for stay_pay in query(stay_pay_list, sort_by=[("stay",False)]):
        niteno = (datum - stay_pay.startDate + 1).days
        stay_pay.pay = stay_pay.pay + usedcompliment
        compno = stay_pay.stay - stay_pay.pay

        if stay_pay.stay < niteno:
            usedcompliment = usedcompliment + compno

        elif (niteofstay >= stay_pay.stay) and (niteno > stay_pay.pay):
            bonus = True
            break

    return rcomp_generate_output()


def ratecode_seek(resnr:int, reslinnr:int, prcode:str, datum:date):

    prepare_cache ([Res_line, Arrangement, Ratecode])

    s_recid = 0
    ct:str = ""
    argtno:int = 0
    rmcatno:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    tmp_date:date = None
    ratecode = res_line = arrangement = None

    db_session = local_storage.db_session

    def rseek_generate_output():
        nonlocal s_recid, ct, argtno, rmcatno, w_day, wd_array, tmp_date, ratecode, res_line, arrangement
        nonlocal resnr, reslinnr, prcode, datum

        return {"s_recid": s_recid}


    res_line = get_cache (Res_line, {"resnr": resnr, "reslinnr": reslinnr}, ['arrangement', 'zikatnr', 'zimmer_wunsch', 'reserve_int', 'erwachs', 'kind1', 'kind2', '_recid'])

    arrangement = get_cache (Arrangement, {"arrangement": res_line.arrangement}, ['argtnr', '_recid'])

    if arrangement:
        argtno = arrangement.argtnr
    rmcatno = res_line.zikatnr
    tmp_date = datum - timedelta(days=1)
    w_day = wd_array[get_weekday(tmp_date) - 1]
    ct = res_line.zimmer_wunsch

    if matches(ct,r"*$CODE$*"):
        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
        prcode = substring(ct, 0, get_index(ct, ";") - 1)

    ratecode = db_session.query(Ratecode).filter(
             (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    ratecode = db_session.query(Ratecode).filter(
             (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs) & (Ratecode.kind1 == res_line.kind1) & (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                 (func.lower(Ratecode.code) == (prcode).lower()) & (Ratecode.marknr == res_line.reserve_int) & (Ratecode.zikatnr == rmcatno) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == res_line.erwachs)).first()

    if ratecode:
        s_recid = ratecode._recid

    return rseek_generate_output()