#using conversion tools version: 1.0.0.119
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from functions.res_changesbl import res_changesbl
from functions.create_historybl import create_historybl
from functions.ratecode_rate import ratecode_rate
from functions.res_dyna_rmrate import res_dyna_rmrate
from models import Res_line, Bill, Htparam, Arrangement, Reservation, Bediener, Outorder, Zimmer, Queasy, Mealcoup, Reslin_queasy, Resplan, Zimkateg, Messages, Waehrung, Guest_pr, Guest, Res_history, Master, Brief, Segment, Sourccod, Counters, Interface, Guestseg
from functions.next_counter_for_update import next_counter_for_update

reslin_list_data, Reslin_list = create_model_like(Res_line)
res_dynarate_data, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":Decimal, "rmcat":string, "argt":string, "prcode":string, "rcode":string, "markno":int, "setup":int, "adult":int, "child":int})

def mk_resline_gobl(pvilanguage:int, accompany_tmpnr1:int, accompany_tmpnr2:int, accompany_tmpnr3:int, accompany_gastnr:int, 
                    accompany_gastnr2:int, accompany_gastnr3:int, comchild:int, rm_bcol:int, marknr:int, bill_instruct:int, 
                    restype:int, restype0:int, restype1:int, contact_nr:int, cutoff_days:int, segm__purcode:int, deposit:Decimal, 
                    limitdate:date, wechsel_str:string, origcontcode:string, groupname:string, guestname:string, main_voucher:string, 
                    resline_comment:string, mainres_comment:string, purpose_svalue:string, letter_svalue:string, segm_svalue:string, 
                    source_svalue:string, res_mode:string, prev_zinr:string, memo_zinr:string, voucherno:string, contcode:string, 
                    child_age:string, flight1:string, flight2:string, eta:string, etd:string, user_init:string, currency_changed:bool, 
                    fixed_rate:bool, grpflag:bool, memozinr_readonly:bool, group_enable:bool, init_fixrate:bool, oral_flag:bool, 
                    pickup_flag:bool, drop_flag:bool, ebdisc_flag:bool, kbdisc_flag:bool, restricted:bool, sharer:bool, coder_exist:bool, 
                    gname_chged:bool, earlyci:bool, reslin_list_data:[Reslin_list], res_dynarate_data:[Res_dynarate], tot_qty:int):

    prepare_cache ([Bill, Htparam, Arrangement, Reservation, Bediener, Outorder, Zimmer, Queasy, Mealcoup, Reslin_queasy, Resplan, Zimkateg, Waehrung, Guest_pr, Res_history, Master, Brief, Segment, Sourccod, Counters, Interface, Guestseg])

    update_kcard = False
    msg_str = ""
    waehrungnr = None
    reserve_dec = None
    dyna_rmrate = None
    accompany_tmpnr:List[int] = create_empty_list(3,0)
    ci_date:date = None
    dynarate_created:bool = False
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    max_resline:int = 0
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    source_changed:bool = False
    priscilla_active:bool = True
    lvcarea:string = "mk-resline"
    move_str:string = ""
    res_line = bill = htparam = arrangement = reservation = bediener = outorder = zimmer = queasy = mealcoup = reslin_queasy = resplan = zimkateg = messages = waehrung = guest_pr = guest = res_history = master = brief = segment = sourccod = counters = interface = guestseg = None

    res_dynarate = reslin_list = resline = bbuff = None

    Resline = create_buffer("Resline",Res_line)
    Bbuff = create_buffer("Bbuff",Bill)


    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    wechsel_str = wechsel_str.strip()
    origcontcode = origcontcode.strip()
    groupname = groupname.strip()
    guestname = guestname.strip()
    main_voucher = main_voucher.strip()
    source_svalue = source_svalue.strip()
    res_mode = res_mode.strip()
    prev_zinr = prev_zinr.strip()
    memo_zinr = memo_zinr.strip()
    voucherno = voucherno.strip()
    contcode = contcode.strip()
    child_age = child_age.strip()
    flight1 = flight1.strip()
    flight2 = flight2.strip()
    eta = eta.strip()
    etd = etd.strip()

    def generate_output():
        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff
        nonlocal res_dynarate, reslin_list, resline, bbuff

        return {"update_kcard": update_kcard, "msg_str": msg_str, "waehrungnr": waehrungnr, "reserve_dec": reserve_dec, "dyna_rmrate": dyna_rmrate, "tot_qty": tot_qty}

    def static_ratecode_rates():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        to_date:date = None
        bill_date:date = None
        curr_zikatnr:int = 0
        early_flag:bool = False
        kback_flag:bool = False
        rate_found:bool = False
        rm_rate:Decimal = to_decimal("0.0")

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if reslin_queasy:

            return

        if reslin_list.ankunft == reslin_list.abreise:
            to_date = reslin_list.abreise
        else:
            to_date = reslin_list.abreise - timedelta(days=1)
        curr_zikatnr = reslin_list.zikatnr

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        for bill_date in date_range(reslin_list.ankunft,to_date) :
            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, origcontcode, None, bill_date, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

            if rate_found:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = reslin_list.resnr
                reslin_queasy.reslinnr = reslin_list.reslinnr
                reslin_queasy.date1 = bill_date
                reslin_queasy.date2 = bill_date
                reslin_queasy.deci1 =  to_decimal(rm_rate)
                reslin_queasy.char2 = origcontcode
                reslin_queasy.char3 = user_init


    def min_resplan():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        curr_date:date = None
        beg_datum:date = None
        i:int = 0
        rline = None
        rpbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Rpbuff =  create_buffer("Rpbuff",Resplan)

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == reslin_list.resnr) & (Rline.reslinnr == reslin_list.reslinnr)).first()

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            curr_date = beg_datum
            while curr_date >= beg_datum and curr_date < rline.abreise:

                resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                if resplan:

                    rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})

                    if rpbuff:
                        rpbuff.anzzim[i - 1] = rpbuff.anzzim[i - 1] - rline.zimmeranz
                        pass
                        pass
                curr_date = curr_date + timedelta(days=1)


    def rmchg_ressharer(act_zinr:string, new_zinr:string):

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        curr_datum:date = None
        res_line2 = None
        rline2 = None
        rpbuff = None
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)
        Rpbuff =  create_buffer("Rpbuff",Resplan)

        res_line2 = db_session.query(Res_line2).filter(
                 (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr != "") & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 11)).first()
        while None != res_line2:

            if reslin_list.zikatnr != res_line2.zikatnr:
                for curr_datum in date_range(res_line2.ankunft,(res_line2.abreise - 1)) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line2.zikatnr)],"datum": [(eq, curr_datum)]})

                    if resplan:

                        rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})

                        if rpbuff:
                            rpbuff.anzzim[10] = rpbuff.anzzim[10] - 1
                            pass
                            pass

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, reslin_list.zikatnr)],"datum": [(eq, curr_datum)]})

                    if not resplan:
                        rpbuff = Resplan()
                        db_session.add(rpbuff)

                        rpbuff.datum = curr_datum
                        rpbuff.zikatnr = reslin_list.zikatnr


                    else:

                        rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                    rpbuff.anzzim[10] = rpbuff.anzzim[10] + 1


                    pass
                    pass

            zimmer = get_cache (Zimmer, {"zinr": [(eq, new_zinr)]})

            rline2 = db_session.query(Rline2).filter(
                         (Rline2._recid == res_line2._recid)).first()
            rline2.zinr = new_zinr
            rline2.zikatnr = reslin_list.zikatnr
            rline2.setup = zimmer.setup


            pass
            pass

            curr_recid = res_line2._recid
            res_line2 = db_session.query(Res_line2).filter(
                     (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr != "") & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 11) & (Res_line2._recid > curr_recid)).first()


    def rmchg_sharer(act_zinr:string, new_zinr:string):

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        res_recid1:int = 0
        parent_nr:int = 0
        curr_datum:date = None
        beg_datum:date = None
        end_datum:date = None
        answer:bool = False
        res_line1 = None
        res_line2 = None
        rline2 = None
        new_zkat = None
        rpbuff = None
        mbuff = None
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)
        New_zkat =  create_buffer("New_zkat",Zimkateg)
        Rpbuff =  create_buffer("Rpbuff",Resplan)
        Mbuff =  create_buffer("Mbuff",Messages)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, new_zinr)]})

        if not zimmer:

            return

        new_zkat = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        beg_datum = htparam.fdate
        end_datum = beg_datum
        res_recid1 = 0

        messages = get_cache (Messages, {"zinr": [(eq, act_zinr)],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(ge, 1)]})
        while None != messages:

            mbuff = db_session.query(Mbuff).filter(
                     (Mbuff._recid == messages._recid)).first()
            mbuff.zinr = new_zinr
            pass
            pass

            curr_recid = messages._recid
            messages = db_session.query(Messages).filter(
                     (Messages.zinr == (act_zinr).lower()) & (Messages.resnr == reslin_list.resnr) & (Messages.reslinnr >= 1) & (Messages._recid > curr_recid)).first()

        for res_line1 in db_session.query(Res_line1).filter(
                 (Res_line1.resnr == resnr) & (Res_line1.zinr == (act_zinr).lower()) & (Res_line1.resstatus == 13)).order_by(Res_line1._recid).all():

            if end_datum <= res_line1.abreise:
                res_recid1 = res_line1._recid
                end_datum = res_line1.abreise

        if res_line.resstatus == 6 and res_recid1 == 0:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})

            if zimmer:
                pass
                zimmer.zistatus = 2
                pass
                pass

        if res_line.resstatus == 6 and res_recid1 != 0:

            res_line1 = db_session.query(Res_line1).filter(
                     (Res_line1._recid == res_recid1)).first()

            res_line2 = db_session.query(Res_line2).filter(
                         (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 13) & (Res_line2.l_zuordnung[inc_value(2)] == 0)).first()
            while None != res_line2:

                if new_zkat.zikatnr != res_line2.zikatnr:
                    for curr_datum in date_range(beg_datum,(res_line2.abreise - 1)) :

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line2.zikatnr)],"datum": [(eq, curr_datum)]})

                        if resplan:

                            rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                            rpbuff.anzzim[12] = rpbuff.anzzim[12] - 1
                            pass
                            pass

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, new_zkat.zikatnr)],"datum": [(eq, curr_datum)]})

                        if not resplan:
                            rpbuff = Resplan()
                            db_session.add(rpbuff)

                            rpbuff.datum = curr_datum
                            rpbuff.zikatnr = new_zkat.zikatnr


                        else:

                            rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                        rpbuff.anzzim[12] = rpbuff.anzzim[12] + 1


                        pass
                        pass

                for bill in db_session.query(Bill).filter(
                             (Bill.resnr == reslin_list.resnr) & (Bill.parent_nr == res_line2.reslinnr)).order_by(Bill._recid).all():

                    bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                    bbuff.zinr = new_zinr
                    pass
                    pass

                rline2 = db_session.query(Rline2).filter(
                             (Rline2._recid == res_line2._recid)).first()
                rline2.zinr = new_zinr
                rline2.zikatnr = new_zkat.zikatnr
                rline2.setup = zimmer.setup


                pass
                pass

                curr_recid = res_line2._recid
                res_line2 = db_session.query(Res_line2).filter(
                             (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 13) & (Res_line2.l_zuordnung[inc_value(2)] == 0) & (Res_line2._recid > curr_recid)).first()

            res_line2 = db_session.query(Res_line2).filter(
                         (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 12)).first()
            while None != res_line2:

                rline2 = db_session.query(Rline2).filter(
                                 (Rline2._recid == res_line2._recid)).first()
                rline2.zinr = new_zinr
                rline2.zikatnr = new_zkat.zikatnr
                rline2.setup = zimmer.setup


                pass
                pass

                curr_recid = res_line2._recid
                res_line2 = db_session.query(Res_line2).filter(
                             (Res_line2.resnr == reslin_list.resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 12) & (Res_line2._recid > curr_recid)).first()

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})

            if zimmer:
                pass
                zimmer.zistatus = 2
                pass
                pass


    def update_billzinr():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        old_zinr:string = ""
        new_zinr:string = ""
        parent_nr:int = 0
        resline = None
        Resline =  create_buffer("Resline",Res_line)

        if reslin_list.zipreis > 0 and res_line.l_zuordnung[2] == 1:

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

            if not bill:
                bill = Bill()
                db_session.add(bill)

                bill.flag = 0
                bill.billnr = 1
                bill.rgdruck = 1
                bill.zinr = reslin_list.zinr
                bill.gastnr = reslin_list.gastnrpay
                bill.resnr = res_line.resnr
                bill.reslinnr = res_line.reslinnr
                bill.parent_nr = res_line.reslinnr
                bill.name = res_line.name
                bill.kontakt_nr = bediener.nr
                bill.segmentcode = reservation.segmentcode
                bill.datum = ci_date

                resline = db_session.query(Resline).filter(
                         (Resline._recid == res_line._recid)).first()

                if resline:
                    pass
                    resline.l_zuordnung[2] = 0


                    pass
                    pass
        old_zinr = res_line.zinr
        new_zinr = reslin_list.zinr

        if old_zinr.lower()  != (new_zinr).lower() :

            for bill in db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():

                bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                bbuff.zinr = new_zinr
                pass
                pass

                resline = db_session.query(Resline).filter(
                         (Resline.resnr == bill.resnr) & (Resline.reslinnr == bill.reslinnr)).first()

                if resline.resstatus == 12:
                    pass
                    resline.zinr = new_zinr
                    pass

            if res_line.active_flag == 1:

                for bill in db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 1)).order_by(Bill._recid).all():

                    bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                    bbuff.zinr = new_zinr
                    pass
                    pass

                    resline = db_session.query(Resline).filter(
                             (Resline.resnr == bill.resnr) & (Resline.reslinnr == bill.reslinnr)).first()

                    if resline.resstatus == 12:
                        pass
                        resline.zinr = new_zinr
                        pass

    def check_currency():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        waehrung1 = None
        Waehrung1 =  create_buffer("Waehrung1",Waehrung)

        if not currency_changed:

            return

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if not reslin_queasy:

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, reslin_list.gastnr)]})

            if not guest_pr:

                return

            if marknr != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

                if not queasy or (queasy and queasy.char3 == ""):

                    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})
            else:

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

            if queasy:

                if queasy.key == 18:

                    waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
                else:

                    waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:
                    waehrungnr = waehrung1.waehrungsnr
                    res_line.betriebsnr = waehrungnr

                    if reslin_list.reserve_dec != 0:
                        reserve_dec =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)
                        res_line.reserve_dec =  to_decimal(reserve_dec)


                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("No AdHoc Rates found; Currency back to : ", lvcarea, "") + waehrung1.wabkurz + chr_unicode(10)


    def add_keycard():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        maxkey:int = 2
        errcode:int = 0
        i:int = 0
        anz0:int = 0
        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 926)]})
        anz0 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 927)]})

        if htparam.finteger != 0:
            maxkey = htparam.finteger
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The Keycard has been created (Qty =", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + ") " + translateExtended ("and need to be replaced.", lvcarea, "") + chr_unicode(10)


    def res_changes():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        do_it:bool = False
        guest1 = None
        cid:string = " "
        cdate:string = " "
        heute:date = None
        zeit:int = 0
        Guest1 =  create_buffer("Guest1",Guest)

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
            res_changes0()

            return

        if res_line.ankunft != reslin_list.ankunft or res_line.abreise != reslin_list.abreise or res_line.zimmeranz != reslin_list.zimmeranz or res_line.erwachs != reslin_list.erwachs or res_line.kind1 != reslin_list.kind1 or res_line.gratis != reslin_list.gratis or res_line.zikatnr != reslin_list.zikatnr or res_line.zinr != reslin_list.zinr or res_line.arrangement != reslin_list.arrangement or res_line.zipreis != reslin_list.zipreis or reslin_list.was_status != to_int(fixed_rate) or res_line.name.lower()  != (guestname).lower()  or reservation.bemerk.lower()  != (mainres_comment).lower()  or res_line.bemerk.lower()  != (resline_comment).lower() :
            do_it = True

        if do_it:
            heute = get_current_date()
            zeit = get_current_time_in_seconds()

            if trim(res_line.changed_id) != "":
                cid = res_line.changed_id
                cdate = to_string(res_line.changed)

            elif length(res_line.reserve_char) >= 14:
                cid = substring(res_line.reserve_char, 13)
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "ResChanges"
            reslin_queasy.resnr = reslin_list.resnr
            reslin_queasy.reslinnr = reslin_list.reslinnr
            reslin_queasy.date2 = heute
            reslin_queasy.number2 = zeit


            if earlyci:
                reslin_queasy.number1 = 1
            reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(reslin_list.zinr) + ";"

            if reslin_list.reserve_int == res_line.reserve_int:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.arrangement) + ";" + to_string(reslin_list.arrangement) + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.arrangement) + ";" + to_string(res_line.reserve_int) + ";"
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(heute) + ";" + to_string(res_line.name) + ";" + to_string(guestname) + ";"

            if reslin_list.was_status == 0:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"

            if not fixed_rate:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"
            pass
            pass

            if (reservation.bemerk.lower()  != (mainres_comment).lower()) or (res_line.bemerk.lower()  != (resline_comment).lower()):
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = heute
                res_history.zeit = zeit
                res_history.aenderung = res_line.bemerk
                res_history.action = "Remark"


                res_history.aenderung = to_string(res_line.resnr, ">>>>>>>9") + "-" + reservation.bemerk + chr_unicode(10) + res_line.bemerk + chr_unicode(10) + chr_unicode(10) + "*** Changed to:" + chr_unicode(10) + chr_unicode(10) + mainres_comment + chr_unicode(10) + resline_comment

                if bediener:
                    res_history.betriebsnr = bediener.nr
                pass


    def res_changes0():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        guest1 = None
        cid:string = " "
        cdate:string = " "
        Guest1 =  create_buffer("Guest1",Guest)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = reslin_list.resnr
        reslin_queasy.reslinnr = reslin_list.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(reslin_list.name) + ";" + to_string("New Reservation") + ";"

        if reslin_list.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"

        if not fixed_rate:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"
        pass
        pass


    def add_resplan():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        anz:int = 0
        rline = None
        rpbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Rpbuff =  create_buffer("Rpbuff",Resplan)

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == reslin_list.resnr) & (Rline.reslinnr == reslin_list.reslinnr)).first()

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            end_datum = rline.abreise - timedelta(days=1)
            curr_date = beg_datum


            for curr_date in date_range(beg_datum,end_datum) :

                resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                if not resplan:
                    rpbuff = Resplan()
                    db_session.add(rpbuff)

                    rpbuff.datum = curr_date
                    rpbuff.zikatnr = zimkateg.zikatnr


                else:

                    rpbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                rpbuff.anzzim[i - 1] = rpbuff.anzzim[i - 1] + rline.zimmeranz


                pass
                pass


    def update_mainres():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        ct:string = ""
        answer:bool = True
        l_grpnr:int = 0
        rline = None
        rgast = None
        Rline =  create_buffer("Rline",Res_line)
        Rgast =  create_buffer("Rgast",Guest)
        pass
        reservation.bemerk = mainres_comment

        if not group_enable:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 440)]})
        l_grpnr = htparam.finteger

        rgast = db_session.query(Rgast).filter(
                 (Rgast.gastnr == reslin_list.gastnr)).first()

        master = get_cache (Master, {"resnr": [(eq, reslin_list.resnr)]})

        if master and master.active:
            reservation.verstat = 1
        else:
            reservation.verstat = 0

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower() :
            reservation.useridanlage = user_init
        ct = letter_svalue

        brief = get_cache (Brief, {"briefkateg": [(eq, l_grpnr)],"briefnr": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if brief:
            reservation.briefnr = brief.briefnr
        else:
            reservation.briefnr = 0
        ct = segm_svalue

        segment = get_cache (Segment, {"segmentcode": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if segment:
            reservation.segmentcode = segment.segmentcode
        ct = source_svalue

        sourccod = get_cache (Sourccod, {"source_code": [(eq, to_int(substring(ct, 0, get_index(ct, " "))))]})

        if sourccod:
            reservation.resart = sourccod.source_code
        reservation.groupname = groupname
        reservation.grpflag = (groupname != "")
        reservation.limitdate = limitdate
        reservation.depositgef =  to_decimal(deposit)
        reservation.vesrdepot = main_voucher
        reservation.kontakt_nr = contact_nr
        reservation.point_resnr = cutoff_days

        if (reservation.insurance and not init_fixrate) or (not reservation.insurance and init_fixrate):
            reservation.insurance = init_fixrate


            resline_reserve_dec()

        if reservation.grpflag:

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == reservation.resnr)).first()
            while None != rline:
                pass
                rline.grpflag = True
                pass

                curr_recid = rline._recid
                rline = db_session.query(Rline).filter(
                         (Rline.resnr == reservation.resnr) & (Rline._recid > curr_recid)).first()

        if master:
            pass

            if not master.active:

                bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, 0)]})

                if bill and bill.saldo != 0:
                    master.active = True
            pass

            if master.active:
                reservation.verstat = 1
            else:
                reservation.verstat = 0

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == master.resnr) & (Rline.active_flag == 1)).first()

            if rline:

                bill = get_cache (Bill, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, 0)]})

                if not bill:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = reslin_list.resnr
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    bill.billtyp = 2

                    if master.rechnr != 0:
                        bill.rechnr = master.rechnr
                    else:

                        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                        counters = db_session.query(Counters).filter(
                                 (Counters.counter_no == 3)).with_for_update().first()
                        counters.counter = counters.counter + 1
                        bill.rechnr = counters.counter
                        pass
                        pass
                        master.rechnr = bill.rechnr
                        pass
                bill.gastnr = reslin_list.gastnr
                bill.name = rgast.name
                bill.segmentcode = reservation.segmentcode


                pass

        if not master and (rgast.karteityp == 1 or rgast.karteityp == 2) and res_mode.lower()  != ("qci").lower()  and rgast.gastnr != ind_gastnr and rgast.gastnr != wig_gastnr:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 166)]})

            if htparam.flogical:
                msg_str = msg_str + chr_unicode(2) + "&Q" +\
                    translateExtended ("Master Bill does not exist, CREATE IT?", lvcarea, "") +\
                    chr_unicode(10)


    def update_resline():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        hh:int = 0
        mm:int = 0
        n:int = 0
        st:string = ""
        ct:string = ""
        memormno:string = ""
        datum:date = None
        curr_zikatnr:int = 0
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        rmrate:Decimal = None
        qsy = None
        resline = None
        rline = None
        accguest = None
        ratecode_date:date = None
        b_receiver = None
        Qsy =  create_buffer("Qsy",Queasy)
        Resline =  create_buffer("Resline",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Accguest =  create_buffer("Accguest",Guest)

        if res_mode.lower()  == ("modify").lower()  and res_line.resstatus == 3 and (reslin_list.resstatus <= 2 or reslin_list.resstatus == 5):
            check_vhponline_conf_email()

        if accompany_gastnr > 0 or accompany_tmpnr[0] > 0:

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.gastnrmember == accompany_gastnr) & (Resline.l_zuordnung[inc_value(2)] == 1)).first()

            if not resline:

                for resline in db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr)).order_by(Resline._recid).all():

                    if resline.reslinnr > max_resline:
                        max_resline = resline.reslinnr
                max_resline = max_resline + 1

                if accompany_gastnr > 0:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_gastnr)).first()
                else:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_tmpnr[0])).first()
                resline = Res_line()
                db_session.add(resline)

                resline.resnr = reslin_list.resnr
                resline.reslinnr = max_resline
                resline.gastnr = reslin_list.gastnr
                resline.gastnrpay = accompany_gastnr
                resline.gastnrmember = accompany_gastnr
                resline.erwachs = 0
                resline.zimmeranz = 1
                resline.l_zuordnung[2] = 1
                resline.kontakt_nr = reslin_list.reslinnr
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.reserve_char = to_string(get_year(get_current_date()) - 2000, "99") + "/" +\
                        to_string(get_month(get_current_date()) , "99") + "/" +\
                        to_string(get_day(get_current_date()) , "99") +\
                        to_string(get_current_time_in_seconds(), "hh:mm") + user_init

                if accompany_gastnr == 0:
                    resline.gastnrpay = accompany_tmpnr[0]
                    resline.gastnrmember = accompany_tmpnr[0]

                if res_mode.lower()  == ("inhouse").lower() :
                    resline.cancelled_id = user_init
                    resline.ankzeit = get_current_time_in_seconds()
                    resline.resstatus = 13


                else:
                    resline.resstatus = 11
                pass
                accompany_vip()

            elif (resline.gastnrmember != accompany_tmpnr[0]) and (accompany_tmpnr[0] > 0):

                accguest = db_session.query(Accguest).filter(
                         (Accguest.gastnr == accompany_tmpnr[0])).first()
                pass
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.gastnrpay = accompany_tmpnr[0]
                resline.gastnrmember = accompany_tmpnr[0]


                accompany_vip()
                pass

        if accompany_gastnr2 > 0 or accompany_tmpnr[1] > 0:

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.gastnrmember == accompany_gastnr2) & (Resline.l_zuordnung[inc_value(2)] == 1)).first()

            if not resline:

                for resline in db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr)).order_by(Resline._recid).all():

                    if resline.reslinnr > max_resline:
                        max_resline = resline.reslinnr
                max_resline = max_resline + 1

                if accompany_gastnr2 > 0:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_gastnr2)).first()
                else:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_tmpnr[1])).first()
                resline = Res_line()
                db_session.add(resline)

                resline.resnr = reslin_list.resnr
                resline.reslinnr = max_resline
                resline.gastnr = reslin_list.gastnr
                resline.gastnrpay = accompany_gastnr2
                resline.gastnrmember = accompany_gastnr2
                resline.erwachs = 0
                resline.zimmeranz = 1
                resline.l_zuordnung[2] = 1
                resline.kontakt_nr = reslin_list.reslinnr
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.reserve_char = to_string(get_year(get_current_date()) - 2000, "99") + "/" +\
                        to_string(get_month(get_current_date()) , "99") + "/" +\
                        to_string(get_day(get_current_date()) , "99") +\
                        to_string(get_current_time_in_seconds(), "hh:mm") + user_init

                if accompany_gastnr2 == 0:
                    resline.gastnrpay = accompany_tmpnr[1]
                    resline.gastnrmember = accompany_tmpnr[1]

                if res_mode.lower()  == ("inhouse").lower() :
                    resline.cancelled_id = user_init
                    resline.ankzeit = get_current_time_in_seconds()
                    resline.resstatus = 13


                else:
                    resline.resstatus = 11
                accompany_vip()
                pass

            elif (resline.gastnrmember != accompany_tmpnr[1]) and (accompany_tmpnr[1] > 0):

                accguest = db_session.query(Accguest).filter(
                         (Accguest.gastnr == accompany_tmpnr[1])).first()
                pass
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.gastnrpay = accompany_tmpnr[1]
                resline.gastnrmember = accompany_tmpnr[1]


                accompany_vip()
                pass

        if accompany_gastnr3 > 0 or accompany_tmpnr[2] > 0:

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.gastnrmember == accompany_gastnr3) & (Resline.l_zuordnung[inc_value(2)] == 1)).first()

            if not resline:

                for resline in db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr)).order_by(Resline._recid).all():

                    if resline.reslinnr > max_resline:
                        max_resline = resline.reslinnr
                max_resline = max_resline + 1

                if accompany_gastnr3 > 0:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_gastnr3)).first()
                else:

                    accguest = db_session.query(Accguest).filter(
                             (Accguest.gastnr == accompany_tmpnr[2])).first()
                resline = Res_line()
                db_session.add(resline)

                resline.resnr = reslin_list.resnr
                resline.reslinnr = max_resline
                resline.gastnr = reslin_list.gastnr
                resline.gastnrpay = accompany_gastnr3
                resline.gastnrmember = accompany_gastnr3
                resline.erwachs = 0
                resline.zimmeranz = 1
                resline.l_zuordnung[2] = 1
                resline.kontakt_nr = reslin_list.reslinnr
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.reserve_char = to_string(get_year(get_current_date()) - 2000, "99") + "/" +\
                        to_string(get_month(get_current_date()) , "99") + "/" +\
                        to_string(get_day(get_current_date()) , "99") +\
                        to_string(get_current_time_in_seconds(), "hh:mm") + user_init

                if accompany_gastnr3 == 0:
                    resline.gastnrpay = accompany_tmpnr[2]
                    resline.gastnrmember = accompany_tmpnr[2]

                if res_mode.lower()  == ("inhouse").lower() :
                    resline.cancelled_id = user_init
                    resline.ankzeit = get_current_time_in_seconds()
                    resline.resstatus = 13


                else:
                    resline.resstatus = 11
                accompany_vip()
                pass

            elif (resline.gastnrmember != accompany_tmpnr[2]) and (accompany_tmpnr[2] > 0):

                accguest = db_session.query(Accguest).filter(
                         (Accguest.gastnr == accompany_tmpnr[2])).first()
                pass
                resline.name = accguest.name + ", " + accguest.vorname1 +\
                        ", " + accguest.anrede1
                resline.gastnrpay = accompany_tmpnr[2]
                resline.gastnrmember = accompany_tmpnr[2]


                accompany_vip()
                pass

        rline = db_session.query(Rline).filter(
                 (Rline.resnr == reslin_list.resnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline.kontakt_nr == reslin_list.reslinnr)).first()
        while None != rline:

            resline = db_session.query(Resline).filter(
                     (Resline._recid == rline._recid)).first()
            resline.gastnrpay = reslin_list.gastnrpay
            resline.ankunft = reslin_list.ankunft
            resline.abreise = reslin_list.abreise
            resline.anztage = reslin_list.anztage
            resline.zikatnr = reslin_list.zikatnr
            resline.zinr = reslin_list.zinr
            resline.arrangement = reslin_list.arrangement
            resline.grpflag = grpflag
            resline.reserve_int = reslin_list.reserve_int
            resline.setup = reslin_list.setup
            resline.active_flag = reslin_list.active_flag
            resline.adrflag = reslin_list.adrflag
            resline.betriebsnr = reslin_list.betriebsnr
            resline.code = to_string(bill_instruct)
            resline.changed = ci_date
            resline.changed_id = user_init


            pass

            curr_recid = rline._recid
            rline = db_session.query(Rline).filter(
                     (Rline.resnr == reslin_list.resnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline.kontakt_nr == reslin_list.reslinnr) & (Rline._recid > curr_recid)).first()

        if purpose_svalue != "":

            queasy = get_cache (Queasy, {"key": [(eq, 143)],"char1": [(eq, entry(0, purpose_svalue, " "))]})

            if queasy:
                segm__purcode = queasy.number1


        ct = ""

        if pickup_flag:
            ct = ct + "pickup;"

        if drop_flag:
            ct = ct + "drop-passanger;"

        if ebdisc_flag:
            ct = ct + "ebdisc;"

        if kbdisc_flag:
            ct = ct + "kbdisc;"

        if restricted or dynarate_created:
            ct = ct + "restricted;"
        for n in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
            st = entry(n - 1, reslin_list.zimmer_wunsch, ";")

            if st.lower()  == ("ebdisc").lower() :
                pass

            elif st.lower()  == ("kbdisc").lower() :
                pass

            elif st.lower()  == ("restricted").lower() :
                pass

            elif substring(st, 0, 7) == ("voucher").lower() :
                pass

            elif substring(st, 0, 5) == ("ChAge").lower() :
                pass

            elif substring(st, 0, 10) == ("$origcode$").lower() :
                pass

            elif substring(st, 0, 6) == ("$CODE$").lower() :
                pass

            elif substring(st, 0, 8) == ("segm_pur").lower() :
                pass

            elif substring(st, 0, 6) == ("pickup").lower() :
                pass

            elif substring(st, 0, 14) == ("drop-passanger").lower() :
                pass

            elif trim(st) == "":
                pass
            else:
                ct = ct + st + ";"

        if segm__purcode != 0:
            ct = ct + "SEGM_PUR" + to_string(segm__purcode) + ";"

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.reslinnr != res_line.reslinnr) & (Resline.active_flag <= 1) & (Resline.resstatus != 12) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
            while None != resline:

                if not matches(resline.zimmer_wunsch,r"*SEGM_PUR*"):

                    rline = db_session.query(Rline).filter(
                             (Rline._recid == resline._recid)).first()

                    if rline:
                        rline.zimmer_wunsch = rline.zimmer_wunsch +\
                                "SEGM_PUR" + to_string(segm__purcode) + ";"


                    pass

                curr_recid = resline._recid
                resline = db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr) & (Resline.reslinnr != res_line.reslinnr) & (Resline.active_flag <= 1) & (Resline.resstatus != 12) & (Resline.l_zuordnung[inc_value(2)] == 0) & (Resline._recid > curr_recid)).first()

        if not pickup_flag and matches(res_line.zimmer_wunsch,r"*pickup*"):
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line.resnr
            res_history.reslinnr = res_line.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Pickup"


            res_history.aenderung = "Pickup has been removed."

        if not drop_flag and matches(res_line.zimmer_wunsch,r"*drop-passanger*"):
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line.resnr
            res_history.reslinnr = res_line.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Drop"


            res_history.aenderung = "DROP Guest has been removed."

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
            ct = ct + "DATE," + to_string(get_year(ci_date)) + to_string(get_month(ci_date) , "99") + to_string(get_day(ci_date) , "99") + ";"

        if voucherno != "":
            ct = ct + "voucher"
            for n in range(1,length(voucherno)  + 1) :

                if substring(voucherno, n - 1, 1) == (";").lower() :
                    ct = ct + ","
                else:
                    ct = ct + substring(voucherno, n - 1, 1)
            ct = ct + ";"

        if child_age != "":
            ct = ct + "ChAge"
            for n in range(1,length(child_age)  + 1) :

                if substring(child_age, n - 1, 1) == (";").lower() :
                    ct = ct + ","
                else:
                    ct = ct + substring(child_age, n - 1, 1)
            ct = ct + ";"

        if reslin_list.ankunft >= ci_date:
            ratecode_date = reslin_list.ankunft
        else:
            ratecode_date = ci_date

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, ratecode_date)],"date2": [(ge, ratecode_date)]})

        if reslin_queasy and reslin_queasy.char2 != "":
            contcode = reslin_queasy.char2

        if contcode != "":
            ct = ct + "$CODE$" + contcode + ";"
        ct = ct + "$origcode$" + origcontcode + ";"
        res_line.zimmer_wunsch = ct

        if not memozinr_readonly and res_line.memozinr.lower()  != ((";" + memo_zinr + ";").lower()):

            if matches(res_line.memozinr,r"*;*"):
                memormno = entry(1, res_line.memozinr, ";")
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Memo RmNo"
            res_history.aenderung = "CHG Memo RmNo " + memormno + " -> " + memo_zinr


            pass
            pass
            res_line.memozinr = ";" + memo_zinr + ";"
            res_line.memodatum = get_current_date()

        if restricted:

            if reslin_list.l_zuordnung[0] != 0:
                curr_zikatnr = reslin_list.l_zuordnung[0]
            else:
                curr_zikatnr = reslin_list.zikatnr

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, reslin_list.gastnr)]})

            if guest_pr:
                for datum in date_range(reslin_list.ankunft,(reslin_list.abreise - 1)) :

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if not reslin_queasy:
                        rate_found, rmrate, early_flag, kback_flag = get_output(ratecode_rate(True, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + guest_pr.code), datum, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

                        if rate_found:
                            reslin_queasy = Reslin_queasy()
                            db_session.add(reslin_queasy)

                            reslin_queasy.key = "arrangement"
                            reslin_queasy.resnr = reslin_list.resnr
                            reslin_queasy.reslinnr = reslin_list.reslinnr
                            reslin_queasy.date1 = datum
                            reslin_queasy.date2 = datum
                            reslin_queasy.deci1 =  to_decimal(rmrate)


                            pass

        if res_line.active_flag == 1 and res_line.zinr != reslin_list.zinr and res_line.zinr != "":

            queasy = get_cache (Queasy, {"key": [(eq, 24)],"char1": [(eq, res_line.zinr)]})
            while None != queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                qsy.char1 = reslin_list.zinr
                pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 24) & (Queasy.char1 == res_line.zinr) & (Queasy._recid > curr_recid)).first()

            resline = db_session.query(Resline).filter(
                     (Resline.active_flag == 1) & (Resline.resstatus != 12) & (Resline.zinr == res_line.zinr) & (Resline._recid != res_line._recid)).first()

            if not resline:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                zimmer.zistatus = 2


                pass
        res_line.flight_nr = to_string(flight1, "x(6)") + to_string(eta, "x(5)") + to_string(flight2, "x(6)") + to_string(etd, "x(5)")

        if res_line.abreisezeit == 0:

            if etd.lower()  != ("0000").lower() :
                hh = to_int(substring(etd, 0, 2))

                if hh > 24:
                    hh = hh - 24
                mm = to_int(substring(etd, 2, 2))

                if mm > 60:
                    mm = mm - 60
                res_line.abreisezeit = hh * 3600 + mm * 60
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 925)]})

                if htparam and htparam.fchar != "":
                    hh = to_int(entry(0, htparam.fchar, ":"))
                    mm = to_int(entry(1, htparam.fchar, ":"))
                    reslin_list.abreisezeit = (hh * 3600) + (mm * 60)
                    res_line.abreisezeit = reslin_list.abreisezeit

                elif reslin_list.abreise > reslin_list.ankunft:
                    res_line.abreisezeit = 12 * 3600

        if res_line.gastnrmember != reslin_list.gastnrmember:
            gname_chged = True
        else:
            gname_chged = False
        res_line.gastnrmember = reslin_list.gastnrmember

        if res_line.gastnrpay != reslin_list.gastnrpay and res_line.active_flag == 1:

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"zinr": [(eq, res_line.zinr)]})

            if bill:
                pass
                B_receiver =  create_buffer("B_receiver",Guest)
                bill.gastnr = reslin_list.gastnrpay

                b_receiver = db_session.query(B_receiver).filter(
                         (B_receiver.gastnr == bill.gastnr)).first()
                bill.name = b_receiver.name
                pass
                pass
        res_line.gastnrpay = reslin_list.gastnrpay
        res_line.ankunft = reslin_list.ankunft
        res_line.abreise = reslin_list.abreise
        res_line.anztage = reslin_list.anztage
        res_line.zimmeranz = reslin_list.zimmeranz
        res_line.erwachs = reslin_list.erwachs
        res_line.kind1 = reslin_list.kind1
        res_line.kind2 = reslin_list.kind2
        res_line.gratis = reslin_list.gratis
        res_line.zikatnr = reslin_list.zikatnr
        res_line.zinr = reslin_list.zinr
        res_line.arrangement = reslin_list.arrangement
        res_line.kontignr = reslin_list.kontignr
        res_line.reserve_int = reslin_list.reserve_int
        res_line.setup = reslin_list.setup
        res_line.active_flag = reslin_list.active_flag
        res_line.adrflag = reslin_list.adrflag
        res_line.betriebsnr = reslin_list.betriebsnr
        res_line.l_zuordnung[0] = reslin_list.l_zuordnung[0]
        res_line.name = guestname
        res_line.grpflag = grpflag
        res_line.code = to_string(bill_instruct)
        res_line.bemerk = resline_comment
        res_line.l_zuordnung[3] = comchild
        res_line.resstatus = reslin_list.resstatus
        res_line.zimmerfix = (res_line.resstatus == 13)
        tot_qty = tot_qty + res_line.zimmeranz

        if accompany_gastnr > 0 or accompany_tmpnr[0] > 0:
            res_line.kontakt_nr = res_line.reslinnr

        if fixed_rate:
            res_line.was_status = 1
        else:
            res_line.was_status = 0

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
            res_line.reserve_char = to_string(get_year(get_current_date()) - 2000, "99") + "/" +\
                to_string(get_month(get_current_date()) , "99") + "/" +\
                to_string(get_day(get_current_date()) , "99") +\
                to_string(get_current_time_in_seconds(), "hh:mm") + user_init


        res_line.zipreis =  to_decimal(reslin_list.zipreis)

        if res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("split").lower()  or res_mode.lower()  == ("inhouse").lower() :
            res_line.changed = ci_date
            res_line.changed_id = user_init

        if res_line.zinr != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            res_line.setup = zimmer.setup
        store_vip()
        pass

        if res_line.code != "":

            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.reslinnr != res_line.reslinnr) & (Resline.resstatus == 12) & (Resline.code == "")).first()
            while None != resline:

                rline = db_session.query(Rline).filter(
                         (Rline._recid == resline._recid)).first()

                if rline:
                    rline.code = res_line.code
                    pass
                    pass

                curr_recid = resline._recid
                resline = db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr) & (Resline.reslinnr != res_line.reslinnr) & (Resline.resstatus == 12) & (Resline.code == "") & (Resline._recid > curr_recid)).first()


    def check_vhponline_conf_email():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        htparam = get_cache (Htparam, {"paramnr": [(eq, 39)]})

        if res_line.gastnr != htparam.finteger:

            return

        interface = get_cache (Interface, {"key": [(eq, 16)],"resnr": [(eq, res_line.resnr)]})

        if interface:

            return
        interface = Interface()
        db_session.add(interface)

        interface.key = 16
        interface.resnr = res_line.resnr
        interface.intdate = get_current_date()
        interface.int_time = get_current_time_in_seconds()


        pass
        pass


    def store_vip():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        gmember = None
        Gmember =  create_buffer("Gmember",Guest)

        gmember = db_session.query(Gmember).filter(
                 (Gmember.gastnr == res_line.gastnrmember)).first()

        if gmember.karteityp != 0:

            return

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:
            res_line.betrieb_gastmem = guestseg.segmentcode
        else:
            res_line.betrieb_gastmem = 0


    def accompany_vip():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        gmember = None
        Gmember =  create_buffer("Gmember",Guest)

        resline = db_session.query(Resline).filter(
                 (Resline.resnr == reslin_list.resnr) & (Resline.reslinnr == max_resline)).first()

        if not resline:

            return

        gmember = db_session.query(Gmember).filter(
                 (Gmember.gastnr == resline.gastnrmember)).first()

        if not gmember:

            return
        pass

        if gmember.karteityp != 0:
            resline.betrieb_gastmem = 0

            return

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:
            resline.betrieb_gastmem = guestseg.segmentcode
        else:
            resline.betrieb_gastmem = 0
        pass


    def resline_reserve_dec():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        exchg_rate:Decimal = to_decimal("0.0")
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        if not reservation.insurance:

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == reservation.resnr) & ((Rline.resstatus == 6) | (Rline.resstatus == 13)) & (Rline.reserve_dec != 0)).order_by(Rline._recid).all():
                rline.reserve_dec =  to_decimal("0")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate != 0:

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == reservation.resnr) & ((Rline.resstatus == 6) | (Rline.resstatus == 13)) & (Rline.reserve_dec == 0)).order_by(Rline._recid).all():
                rline.reserve_dec =  to_decimal(exchg_rate)

    def res_dyna_rmrate():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        rmrate:Decimal = None
        arrival_date:date = None
        zikatstr:string = ""

        if origcontcode == "":

            return

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, origcontcode)]})

        if not queasy:

            return

        if not queasy.logi2:
            static_ratecode_rates()

            return

        if res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("inhouse").lower() :

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

            if reslin_queasy:

                return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, reslin_list.zikatnr)]})
        zikatstr = zimkateg.kurzbez

        res_dynarate = query(res_dynarate_data, first=True)

        if not res_dynarate:

            if not fixed_rate:
                dynarate_created, rmrate = get_output(res_dyna_rmrate(reslin_list.resnr, reslin_list.reslinnr, reslin_list.reserve_int, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.betriebsnr, arrangement.argtnr, zikatstr, reslin_list.ankunft, reslin_list.abreise, origcontcode, user_init, reslin_list.reserve_dec, ebdisc_flag, kbdisc_flag))

                if rmrate != None and rmrate != reslin_list.zipreis:
                    dyna_rmrate =  to_decimal(rmrate)


                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Room Rate has been updated.", lvcarea, "") + chr_unicode(2)
                    reslin_list.zipreis =  to_decimal(rmrate)

            return
        arrival_date = res_dynarate.date1

        res_dynarate = query(res_dynarate_data, last=True)

        if reslin_list.ankunft != arrival_date or reslin_list.abreise != res_dynarate.date2 + 1 or reslin_list.erwachs != res_dynarate.adult or reslin_list.kind1 != res_dynarate.child or reslin_list.arrangement != res_dynarate.argt or zikatstr != res_dynarate.rmcat or marknr != res_dynarate.markno:

            if reslin_list.ankunft == arrival_date and reslin_list.abreise == reslin_list.ankunft:
                pass

            elif reslin_list.gratis > 0 and reslin_list.zipreis == 0:
                pass
            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Reservation data was changed,", lvcarea, "") + chr_unicode(10) + translateExtended ("Please re-check the rates.", lvcarea, "") + chr_unicode(2)
        dynarate_created = True

        for res_dynarate in query(res_dynarate_data):

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(eq, res_dynarate.date1)],"date2": [(eq, res_dynarate.date2)]})

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = reslin_list.resnr
                reslin_queasy.reslinnr = reslin_list.reslinnr
                reslin_queasy.date1 = res_dynarate.date1
                reslin_queasy.date2 = res_dynarate.date2
                reslin_queasy.deci1 =  to_decimal(res_dynarate.rate)
                reslin_queasy.char2 = res_dynarate.prcode
                reslin_queasy.char3 = user_init


    def update_qsy171():

        nonlocal update_kcard, msg_str, waehrungnr, reserve_dec, dyna_rmrate, accompany_tmpnr, ci_date, dynarate_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, max_resline, ind_gastnr, wig_gastnr, source_changed, priscilla_active, lvcarea, move_str, res_line, bill, htparam, arrangement, reservation, bediener, outorder, zimmer, queasy, mealcoup, reslin_queasy, resplan, zimkateg, messages, waehrung, guest_pr, guest, res_history, master, brief, segment, sourccod, counters, interface, guestseg
        nonlocal pvilanguage, accompany_tmpnr1, accompany_tmpnr2, accompany_tmpnr3, accompany_gastnr, accompany_gastnr2, accompany_gastnr3, comchild, rm_bcol, marknr, bill_instruct, restype, restype0, restype1, contact_nr, cutoff_days, segm__purcode, deposit, limitdate, wechsel_str, origcontcode, groupname, guestname, main_voucher, resline_comment, mainres_comment, purpose_svalue, letter_svalue, segm_svalue, source_svalue, res_mode, prev_zinr, memo_zinr, voucherno, contcode, child_age, flight1, flight2, eta, etd, user_init, currency_changed, fixed_rate, grpflag, memozinr_readonly, group_enable, init_fixrate, oral_flag, pickup_flag, drop_flag, ebdisc_flag, kbdisc_flag, restricted, sharer, coder_exist, gname_chged, earlyci, tot_qty
        nonlocal resline, bbuff


        nonlocal res_dynarate, reslin_list, resline, bbuff

        qsy = None
        bqsy = None
        zbuff = None
        zbuff1 = None
        qsy_buff = None
        upto_date:date = None
        datum:date = None
        start_date:date = None
        i:int = 0
        iftask:string = ""
        origcode:string = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        roomnr1:int = 0
        Qsy =  create_buffer("Qsy",Queasy)
        Bqsy =  create_buffer("Bqsy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Zbuff1 =  create_buffer("Zbuff1",Zimkateg)
        Qsy_buff =  create_buffer("Qsy_buff",Queasy)

        if origcode == "":
            origcode = origcontcode

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, origcode)]})

        if queasy and origcode != "":
            do_it = True

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr

        zbuff1 = get_cache (Zimkateg, {"zikatnr": [(eq, reslin_list.zikatnr)]})

        if zbuff1:

            if cat_flag:
                roomnr1 = zbuff1.typ
            else:
                roomnr1 = zbuff1.zikatnr

        if (res_line.zikatnr != reslin_list.zikatnr) or (res_line.zimmeranz != reslin_list.zimmeranz) or (res_line.abreise != reslin_list.abreise) or (res_line.ankunft != reslin_list.ankunft):
            get_output(intevent_1(1, res_line.zinr, "DataExchange", res_line.resnr, res_line.reslinnr))

        if res_line.zikatnr != reslin_list.zikatnr:

            if res_line.ankunft == res_line.abreise:
                upto_date = res_line.abreise
            else:
                upto_date = res_line.abreise - timedelta(days=1)
            for datum in date_range(res_line.ankunft,upto_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:
                    pass
                    queasy.logi2 = True


                    pass
                    pass

                if do_it:

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True


                        pass
                        pass

            if reslin_list.ankunft == reslin_list.abreise:
                upto_date = reslin_list.abreise
            else:
                upto_date = reslin_list.abreise - timedelta(days=1)
            for datum in date_range(reslin_list.ankunft,upto_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:
                    pass
                    queasy.logi2 = True


                    pass
                    pass

                if do_it:

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True


                        pass
                        pass

        elif res_line.zikatnr == reslin_list.zikatnr:

            if res_line.resstatus != reslin_list.resstatus:

                if reslin_list.ankunft == reslin_list.abreise:
                    upto_date = reslin_list.abreise
                else:
                    upto_date = reslin_list.abreise - timedelta(days=1)
                for datum in date_range(reslin_list.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, "")]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                        if qsy:
                            qsy.logi2 = True
                            pass
                            pass

                    if do_it:

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, origcode)]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:

                            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                            if qsy:
                                qsy.logi2 = True
                                pass
                                pass

            elif res_line.ankunft == reslin_list.ankunft and res_line.abreise == reslin_list.abreise and res_line.zimmeranz == reslin_list.zimmeranz:
                pass

            elif res_line.zimmeranz != reslin_list.zimmeranz:

                if reslin_list.ankunft == reslin_list.abreise:
                    upto_date = reslin_list.abreise
                else:
                    upto_date = reslin_list.abreise - timedelta(days=1)
                for datum in date_range(reslin_list.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, "")]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True


                        pass
                        pass

                    if do_it:

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, origcode)]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

            elif res_line.ankunft == reslin_list.ankunft and res_line.abreise != reslin_list.abreise:

                if res_line.abreise > reslin_list.abreise:
                    for datum in date_range(reslin_list.abreise,res_line.abreise - 1) :

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

                        if do_it:

                            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                            if queasy and queasy.logi1 == False and queasy.logi2 == False:
                                pass
                                queasy.logi2 = True


                                pass
                                pass

                elif reslin_list.abreise > res_line.abreise:
                    for datum in date_range(res_line.abreise,reslin_list.abreise - 1) :

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

                        if do_it:

                            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                            if queasy and queasy.logi1 == False and queasy.logi2 == False:
                                pass
                                queasy.logi2 = True


                                pass
                                pass

            elif res_line.ankunft != reslin_list.ankunft and res_line.abreise == reslin_list.abreise:

                if res_line.ankunft > reslin_list.ankunft:
                    for datum in date_range(reslin_list.ankunft,res_line.ankunft - 1) :

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

                        if do_it:

                            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                            if queasy and queasy.logi1 == False and queasy.logi2 == False:
                                pass
                                queasy.logi2 = True


                                pass
                                pass

                elif reslin_list.ankunft > res_line.ankunft:
                    for datum in date_range(res_line.ankunft,reslin_list.ankunft - 1) :

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

                        if do_it:

                            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                            if queasy and queasy.logi1 == False and queasy.logi2 == False:
                                pass
                                queasy.logi2 = True


                                pass
                                pass

            elif res_line.ankunft != reslin_list.ankunft and res_line.abreise != reslin_list.abreise:

                if res_line.ankunft == res_line.abreise:
                    upto_date = res_line.abreise
                else:
                    upto_date = res_line.abreise - timedelta(days=1)
                for datum in date_range(res_line.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True


                        pass
                        pass

                    if do_it:

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass

                if reslin_list.ankunft == reslin_list.abreise:
                    upto_date = reslin_list.abreise
                else:
                    upto_date = reslin_list.abreise - timedelta(days=1)
                for datum in date_range(reslin_list.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, "")]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True


                        pass
                        pass

                    if do_it:

                        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, origcode)]})

                        if queasy and queasy.logi1 == False and queasy.logi2 == False:
                            pass
                            queasy.logi2 = True


                            pass
                            pass


    wig_gastnr = get_output(htpint(109))
    ind_gastnr = get_output(htpint(123))
    accompany_tmpnr[0] = accompany_tmpnr1
    accompany_tmpnr[1] = accompany_tmpnr2
    accompany_tmpnr[2] = accompany_tmpnr3


    ci_date = get_output(htpdate(87))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    reslin_list = query(reslin_list_data, first=True)

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, reslin_list.resnr)]})

    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if to_int(substring(source_svalue, 0, get_index(source_svalue, " "))) != reservation.resart:
        source_changed = True

    if res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("split").lower()  or res_mode.lower()  == ("inhouse").lower() :
        min_resplan()

    if res_line.betrieb_gast > 0 and res_line.zinr != "":
        update_kcard = (res_line.ankunft != reslin_list.ankunft) or (res_line.abreise != reslin_list.abreise) or (reslin_list.zinr != res_line.zinr)

    if rm_bcol != 15 and reslin_list.ankunft != res_line.ankunft and reslin_list.resstatus == 1:

        outorder = get_cache (Outorder, {"zinr": [(eq, reslin_list.zinr)],"betriebsnr": [(eq, reslin_list.resnr)]})

        if outorder:
            pass
            outorder.gespstart = reslin_list.ankunft - timedelta(days=outorder.gespende +\
                    outorder.gespstart)
            outorder.gespende = reslin_list.ankunft


            pass
            pass

    if res_mode.lower()  == ("inhouse").lower() :

        if res_line.abreise == ci_date and reslin_list.abreise > res_line.abreise and res_line.zinr == reslin_list.zinr:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if zimmer and zimmer.zistatus == 3:
                pass
                zimmer.zistatus = 4
                pass

        if res_line.zinr != reslin_list.zinr and res_line.resstatus == 6 and not sharer and not (res_line.zinr == ""):
            rmchg_sharer(res_line.zinr, reslin_list.zinr)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

            if htparam.flogical:
                get_output(intevent_1(2, res_line.zinr, "Move out", res_line.resnr, res_line.reslinnr))

        if (res_line.resstatus == 6) and not sharer and (res_line.abreise != reslin_list.abreise) and (res_line.zinr == reslin_list.zinr):

            htparam = get_cache (Htparam, {"paramnr": [(eq, 341)]})

            if htparam.fchar != "":
                get_output(intevent_1(9, res_line.zinr, "Chg DepTime!", res_line.resnr, res_line.reslinnr))

        if (res_line.resstatus == 6) and ((res_line.abreise != reslin_list.abreise) or (res_line.zinr != reslin_list.zinr) or (res_line.zikatnr != reslin_list.zikatnr) or source_changed):
            get_output(intevent_1(1, res_line.zinr, "DataExchange", res_line.resnr, res_line.reslinnr))
        update_billzinr()

    elif res_mode.lower()  == ("modify").lower() :

        if res_line.zinr != reslin_list.zinr and (res_line.resstatus <= 2 or res_line.resstatus == 5):
            rmchg_ressharer(res_line.zinr, reslin_list.zinr)

    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})
    prev_zinr = res_line.zinr
    check_currency()
    get_output(res_changesbl(pvilanguage, res_mode, guestname, mainres_comment, resline_comment, user_init, earlyci, fixed_rate, reslin_list_data))

    queasy = get_cache (Queasy, {"key": [(eq, 171)]})

    if queasy:
        update_qsy171()
    update_resline()
    res_dyna_rmrate()
    update_mainres()
    add_resplan()

    if res_mode.lower()  == ("inhouse").lower()  and (prev_zinr != res_line.zinr):

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam.flogical:
            move_str = "Move in|" + prev_zinr


            get_output(intevent_1(1, res_line.zinr, move_str, res_line.resnr, res_line.reslinnr))
        get_output(create_historybl(res_line.resnr, res_line.reslinnr, prev_zinr, "roomchg", user_init, wechsel_str))

        resline = db_session.query(Resline).filter(
                 (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.resstatus != 12) & (Resline.zinr == (prev_zinr).lower())).first()

        if not resline:

            mealcoup = get_cache (Mealcoup, {"zinr": [(eq, prev_zinr)],"activeflag": [(eq, True)]})

            if mealcoup:
                mealcoup.zinr = res_line.zinr
                pass

        if res_mode.lower()  == ("inhouse").lower()  and res_line.resstatus == 6 and gname_chged:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

            if htparam.flogical:
                get_output(intevent_1(1, res_line.zinr, "Change name", res_line.resnr, res_line.reslinnr))

            htparam = get_cache (Htparam, {"paramnr": [(eq, 359)]})

            if htparam.flogical:
                get_output(intevent_1(1, res_line.zinr, "Change name", res_line.resnr, res_line.reslinnr))

        if update_kcard:

            if coder_exist:
                add_keycard()
            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Replace the KeyCard / Qty =", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + chr_unicode(10)

    if priscilla_active and res_line.active_flag != 2 and (res_line.resstatus != 11 and res_line.l_zuordnung[2] != 1) and res_line.resstatus != 12:

        if res_mode.lower()  == ("modify").lower() :
            get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        elif res_mode.lower()  == ("qci").lower() :
            get_output(intevent_1(10, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        elif res_mode.lower()  == ("insert").lower() :
            get_output(intevent_1(11, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        elif res_mode.lower()  == ("new").lower() :
            get_output(intevent_1(12, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        elif res_mode.lower()  == ("inhouse").lower() :
            get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

    return generate_output()