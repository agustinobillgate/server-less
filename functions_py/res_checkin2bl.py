#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/7/25
# include file: res-zimplan.i, gabung di .p, konversi
#
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.post_dayuse import post_dayuse
from functions.intevent_1 import intevent_1
from functions.mk_mcoupon import mk_mcoupon
from models import Res_line, Guest, Bill, Htparam, Outorder, Reservation, Waehrung, Master, Counters, Bediener, Queasy, Artikel, Billjournal, Bill_line, Umsatz, Res_history, Reslin_queasy, Exrate, Messages, Zimplan, Zimmer, Resplan, Zimkateg

def res_checkin2bl(pvilanguage:int, resnr:int, reslinnr:int, user_init:string, silenzio:bool):

    prepare_cache ([Res_line, Guest, Bill, Htparam, Reservation, Waehrung, Master, Counters, Bediener, Artikel, Billjournal, Bill_line, Umsatz, Res_history, Reslin_queasy, Exrate, Messages, Zimmer, Resplan, Zimkateg])

    new_resstatus = 0
    checked_in = False
    ask_deposit = False
    ask_keycard = False
    ask_mcard = False
    msg_str = ""
    dummy_b:bool = False
    answer:bool = True
    res_recid:int = 0
    res_mode:string = "inhouse"
    resno:int = 0
    resline:int = 0
    exchg_rate:Decimal = 1
    price_decimal:int = 0
    double_currency:bool = False
    err_status:int = 0
    deposit:Decimal = to_decimal("0.0")
    deposit_foreign:Decimal = to_decimal("0.0")
    bill_date:date = None
    sys_id:string = ""
    it_is:bool = False
    inv_nr:int = 0
    nat_bez:string = ""
    curr_i:int = 0
    curr_st:string = ""
    curr_ct:string = ""
    mc_flag:bool = False
    mc_pos1:int = 0
    mc_pos2:int = 0
    priscilla_active:bool = True
    casenum:int = 0
    rmno:string = ""
    outstand:Decimal = to_decimal("0.0")
    passwd_ok:bool = False
    stra:string = ""
    strb:string = ""
    strc:string = ""
    bill_no:int = 0
    loopi:int = 0
    lvcarea:string = "res-checkin"
    res_line = guest = bill = htparam = outorder = reservation = waehrung = master = counters = bediener = queasy = artikel = billjournal = bill_line = umsatz = res_history = reslin_queasy = exrate = messages = zimplan = zimmer = resplan = zimkateg = None

    res_member = receiver = res_sharer = res_line1 = rline = b_receiver = buff_bill = buf_resline = bbill = art1 = None

    Res_member = create_buffer("Res_member",Res_line)
    Receiver = create_buffer("Receiver",Guest)
    Res_sharer = create_buffer("Res_sharer",Res_line)
    Res_line1 = create_buffer("Res_line1",Res_line)
    Rline = create_buffer("Rline",Res_line)
    B_receiver = create_buffer("B_receiver",Guest)
    Buff_bill = create_buffer("Buff_bill",Bill)
    Buf_resline = create_buffer("Buf_resline",Res_line)
    Bbill = create_buffer("Bbill",Bill)
    Art1 = create_buffer("Art1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        return {"new_resstatus": new_resstatus, "checked_in": checked_in, "ask_deposit": ask_deposit, "ask_keycard": ask_keycard, "ask_mcard": ask_mcard, "msg_str": msg_str}

    def generate_keycard():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1111)]})
        ask_keycard = htparam.flogical


    def check_masterbill():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        master_flag = False

        def generate_inner_output():
            return (master_flag)


        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master:
            master_flag = True

        return generate_inner_output()


    def update_mastbill():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        inv_nr = 0
        mbill = None

        def generate_inner_output():
            return (inv_nr)

        Mbill =  create_buffer("Mbill",Bill)

        mbill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})
        mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(deposit)
        mbill.rgdruck = 0
        mbill.datum = bill_date
        mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(deposit)
        mbill.mwst[98] = mbill.mwst[98] + deposit_foreign

        if mbill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters.counter = counters.counter + 1
            mbill.rechnr = counters.counter
            pass
            pass
            master.rechnr = mbill.rechnr
            pass
        inv_nr = mbill.rechnr
        pass

        return generate_inner_output()


    def calculate_deposit_amount():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        deposit_exrate:Decimal = 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel.pricetab:
            deposit =  - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)


        else:
            deposit_exrate =  to_decimal("1")

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if reservation.zahldatum == bill_date:

                if waehrung:
                    deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:

                exrate = get_cache (Exrate, {"artnr": [(eq, artikel.betriebsnr)],"datum": [(eq, reservation.zahldatum)]})

                if exrate:
                    deposit_exrate =  to_decimal(exrate.betrag)

                elif waehrung:
                    deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            deposit =  - to_decimal(reservation.depositbez) * to_decimal(deposit_exrate)

            if reservation.depositbez2 != 0:
                deposit_exrate =  to_decimal("1")

                if reservation.zahldatum == bill_date:

                    if waehrung:
                        deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                else:

                    exrate = get_cache (Exrate, {"artnr": [(eq, artikel.betriebsnr)],"datum": [(eq, reservation.zahldatum2)]})

                    if exrate:
                        deposit_exrate =  to_decimal(exrate.betrag)

                    elif waehrung:
                        deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            deposit =  to_decimal(deposit) - to_decimal(reservation.depositbez2) * to_decimal(deposit_exrate)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        deposit_foreign = to_decimal(round(deposit / exchg_rate , 2))


    def check_messages():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        messages = get_cache (Messages, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if messages:
            get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))

            if not silenzio:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Message(s) exist for this guest.", lvcarea, "") + chr_unicode(10)


    def check_midnite_checkin():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        if get_current_time_in_seconds() > 6 * 3600:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

        if htparam.fdate == get_current_date() and not silenzio:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("EARLY CHECKED-IN GUEST! POST DAY-USE FEE IF NEEDED.", lvcarea, "") + chr_unicode(10)


    def assign_zinr(resline_recid:int, ankunft:date, abreise:date, zinr:string, resstatus:int, gastnrmember:int, bemerk:string, name:string):

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        room_blocked = False
        sharer:bool = False
        curr_datum:date = None
        beg_datum:date = None
        res_recid:int = 0
        res_line1 = None
        zimplan1 = None
        resline = None
        zbuff = None

        def generate_inner_output():
            return (room_blocked)

        Res_line1 =  create_buffer("Res_line1",Res_line)
        Zimplan1 =  create_buffer("Zimplan1",Zimplan)
        resline =  create_buffer("resline",Res_line)
        Zbuff =  create_buffer("Zbuff",Zimplan)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        sharer = (resstatus == 11) or (resstatus == 13)

        if zinr != "" and not sharer:

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = htparam.fdate
            else:
                beg_datum = ankunft
            room_blocked = False
            for curr_datum in date_range(beg_datum,(abreise - 1)) :

                zimplan1 = db_session.query(Zimplan1).filter(
                         (Zimplan1.datum == curr_datum) & (Zimplan1.zinr == (zinr).lower())).first()

                if (not zimplan1) and (not room_blocked):
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = curr_datum
                    zimplan.zinr = zinr
                    zimplan.res_recid = resline_recid
                    zimplan.gastnrmember = gastnrmember
                    zimplan.bemerk = bemerk
                    zimplan.resstatus = resstatus
                    zimplan.name = name
                    pass
                    pass
                else:

                    if zimplan1 and (zimplan1.res_recid != resline_recid):

                        resline = get_cache (Res_line, {"_recid": [(eq, zimplan1.res_recid)]})

                        if resline and resline.zinr.lower()  == (zinr).lower()  and resline.active_flag < 2 and resline.ankunft <= zimplan1.datum and resline.abreise > zimplan1.datum:
                            curr_datum = abreise
                            room_blocked = True
                        else:
                            pass
                            zimplan1.res_recid = resline_recid
                            zimplan1.gastnrmember = gastnrmember
                            zimplan1.bemerk = bemerk
                            zimplan1.resstatus = resstatus
                            zimplan1.name = name
                            pass
                            pass

            if room_blocked:
                for curr_datum in date_range(beg_datum,(abreise - 1)) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_datum)],"zinr": [(eq, zinr)],"res_recid": [(eq, resline_recid)]})

                    if zimplan:

                        zbuff = db_session.query(Zbuff).filter(
                                 (Zbuff._recid == zimplan._recid)).first()
                        db_session.delete(zbuff)
                        pass
            else:

                if resstatus == 6 or resstatus == 13:

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

                    if abreise > htparam.fdate and zimmer.zistatus == 0:
                        zimmer.zistatus = 5

                    elif abreise > htparam.fdate and zimmer.zistatus == 3:
                        zimmer.zistatus = 4

                    elif abreise == htparam.fdate:

                        res_line1 = db_session.query(Res_line1).filter(
                                 (Res_line1._recid != resline_recid) & (Res_line1.abreise == abreise) & (Res_line1.zinr == zimmer.zinr) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

                        if not res_line1:
                            zimmer.zistatus = 3
                    pass

                    queasy = get_cache (Queasy, {"key": [(eq, 162)],"char1": [(eq, zimmer.zinr)]})

                    if queasy:
                        db_session.delete(queasy)
                    pass

        return generate_inner_output()


    def release_zinr(new_zinr:string):

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        res_line1 = None
        res_line2 = None
        rline = None
        rline2 = None
        bbuff = None
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)
        Bbuff =  create_buffer("Bbuff",Bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == ("delete").lower()  or res_mode.lower()  == ("cancel").lower()  and rline.resstatus == 1:

                res_line1 = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 11)]})

                if res_line1:
                    pass
                    res_line1.resstatus = 1
                    pass
                    res_recid1 = res_line1._recid

            if res_mode.lower()  == ("inhouse").lower() :
                answer = True
                beg_datum = htparam.fdate

                if rline.resstatus == 6 and (rline.zinr.lower()  != (new_zinr).lower()):

                    res_line1 = get_cache (Res_line, {"resnr": [(eq, resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 13)]})

                    if res_line1:

                        for res_line2 in db_session.query(Res_line2).filter(
                                 (Res_line2.resnr == resnr) & (Res_line2.zinr == rline.zinr) & (Res_line2.resstatus == 13)).order_by(Res_line2._recid).all():

                            bill = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, res_line2.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line2.zinr)]})
                            bill.zinr = new_zinr


                            parent_nr = bill.parent_nr
                            pass

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == resnr) & (Bill.parent_nr == parent_nr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():

                                bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                                bbuff.zinr = new_zinr
                                pass
                                pass

                            rline2 = get_cache (Res_line, {"_recid": [(eq, res_line2._recid)]})
                            rline2.zinr = new_zinr
                            pass
                            pass

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})
                        zimmer.zistatus = 2
                        pass

            for zimplan in db_session.query(Zimplan).filter(
                         (Zimplan.zinr == rline.zinr) & (Zimplan.datum >= beg_datum) & (Zimplan.datum < rline.abreise)).order_by(Zimplan._recid).all():

                if res_recid1 != 0:
                    zimplan.res_recid = res_recid1
                else:
                    db_session.delete(zimplan)
                pass


    def add_resplan():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        anz:int = 0
        rline = None
        rbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Rbuff =  create_buffer("Rbuff",Resplan)

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

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
                    resplan = Resplan()
                    db_session.add(resplan)

                    resplan.datum = curr_date
                    resplan.zikatnr = zimkateg.zikatnr
                    anz = resplan.anzzim[i - 1] + rline.zimmeranz
                    resplan.anzzim[i - 1] = anz

                anz = resplan.anzzim[i - 1] + rline.zimmeranz

                rbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                # Rd, 21/7/25
                # add if rbuff
                if rbuff:
                    rbuff.anzzim[i - 1] = anz
                pass
                pass


    def min_resplan():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        curr_date:date = None
        beg_datum:date = None
        i:int = 0
        rline = None
        rbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Rbuff =  create_buffer("Rbuff",Resplan)

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

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

                    rbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                    rbuff.anzzim[i - 1] = rbuff.anzzim[i - 1] - rline.zimmeranz
                    pass
                    pass
                curr_date = curr_date + timedelta(days=1)


    def rmchg_sharer(act_zinr:string, new_zinr:string):

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, bill_no, loopi, lvcarea, res_line, guest, bill, htparam, outorder, reservation, waehrung, master, counters, bediener, queasy, artikel, billjournal, bill_line, umsatz, res_history, reslin_queasy, exrate, messages, zimplan, zimmer, resplan, zimkateg
        nonlocal pvilanguage, resnr, reslinnr, user_init, silenzio
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, buff_bill, buf_resline, bbill, art1

        res_recid1:int = 0
        res_line1 = None
        res_line2 = None
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        curr_datum:date = None
        end_datum:date = None
        new_zkat = None
        bbuff = None
        rbuff = None
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        New_zkat =  create_buffer("New_zkat",Zimkateg)
        Bbuff =  create_buffer("Bbuff",Bill)
        Rbuff =  create_buffer("Rbuff",Resplan)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        beg_datum = htparam.fdate
        end_datum = beg_datum
        res_recid1 = 0

        for messages in db_session.query(Messages).filter(
                     (Messages.zinr == (act_zinr).lower()) & (Messages.resnr == res_line.resnr) & (Messages.reslinnr >= 1)).order_by(Messages._recid).all():
            messages.zinr = new_zinr

        for res_line1 in db_session.query(Res_line1).filter(
                     (Res_line1.resnr == resnr) & (Res_line1.zinr == (act_zinr).lower()) & (Res_line1.resstatus == 13)).order_by(Res_line1._recid).all():

            if end_datum <= res_line1.abreise:
                res_recid1 = res_line1._recid
                end_datum = res_line1.abreise

        if res_line.resstatus == 6 and res_recid1 == 0:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})
            zimmer.zistatus = 2
            pass

        if res_line.resstatus == 6 and res_recid1 != 0:

            res_line1 = get_cache (Res_line, {"_recid": [(eq, res_recid1)]})

            for res_line2 in db_session.query(Res_line2).filter(
                             (Res_line2.resnr == resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 13) & (Res_line2.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line2._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, new_zinr)]})

                new_zkat = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                if new_zkat.zikatnr != res_line2.zikatnr:
                    for curr_datum in date_range(beg_datum,(res_line2.abreise - 1)) :

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line2.zikatnr)],"datum": [(eq, curr_datum)]})

                        if resplan:

                            rbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                            rbuff.anzzim[12] = rbuff.anzzim[12] - 1
                            pass
                            pass

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, new_zkat.zikatnr)],"datum": [(eq, curr_datum)]})

                        if not resplan:
                            resplan = Resplan()
                            db_session.add(resplan)

                            resplan.datum = curr_datum
                            resplan.zikatnr = new_zkat.zikatnr
                            resplan.anzzim[12] = resplan.anzzim[12] + 1
                        else:

                            rbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                            rbuff.anzzim[12] = rbuff.anzzim[12] + 1
                            pass
                            pass

                for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == resnr) & (Bill.parent_nr == res_line2.reslinnr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():
                    bill.zinr = new_zinr
                    pass
                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


                pass

            for res_line2 in db_session.query(Res_line2).filter(
                             (Res_line2.resnr == resnr) & (Res_line2.zinr == (act_zinr).lower()) & (Res_line2.resstatus == 12)).order_by(Res_line2._recid).all():
                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


                pass

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})
            zimmer.zistatus = 2
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 336)]})

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
        mc_pos1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
        mc_pos2 = htparam.finteger

    buf_resline = db_session.query(Buf_resline).filter(
             (Buf_resline.resnr == resnr) & (Buf_resline.reslinnr == reslinnr) & ((Buf_resline.resstatus == 6) | (Buf_resline.resstatus == 13))).first()

    if buf_resline:
        msg_str = translateExtended ("Guest already checkin by another user.", lvcarea, "")

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if not res_line:

        return generate_output()
    else:

        if res_line.resstatus != 11:

            for res_sharer in db_session.query(Res_sharer).filter(
                         (Res_sharer.resnr == resnr) & (Res_sharer.kontakt_nr == reslinnr) & (Res_sharer.l_zuordnung[inc_value(2)] == 1)).order_by(Res_sharer._recid).all():
                res_sharer.zinr = res_line.zinr
                res_sharer.zikatnr = res_line.zikatnr
                res_sharer.setup = res_line.setup


        res_sharer = get_cache (Res_line, {"resnr": [(eq, resnr)],"kontakt_nr": [(eq, reslinnr)],"l_zuordnung[2]": [(eq, 1)]})
        while None != res_sharer:
            pass
            res_sharer.active_flag = 1
            res_sharer.resstatus = 13
            res_sharer.ziwechseldat = get_current_date()
            res_sharer.ankzeit = get_current_time_in_seconds()
            res_sharer.cancelled_id = user_init


            pass

            curr_recid = res_sharer._recid
            res_sharer = db_session.query(Res_sharer).filter(
                         (Res_sharer.resnr == resnr) & (Res_sharer.kontakt_nr == reslinnr) & (Res_sharer.l_zuordnung[inc_value(2)] == 1) & (Res_sharer._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line.resstatus != 11:
            release_zinr(res_line.zinr)
        min_resplan()

        outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"betriebsnr": [(eq, res_line.resnr)]})

        if outorder:
            pass
            db_session.delete(outorder)
            pass

            if not silenzio:
                msg_str = translateExtended ("Off-Market record found and has been removed.", lvcarea, "") + chr_unicode(10)

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if res_line.resstatus == 11:
            new_resstatus = 13
        else:
            new_resstatus = 6

        if res_line.zipreis > 0:
            res_line.l_zuordnung[2] = 0
        res_line.resstatus = new_resstatus
        res_line.active_flag = 1
        res_line.zimmerfix = (res_line.resstatus == 13)
        res_line.ziwechseldat = get_current_date()
        res_line.ankzeit = get_current_time_in_seconds()
        res_line.cancelled_id = user_init


        for curr_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            curr_st = entry(curr_i - 1, res_line.zimmer_wunsch, ";")

            if substring(curr_st, 0, 7) == ("abreise").lower() :
                pass
            else:
                curr_ct = curr_ct + curr_st + ";"
        res_line.zimmer_wunsch = curr_ct + "abreise" +\
                to_string(get_year(res_line.abreise)) +\
                to_string(get_month(res_line.abreise) , "99") +\
                to_string(get_day(res_line.abreise) , "99") + ";"

        if res_line.reserve_dec == 0:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation.insurance:

                if res_line.betriebsnr != 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                else:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

                    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

                if waehrung:
                    res_line.reserve_dec =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        pass

        if res_line.resstatus == 6:
            dummy_b = assign_zinr(res_line._recid, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.resstatus, res_line.gastnrmember, res_line.bemerk, res_line.name)
        add_resplan()

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        guest.resflag = 2
        pass

        if res_line.resstatus == 6 or res_line.resstatus == 13:

            master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"flag": [(eq, 0)],"active": [(eq, True)]})

            if master and master.rechnr != 0:

                bill = get_cache (Bill, {"rechnr": [(eq, master.rechnr)],"resnr": [(eq, master.resnr)],"reslinnr": [(eq, 0)]})

                if not bill:
                    casenum = 1

                    bill = get_cache (Bill, {"rechnr": [(eq, master.rechnr)]})

                    if bill:
                        casenum = 2

                    b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})

                    if casenum == 1:
                        bill = Bill()
                        db_session.add(bill)

                        bill.resnr = master.resnr
                        bill.reslinnr = 0
                        bill.rgdruck = 1
                        bill.billtyp = 2
                        bill.rechnr = master.rechnr
                        bill.gastnr = master.gastnrpay
                        bill.datum = bill_date
                        bill.name = b_receiver.name


                        bill_no = bill.rechnr
                        pass

                    elif casenum == 2:

                        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
                        counters.counter = counters.counter + 1
                        pass
                        pass
                        bill = Bill()
                        db_session.add(bill)

                        bill.resnr = master.resnr
                        bill.reslinnr = 0
                        bill.rgdruck = 1
                        bill.billtyp = 2
                        bill.rechnr = counters.counter
                        bill.gastnr = master.gastnrpay
                        bill.datum = bill_date
                        bill.name = b_receiver.name
                        master.rechnr = bill.rechnr


                        bill_no = bill.rechnr
                        pass
                        pass

                elif bill:
                    pass
                    bill.flag = 0


                    pass

            elif master and master.rechnr == 0:
                bill = Bill()
                db_session.add(bill)

                bill.resnr = master.resnr
                bill.reslinnr = 0
                bill.rgdruck = 1
                bill.billtyp = 2
                bill.datum = bill_date

                counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

                if not counters:
                    counters = Counters()
                    db_session.add(counters)

                    counters.counter_no = 3
                    counters.counter_bez = "Counter for Bill No"


                counters.counter = counters.counter + 1
                bill.rechnr = counters.counter
                pass
                pass
                master.rechnr = bill.rechnr
                pass
                bill.gastnr = master.gastnrpay

                b_receiver = get_cache (Guest, {"gastnr": [(eq, master.gastnr)]})
                bill.name = b_receiver.name
                pass
                bill_no = bill.rechnr

            if bill_no != 0:

                buff_bill = get_cache (Bill, {"rechnr": [(eq, bill_no)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(ne, 2)]})

                if buff_bill:
                    pass
                    db_session.delete(buff_bill)
                    pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        receiver = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)],"gastnr": [(eq, res_line.gastnr)]})

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line.zinr)]})

        if (not bill) and (res_line.l_zuordnung[2] == 0):
            bill = Bill()
            db_session.add(bill)

            bill.flag = 0
            bill.billnr = 1
            bill.rgdruck = 1
            bill.zinr = res_line.zinr
            bill.gastnr = res_line.gastnrpay
            bill.resnr = res_line.resnr
            bill.reslinnr = res_line.reslinnr
            bill.parent_nr = res_line.reslinnr
            bill.name = receiver.name
            bill.kontakt_nr = bediener.nr
            bill.segmentcode = reservation.segmentcode
            bill.datum = bill_date

        htparam = get_cache (Htparam, {"paramnr": [(eq, 932)]})

        if htparam.feldtyp == 4 and htparam.flogical  and bill and bill.rechnr == 0:

            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters.counter = counters.counter + 1
            bill.rechnr = counters.counter
            pass

            queasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, res_line.resnr)],"logi1": [(eq, True)]})

            if queasy:
                for loopi in range(1,4 + 1) :
                    bbill = Bill()
                    db_session.add(bbill)

                    bbill.flag = 0
                    bbill.billnr = loopi + 1
                    bbill.rgdruck = 1
                    bbill.zinr = res_line.zinr
                    bbill.gastnr = res_line.gastnrpay
                    bbill.resnr = res_line.resnr
                    bbill.reslinnr = res_line.reslinnr
                    bbill.parent_nr = res_line.reslinnr
                    bbill.name = receiver.name
                    bbill.kontakt_nr = bediener.nr
                    bbill.segmentcode = reservation.segmentcode
                    bbill.datum = bill_date

                    counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 3
                        counters.counter_bez = "Counter for Bill No"


                    counters.counter = counters.counter + 1
                    bbill.rechnr = counters.counter
                    pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 799)]})

        if htparam.flogical and htparam.feldtyp == 4:

            counters = get_cache (Counters, {"counter_no": [(eq, 29)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 29
                counters.counter_bez = "Counter for Registration No"


            counters.counter = counters.counter + 1
            pass

            if bill:
                bill.rechnr2 = counters.counter
            pass
        pass

        if reservation.depositbez != 0 and reservation.bestat_datum == None and bill:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

            artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

            if not artikel:

                if not silenzio:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("deposit article not defined, deposit transfer", lvcarea, "") + chr_unicode(10) + translateExtended ("to the guest bill not possible!", lvcarea, "") + chr_unicode(10)
            else:
                answer = True

                htparam = get_cache (Htparam, {"paramnr": [(eq, 946)]})

                if htparam.paramgruppe == 6 and htparam.flogical and not silenzio:

                    res_member = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(ne, reslinnr)],"active_flag": [(eq, 0)],"l_zuordnung[2]": [(eq, 0)]})

                    if res_member and htparam.paramgruppe == 6 and htparam.flogical and not silenzio:
                        answer = False
                        ask_deposit = True
                        msg_str = msg_str + chr_unicode(2) + "&Q" +\
                            translateExtended ("Transfer deposit amount to the bill NOW?", lvcarea, "") + chr_unicode(10)

                if answer:
                    pass
                    reservation.bestat_datum = bill_date
                    calculate_deposit_amount()

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
                    sys_id = htparam.fchar
                    it_is = check_masterbill()

                    if it_is:
                        inv_nr = update_mastbill()
                    else:

                        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

                        if not counters:
                            counters = Counters()
                            db_session.add(counters)

                            counters.counter_no = 3
                            counters.counter_bez = "Counter for Bill No"


                        counters.counter = counters.counter + 1
                        bill.rechnr = counters.counter
                        bill.saldo =  to_decimal(bill.saldo) + to_decimal(deposit)
                        bill.mwst[98] = bill.mwst[98] + deposit_foreign
                        bill.rgdruck = 0


                        pass
                        inv_nr = bill.rechnr

                    art1 = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})

                    for billjournal in db_session.query(Billjournal).order_by(Billjournal._recid).all():

                        if num_entries(billjournal.bezeich, "#") > 1:
                            stra = entry(1, billjournal.bezeich, "#")

                            if num_entries(stra, chr_unicode(32)) > 0:
                                strb = entry(0, stra, chr_unicode(32))

                                if strb == to_string(res_line.resnr):
                                    strc = entry(1, stra, "]")
                    bill_line = Bill_line()
                    db_session.add(bill_line)

                    bill_line.rechnr = inv_nr
                    bill_line.artnr = artikel.artnr
                    bill_line.bezeich = artikel.bezeich + "/" + strc
                    bill_line.anzahl = 1
                    bill_line.betrag =  to_decimal(deposit)
                    bill_line.fremdwbetrag =  to_decimal(deposit_foreign)
                    bill_line.zeit = get_current_time_in_seconds()
                    bill_line.userinit = sys_id
                    bill_line.zinr = res_line.zinr
                    bill_line.massnr = res_line.resnr
                    bill_line.billin_nr = res_line.reslinnr
                    bill_line.arrangement = res_line.arrangement
                    bill_line.bill_datum = bill_date

                    if art1:
                        bill_line.bezeich = bill_line.bezeich + " [" + art1.bezeich + "]"
                    pass
                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = inv_nr
                    billjournal.artnr = artikel.artnr
                    billjournal.anzahl = 1
                    billjournal.fremdwaehrng =  to_decimal(deposit_foreign)
                    billjournal.betrag =  to_decimal(deposit)
                    billjournal.bezeich = artikel.bezeich + " " + to_string(reservation.resnr)
                    billjournal.zinr = res_line.zinr
                    billjournal.epreis =  to_decimal("0")
                    billjournal.zinr = res_line.zinr
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.userinit = sys_id
                    billjournal.bill_datum = bill_date

                    if art1:
                        billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]"
                    pass

                    umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

                    if not umsatz:
                        umsatz = Umsatz()
                        db_session.add(umsatz)

                        umsatz.artnr = artikel.artnr
                        umsatz.datum = bill_date
                    umsatz.anzahl = umsatz.anzahl + 1
                    umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit)
                    pass

        if bill:
            pass

        if (res_line.ankunft == res_line.abreise) and (res_line.zipreis > 0):
            get_output(post_dayuse(res_line.resnr, res_line.reslinnr))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

        if htparam.flogical:
            get_output(intevent_1(1, res_line.zinr, "My Checkin!", res_line.resnr, res_line.reslinnr))
        else:

            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 246) & (Queasy.logi1)).first()

            if queasy:
                get_output(intevent_1(1, res_line.zinr, "My Checkin!", res_line.resnr, res_line.reslinnr))

        if priscilla_active:
            get_output(intevent_1(1, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
        check_messages()
        checked_in = True

        if res_line.resstatus == 6:
            get_output(mk_mcoupon(res_line.resnr, res_line.zinr))

        if not silenzio:

            res_sharer = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 11)],"zinr": [(eq, res_line.zinr)]})

            if res_sharer:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("NOTE: Room sharer", lvcarea, "") + " " + res_sharer.name + " " + translateExtended ("not yet checked-in.", lvcarea, "") + chr_unicode(10)
            generate_keycard()

            if mc_flag and not silenzio:
                ask_mcard = True
            msg_str = msg_str + chr_unicode(2) + "&M" + translateExtended ("Guest checked-in.", lvcarea, "") + chr_unicode(10)

            if not silenzio:
                check_midnite_checkin()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.resnr = res_line.resnr
        res_history.reslinnr = res_line.reslinnr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "CheckIn Room " + res_line.zinr +\
                " resno " + to_string(res_line.resnr)
        res_history.action = "Checkin"


        pass
        pass
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = res_line.resnr
        reslin_queasy.reslinnr = res_line.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string("CHECKED-IN") + ";" + to_string(" ") + ";" + to_string(" ") + ";"
        pass
        pass
        pass

    return generate_output()
