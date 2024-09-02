from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.post_dayuse import post_dayuse
from functions.intevent_1 import intevent_1
from functions.mk_mcoupon import mk_mcoupon
from models import Res_line, Guest, Htparam, Outorder, Reservation, Waehrung, Master, Bill, Counters, Bediener, Artikel, Billjournal, Bill_line, Umsatz, Queasy, Res_history, Reslin_queasy, Exrate, Messages

def res_checkin2bl(pvilanguage:int, resnr:int, reslinnr:int, user_init:str, silenzio:bool):
    new_resstatus = 0
    checked_in = False
    ask_deposit = False
    ask_keycard = False
    ask_mcard = False
    msg_str = ""
    dummy_b:bool = False
    answer:bool = True
    res_recid:int = 0
    res_mode:str = "inhouse"
    resno:int = 0
    resline:int = 0
    exchg_rate:decimal = 1
    price_decimal:int = 0
    double_currency:bool = False
    err_status:int = 0
    deposit:decimal = 0
    deposit_foreign:decimal = 0
    bill_date:date = None
    sys_id:str = ""
    it_is:bool = False
    inv_nr:int = 0
    nat_bez:str = ""
    curr_i:int = 0
    curr_st:str = ""
    curr_ct:str = ""
    mc_flag:bool = False
    mc_pos1:int = 0
    mc_pos2:int = 0
    priscilla_active:bool = True
    casenum:int = 0
    rmno:str = ""
    outstand:decimal = 0
    passwd_ok:bool = False
    stra:str = ""
    strb:str = ""
    strc:str = ""
    lvcarea:str = "res_checkin"
    res_line = guest = htparam = outorder = reservation = waehrung = master = bill = counters = bediener = artikel = billjournal = bill_line = umsatz = queasy = res_history = reslin_queasy = exrate = messages = None

    res_member = receiver = res_sharer = res_line1 = rline = b_receiver = art1 = mbill = None

    Res_member = Res_line
    Receiver = Guest
    Res_sharer = Res_line
    Res_line1 = Res_line
    Rline = Res_line
    B_receiver = Guest
    Art1 = Artikel
    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill
        return {"new_resstatus": new_resstatus, "checked_in": checked_in, "ask_deposit": ask_deposit, "ask_keycard": ask_keycard, "ask_mcard": ask_mcard, "msg_str": msg_str}

    def generate_keycard():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1111)).first()
        ask_keycard = htparam.flogical

    def check_masterbill():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        master_flag = False

        def generate_inner_output():
            return master_flag

        master = db_session.query(Master).filter(
                (Master.resnr == res_line.resnr) &  (Master.active) &  (Master.flag == 0)).first()

        if master:
            master_flag = True


        return generate_inner_output()

    def update_mastbill():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        inv_nr = 0

        def generate_inner_output():
            return inv_nr
        Mbill = Bill

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == res_line.resnr) &  (Mbill.reslinnr == 0)).first()
        mbill.gesamtumsatz = mbill.gesamtumsatz + deposit
        mbill.rgdruck = 0
        mbill.datum = bill_date
        mbill.saldo = mbill.saldo + deposit
        mbill.mwst[98] = mbill.mwst[98] + deposit_foreign

        if mbill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters = counters + 1
            mbill.rechnr = counters

            counters = db_session.query(Counters).first()

            master = db_session.query(Master).first()
            master.rechnr = mbill.rechnr

            master = db_session.query(Master).first()
        inv_nr = mbill.rechnr

        mbill = db_session.query(Mbill).first()


        return generate_inner_output()

    def calculate_deposit_amount():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        deposit_exrate:decimal = 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 120)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if not artikel.pricetab:
            deposit = - reservation.depositbez - reservation.depositbez2


        else:
            deposit_exrate = 1

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if reservation.zahldatum == bill_date:

                if waehrung:
                    deposit_exrate = waehrung.ankauf / waehrung.einheit
            else:

                exrate = db_session.query(Exrate).filter(
                        (Exrate.artnr == artikel.betriebsnr) &  (Exrate.datum == reservation.zahldatum)).first()

                if exrate:
                    deposit_exrate = exrate.betrag

                elif waehrung:
                    deposit_exrate = waehrung.ankauf / waehrung.einheit
            deposit = - reservation.depositbez * deposit_exrate

            if reservation.depositbez2 != 0:
                deposit_exrate = 1

                if reservation.zahldatum == bill_date:

                    if waehrung:
                        deposit_exrate = waehrung.ankauf / waehrung.einheit
                else:

                    exrate = db_session.query(Exrate).filter(
                            (Exrate.artnr == artikel.betriebsnr) &  (Exrate.datum == reservation.zahldatum2)).first()

                    if exrate:
                        deposit_exrate = exrate.betrag

                    elif waehrung:
                        deposit_exrate = waehrung.ankauf / waehrung.einheit
            deposit = deposit - reservation.depositbez2 * deposit_exrate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
        deposit_foreign = round(deposit / exchg_rate, 2)

    def check_messages():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        messages = db_session.query(Messages).filter(
                (Messages.resnr == resnr) &  (Messages.reslinnr == reslinnr)).first()

        if messages:
            get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))

            if not silenzio:
                msg_str = msg_str + chr(2) + translateExtended ("Message(s) exist for this guest.", lvcarea, "") + chr(10)

    def check_midnite_checkin():

        nonlocal new_resstatus, checked_in, ask_deposit, ask_keycard, ask_mcard, msg_str, dummy_b, answer, res_recid, res_mode, resno, resline, exchg_rate, price_decimal, double_currency, err_status, deposit, deposit_foreign, bill_date, sys_id, it_is, inv_nr, nat_bez, curr_i, curr_st, curr_ct, mc_flag, mc_pos1, mc_pos2, priscilla_active, casenum, rmno, outstand, passwd_ok, stra, strb, strc, lvcarea, res_line, guest, htparam, outorder, reservation, waehrung, master, bill, counters, bediener, artikel, billjournal, bill_line, umsatz, queasy, res_history, reslin_queasy, exrate, messages
        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill


        nonlocal res_member, receiver, res_sharer, res_line1, rline, b_receiver, art1, mbill

        if get_current_time_in_seconds() > 6 * 3600:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()

        if htparam.fdate == get_current_date() and not silenzio:
            msg_str = msg_str + chr(2) + translateExtended ("EARLY CHECKED_IN GUEST! POST DAY_USE FEE IF NEEDED.", lvcarea, "") + chr(10)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 336)).first()

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 337)).first()
        mc_pos1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 338)).first()
        mc_pos2 = htparam.finteger

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line.resstatus != 11:

        for res_sharer in db_session.query(Res_sharer).filter(
                    (Res_sharer.resnr == resnr) &  (Res_sharer.kontakt_nr == reslinnr) &  (Res_sharer.l_zuordnung[2] == 1)).all():
            res_sharer.zinr = res_line.zinr
            res_sharer.zikatnr = res_line.zikatnr
            res_sharer.setup = res_line.setup


    res_sharer = db_session.query(Res_sharer).filter(
                (Res_sharer.resnr == resnr) &  (Res_sharer.kontakt_nr == reslinnr) &  (Res_sharer.l_zuordnung[2] == 1)).first()
    while None != res_sharer:

        res_sharer = db_session.query(Res_sharer).first()
        res_sharer.active_flag = 1
        res_sharer.resstatus = 13
        res_sharer.ziwechseldat = get_current_date()
        res_sharer.ankzeit = get_current_time_in_seconds()
        res_sharer.cancelled_id = user_init

        res_sharer = db_session.query(Res_sharer).first()

        res_sharer = db_session.query(Res_sharer).filter(
                    (Res_sharer.resnr == resnr) &  (Res_sharer.kontakt_nr == reslinnr) &  (Res_sharer.l_zuordnung[2] == 1)).first()

    res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line.resstatus != 11:
        release_zinr(res_line.zinr)
    min_resplan()

    outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == res_line.zinr) &  (Outorder.betriebsnr == res_line.resnr)).first()

    if outorder:

        outorder = db_session.query(Outorder).first()
        db_session.delete(outorder)


        if not silenzio:
            msg_str = translateExtended ("Off_Market record found and has been removed.", lvcarea, "") + chr(10)

    res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

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

        if substring(curr_st, 0, 7) == "abreise":
            1
        else:
            curr_ct = curr_ct + curr_st + ";"
    res_line.zimmer_wunsch = curr_ct + "abreise" +\
            to_string(get_year(res_line.abreise)) +\
            to_string(get_month(res_line.abreise) , "99") +\
            to_string(get_day(res_line.abreise) , "99") + ";"

    if res_line.reserve_dec == 0:

        reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

        if reservation.insurance:

            if res_line.betriebsnr != 0:

                waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == res_line.betriebsnr)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 144)).first()

                waehrung = db_session.query(Waehrung).filter(
                            (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                res_line.reserve_dec = waehrung.ankauf / waehrung.einheit

    res_line = db_session.query(Res_line).first()

    if res_line.resstatus == 6:
        dummy_b = assign_zinr(res_line._recid, res_line.ankunft, res_line.abreise, res_line.zinr, res_line.resstatus, res_line.gastnrmember, res_line.bemerk, res_line.name)
    add_resplan()

    guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
    guest.resflag = 2

    guest = db_session.query(Guest).first()

    if res_line.resstatus == 6 or res_line.resstatus == 13:

        master = db_session.query(Master).filter(
                    (Master.resnr == res_line.resnr) &  (Master.flag == 0) &  (Master.ACTIVE)).first()

        if master and master.rechnr != 0:

            bill = db_session.query(Bill).filter(
                        (Bill.rechnr == master.rechnr) &  (Bill.resnr == master.resnr) &  (Bill.reslinnr == 0)).first()

            if not bill:
                casenum = 1

                bill = db_session.query(Bill).filter(
                            (Bill.rechnr == master.rechnr)).first()

                if bill:
                    casenum = 2

                b_receiver = db_session.query(B_receiver).filter(
                            (B_receiver.gastnr == master.gastnr)).first()

                if casenum == 1:
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = master.resnr
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    billtyp = 2
                    bill.rechnr = master.rechnr
                    bill.gastnr = master.gastnrpay
                    bill.datum = bill_date
                    bill.name = b_receiver.name

                    bill = db_session.query(Bill).first()

                elif casenum == 2:

                    counters = db_session.query(Counters).filter(
                                (Counters.counter_no == 3)).first()
                    counters = counters + 1

                    counters = db_session.query(Counters).first()

                    master = db_session.query(Master).first()
                    bill = Bill()
                    db_session.add(bill)

                    bill.resnr = master.resnr
                    bill.reslinnr = 0
                    bill.rgdruck = 1
                    billtyp = 2
                    bill.rechnr = counters
                    bill.gastnr = master.gastnrpay
                    bill.datum = bill_date
                    bill.name = b_receiver.name
                    master.rechnr = bill.rechnr

                    bill = db_session.query(Bill).first()

                    master = db_session.query(Master).first()

        elif master and master.rechnr == 0:
            bill = Bill()
            db_session.add(bill)

            bill.resnr = master.resnr
            bill.reslinnr = 0
            bill.rgdruck = 1
            billtyp = 2
            bill.datum = bill_date

            counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 3)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters = counters + 1
            bill.rechnr = counters

            counters = db_session.query(Counters).first()

            master = db_session.query(Master).first()
            master.rechnr = bill.rechnr

            master = db_session.query(Master).first()
            bill.gastnr = master.gastnrpay

            b_receiver = db_session.query(B_receiver).filter(
                        (B_receiver.gastnr == master.gastnr)).first()
            bill.name = b_receiver.name

            bill = db_session.query(Bill).first()

    bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

    receiver = db_session.query(Receiver).filter(
                (Receiver.gastnr == res_line.gastnrpay)).first()

    reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr) &  (Reservation.gastnr == res_line.gastnr)).first()

    bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.flag == 0) &  (Bill.zinr == res_line.zinr)).first()

    if (not bill) and (res_line.l_zuordnung[2] == 0):
        bill = Bill()
        db_session.add(bill)

        bill.flag = 0
        billnr = 1
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

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 932)).first()

    if htparam.feldtyp == 4 and htparam.flogical  and bill and bill.rechnr == 0:

        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 3
            counters.counter_bez = "Counter for Bill No"


        counters = counters + 1
        bill.rechnr = counters

        counters = db_session.query(Counters).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 799)).first()

    if htparam.flogical and htparam.feldtyp == 4:

        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 29)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 29
            counters.counter_bez = "Counter for Registration No"


        counters = counters + 1

        counters = db_session.query(Counters).first()

        if bill:
            bill.rechnr2 = counters


    reservation = db_session.query(Reservation).first()

    if reservation.depositbez != 0 and reservation.bestat_datum == None and bill:

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 120)).first()

        artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if not artikel:

            if not silenzio:
                msg_str = msg_str + chr(2) + translateExtended ("deposit article not defined, deposit transfer", lvcarea, "") + chr(10) + translateExtended ("to the guest bill not possible!", lvcarea, "") + chr(10)
        else:
            answer = True

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 946)).first()

            if htparam.paramgruppe == 6 and htparam.flogical and not silenzio:

                res_member = db_session.query(Res_member).filter(
                            (Res_member.resnr == resnr) &  (Res_member.reslinnr != reslinnr) &  (Res_member.active_flag == 0) &  (Res_member.l_zuordnung[2] == 0)).first()

                if res_member and htparam.paramgruppe == 6 and htparam.flogical and not silenzio:
                    answer = False
                    ask_deposit = True
                    msg_str = msg_str + chr(2) + "&Q" +\
                        translateExtended ("Transfer deposit amount to the bill NOW?", lvcarea, "") + chr(10)

            if answer:

                reservation = db_session.query(Reservation).first()
                reservation.bestat_dat = bill_date
                calculate_deposit_amount()

                htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 104)).first()
                sys_id = htparam.fchar
                it_is = check_masterbill()

                if it_is:
                    inv_nr = update_mastbill()
                else:

                    counters = db_session.query(Counters).filter(
                                (Counters.counter_no == 3)).first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 3
                        counters.counter_bez = "Counter for Bill No"


                    counters = counters + 1
                    bill.rechnr = counters
                    bill.saldo = bill.saldo + deposit
                    bill.mwst[98] = bill.mwst[98] + deposit_foreign
                    bill.rgdruck = 0

                    counters = db_session.query(Counters).first()
                    inv_nr = bill.rechnr

                art1 = db_session.query(Art1).filter(
                            (Art1.artnr == reservation.zahlkonto) &  (Art1.departement == 0)).first()

                for billjournal in db_session.query(Billjournal).all():

                    if num_entries(billjournal.bezeich, "#") > 1:
                        stra = entry(1, billjournal.bezeich, "#")

                        if num_entries(stra, chr(32)) > 0:
                            strb = entry(0, stra, chr(32))

                            if strb == to_string(res_line.resnr):
                                strc = entry(1, stra, "]")
                bill_line = Bill_line()
                db_session.add(bill_line)

                bill_line.rechnr = inv_nr
                bill_line.artnr = artikel.artnr
                bill_line.bezeich = artikel.bezeich + "/" + strc
                bill_line.anzahl = 1
                bill_line.betrag = deposit
                bill_line.fremdwbetrag = deposit_foreign
                bill_line.zeit = get_current_time_in_seconds()
                bill_line.userinit = sys_id
                bill_line.zinr = res_line.zinr
                bill_line.massnr = res_line.resnr
                bill_line.billin_nr = res_line.reslinnr
                bill_line.arrangement = res_line.arrangement
                bill_line.bill_datum = bill_date

                if art1:
                    bill_line.bezeich = bill_line.bezeich + " [" + art1.bezeich + "]"

                bill_line = db_session.query(Bill_line).first()
                billjournal = Billjournal()
                db_session.add(billjournal)

                billjournal.rechnr = inv_nr
                billjournal.artnr = artikel.artnr
                billjournal.anzahl = 1
                billjournal.fremdwaehrng = deposit_foreign
                billjournal.betrag = deposit
                billjournal.bezeich = artikel.bezeich + " " + to_string(reservation.resnr)
                billjournal.zinr = res_line.zinr
                billjournal.epreis = 0
                billjournal.zinr = res_line.zinr
                billjournal.zeit = get_current_time_in_seconds()
                billjournal.userinit = sys_id
                billjournal.bill_datum = bill_date

                if art1:
                    billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]"

                billjournal = db_session.query(Billjournal).first()

                umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

                if not umsatz:
                    umsatz = Umsatz()
                    db_session.add(umsatz)

                    umsatz.artnr = artikel.artnr
                    umsatz.datum = bill_date
                umsatz.anzahl = umsatz.anzahl + 1
                umsatz.betrag = umsatz.betrag + deposit

                umsatz = db_session.query(Umsatz).first()

    if bill:

        bill = db_session.query(Bill).first()

    if (res_line.ankunft == res_line.abreise) and (res_line.zipreis > 0):
        get_output(post_dayuse(res_line.resnr, res_line.reslinnr))

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 307)).first()

    if htparam.flogical:
        get_output(intevent_1(1, res_line.zinr, "My Checkin!", res_line.resnr, res_line.reslinnr))
    else:

        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 246) &  (Queasy.logi1)).first()

        if queasy:
            get_output(intevent_1(1, res_line.zinr, "My Checkin!", res_line.resnr, res_line.reslinnr))

    if priscilla_active:
        get_output(intevent_1(1, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
    check_messages()
    checked_in = True

    if res_line.resstatus == 6:
        get_output(mk_mcoupon(res_line.resnr, res_line.zinr))

    if not silenzio:

        res_sharer = db_session.query(Res_sharer).filter(
                    (Res_sharer.resnr == res_line.resnr) &  (Res_sharer.reslinnr != res_line.reslinnr) &  (Res_sharer.resstatus == 11) &  (Res_sharer.zinr == res_line.zinr)).first()

        if res_sharer:
            msg_str = msg_str + chr(2) + translateExtended ("NOTE: Room sharer", lvcarea, "") + " " + res_sharer.name + " " + translateExtended ("not yet checked_in.", lvcarea, "") + chr(10)
        generate_keycard()

        if mc_flag and not silenzio:
            ask_mcard = True
        msg_str = msg_str + chr(2) + "&M" + translateExtended ("Guest checked_in.", lvcarea, "") + chr(10)

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

    res_history = db_session.query(Res_history).first()

    reslin_queasy = Reslin_queasy()
    db_session.add(reslin_queasy)

    reslin_queasy.key = "ResChanges"
    reslin_queasy.resnr = res_line.resnr
    reslin_queasy.reslinnr = res_line.reslinnr
    reslin_queasy.date2 = get_current_date()
    reslin_queasy.number2 = get_current_time_in_seconds()


    reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string("CHECKED_IN") + ";" + to_string(" ") + ";" + to_string(" ") + ";"

    reslin_queasy = db_session.query(Reslin_queasy).first()


    return generate_output()