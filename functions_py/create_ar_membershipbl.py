#using conversion tools version: 1.0.0.117
#---------------------------------------------------
# Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
#---------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Cl_member, Guest, Artikel, Mc_fee, Cl_memtype, Htparam, Counters, Bill, Bill_line, Billjournal, Umsatz, Debitor, Bediener, Cl_histpay, Cl_log, Cl_histstatus
from functions.next_counter_for_update import next_counter_for_update

def create_ar_membershipbl(guestno:int, init_fee:Decimal, mber_fee:Decimal, user_init:string):

    prepare_cache ([Cl_member, Guest, Artikel, Mc_fee, Cl_memtype, Htparam, Counters, Bill, Bill_line, Billjournal, Umsatz, Debitor, Bediener, Cl_histpay, Cl_log, Cl_histstatus])

    msg_str = ""
    art_init:int = 0
    artnr1:int = 0
    art_disc:int = 0
    art_disc1:int = 0
    art_tax:int = 0
    art_ccard:int = 0
    pay_art:int = 0
    str_art:string = ""
    billdate:date = None
    dept:int = 0
    member_code:string = ""
    i:int = 0
    s:string = ""
    from_date:date = None
    to_date:date = None
    billname:string = ""
    active_flag:bool = True
    validity:int = 0
    memname:string = ""
    betrag:Decimal = to_decimal("0.0")
    paid_amt:Decimal = to_decimal("0.0")
    paid_flag:bool = False
    typenr:int = 0
    membertype:string = ""
    payment:Decimal = to_decimal("0.0")
    curr_time:int = 0
    billgastnr:int = 0
    cl_member = guest = artikel = mc_fee = cl_memtype = htparam = counters = bill = bill_line = billjournal = umsatz = debitor = bediener = cl_histpay = cl_log = cl_histstatus = None

    mbuff = gbuff = gbuff1 = artikel1 = fbuff = tbuff = None

    Mbuff = create_buffer("Mbuff",Cl_member)
    Gbuff = create_buffer("Gbuff",Guest)
    Gbuff1 = create_buffer("Gbuff1",Guest)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Fbuff = create_buffer("Fbuff",Mc_fee)
    Tbuff = create_buffer("Tbuff",Cl_memtype)


    db_session = local_storage.db_session
    last_count:int = 0
    error_lock:string = ""

    def generate_output():
        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        return {"msg_str": msg_str}

    def init_display():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        gbuff = get_cache (Guest, {"gastnr": [(eq, guestno)]})

        if gbuff:
            memname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1

        mbuff = get_cache (Cl_member, {"gastnr": [(eq, guestno)],"memstatus": [(le, 2)]})

        mc_fee = get_cache (Mc_fee, {"key": [(eq, 2)],"nr": [(eq, mbuff.membertype)],"gastnr": [(eq, mbuff.gastnr)],"activeflag": [(eq, 0)]})
        billgastnr = mbuff.billgastnr
        from_date = mc_fee.von_datum
        to_date = mc_fee.bis_datum
        validity = mbuff.num1
        member_code = mbuff.codenum

        gbuff1 = get_cache (Guest, {"gastnr": [(eq, mbuff.billgastnr)]})

        if gbuff1:

            if gbuff1.karteityp == 0:
                billname = gbuff1.name + ", " + gbuff1.vorname1 + " " +\
                    gbuff.anrede1


            else:
                billname = gbuff1.name + ", " + gbuff1.anredefirma


        else:

            if gbuff.karteityp == 0:
                billname = gbuff.name + ", " + gbuff.vorname1 + " " +\
                    gbuff.anrede1


            else:
                billname = gbuff.name + ", " + gbuff.anredefirma

        fbuff = get_cache (Mc_fee, {"gastnr": [(eq, guestno)],"activeflag": [(eq, 0)]})

        if fbuff:
            betrag =  to_decimal(fbuff.betrag)
            paid_amt =  to_decimal(fbuff.bezahlt)

            if fbuff.bezahlt == 0:
                paid_flag = False

        tbuff = get_cache (Cl_memtype, {"nr": [(eq, fbuff.nr)]})

        if tbuff:
            membertype = tbuff.DESCRIPT
            typenr = tbuff.nr

            if validity == 0:
                validity = tbuff.dauer
        payment =  to_decimal(init_fee) + to_decimal(mber_fee)


    def validation():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        artikel1 = get_cache (Artikel, {"artnr": [(eq, artnr1)],"departement": [(eq, dept)]})

        if not artikel1:
            msg_str = "F/O artNo for membership fee not yet been setup."

        if init_fee != 0:

            artikel1 = get_cache (Artikel, {"artnr": [(eq, art_init)],"departement": [(eq, dept)]})

            if not artikel1:
                msg_str = msg_str + chr_unicode(13) + "F/O artNo for INITIAL fee not yet been setup."


    def create_bill():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(3))

        pass
        bill = Bill()
        db_session.add(bill)

        bill.gastnr = guestno
        # bill.rechnr = counters.counter
        bill.rechnr = last_count
        

        bill.datum = billdate
        bill.billtyp = dept
        bill.name = billname
        bill.bilname = memname
        bill.reslinnr = 1
        bill.rgdruck = 0
        bill.saldo =  to_decimal("0")


        pass
        curr_time = get_current_time_in_seconds()

        if init_fee != 0:
            create_bill_line(art_init, init_fee, "", curr_time, dept)

        if mber_fee != 0:
            create_bill_line(artnr1, mber_fee, "", curr_time, dept)
        curr_time = curr_time + 1
        create_bill_line(pay_art, - payment, "", curr_time, 0)

        artikel = get_cache (Artikel, {"artnr": [(eq, pay_art)],"departement": [(eq, 0)]})

        if artikel.artart == 2 or artikel.artart == 7:
            inv_ar(pay_art, " ", billgastnr, guestno, bill.rechnr, - betrag, 0, billdate, billname, user_init)
        pass
        mc_fee.activeflag = 1
        mc_fee.bezahlt =  to_decimal(betrag)
        mc_fee.bez_datum = billdate
        mc_fee.usr_init = user_init
        mc_fee.artnr = pay_art


        pass
        create_history()

        if active_flag:
            update_membership()
        else:
            update_joindate()


    def create_bill_line(artnr:int, amt:Decimal, voucher:string, curr_time:int, deptnr:int):

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        artikel1 = None
        do_it:bool = True
        Artikel1 =  create_buffer("Artikel1",Artikel)

        artikel1 = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, deptnr)]})
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = artnr
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(amt)
        bill_line.bezeich = artikel1.bezeich
        bill_line.departement = deptnr
        bill_line.zeit = curr_time
        bill_line.userinit = user_init
        bill_line.bill_datum = billdate

        if voucher != "":
            bill_line.bezeich = bill_line.bezeich + "/" + voucher
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = artnr
        billjournal.betrag =  to_decimal(amt)
        billjournal.anzahl = 1
        billjournal.bezeich = bill_line.bezeich
        billjournal.departement = deptnr
        billjournal.zeit = curr_time
        billjournal.userinit = user_init
        billjournal.bill_datum = billdate

        umsatz = get_cache (Umsatz, {"artnr": [(eq, artnr)],"departement": [(eq, deptnr)],"datum": [(eq, billdate)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artnr
            umsatz.departement = deptnr
            umsatz.datum = billdate


        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amt)
        pass


    def inv_ar(curr_art:int, zinr:string, gastnr:int, gastnrmember:int, rechnr:int, saldo:Decimal, saldo_foreign:Decimal, bill_date:date, billname:string, userinit:string):

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        debt = None
        bill1 = None
        comment:string = ""
        verstat:int = 0
        fsaldo:Decimal = to_decimal("0.0")
        lsaldo:Decimal = to_decimal("0.0")
        foreign_rate:bool = False
        currency_nr:int = 0
        double_currency:bool = False
        Debt =  create_buffer("Debt",Debitor)
        Bill1 =  create_buffer("Bill1",Bill)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
        foreign_rate = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
        double_currency = htparam.flogical

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 997)]})

        if not htparam.flogical:

            return

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
        billname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        debt = get_cache (Debitor, {"artnr": [(eq, curr_art)],"rechnr": [(eq, rechnr)],"opart": [(eq, 0)],"rgdatum": [(eq, bill_date)],"counter": [(eq, 0)],"saldo": [(eq, saldo)]})

        if debt:
            pass
            db_session.delete(debt)

            return

        if gastnr != gastnrmember:

            guest = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
            comment = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        comment = comment + " Membership Fee - " + member_code
        debitor = Debitor()
        db_session.add(debitor)

        debitor.artnr = curr_art
        debitor.betrieb_gastmem = currency_nr
        debitor.zinr = zinr
        debitor.gastnr = gastnr
        debitor.gastnrmember = gastnrmember
        debitor.rechnr = rechnr
        debitor.saldo =  - to_decimal(saldo)
        debitor.transzeit = get_current_time_in_seconds()
        debitor.rgdatum = bill_date
        debitor.bediener_nr = bediener.nr
        debitor.name = billname
        debitor.vesrcod = comment
        debitor.verstat = verstat

        if double_currency or foreign_rate:
            debitor.vesrdep =  - to_decimal(saldo_foreign)
        pass


    def create_history():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        mber = None
        sbuff = None
        Mber =  create_buffer("Mber",Cl_member)
        Sbuff =  create_buffer("Sbuff",Bediener)
        cl_histpay = Cl_histpay()
        db_session.add(cl_histpay)

        cl_histpay.key = 1
        cl_histpay.datum = billdate
        cl_histpay.datum1 = from_date
        cl_histpay.datum2 = to_date
        cl_histpay.gastnr = guestno
        cl_histpay.amount =  to_decimal(mber_fee)
        cl_histpay.paid =  to_decimal(payment)
        cl_histpay.balance =  to_decimal("0")
        cl_histpay.remarks = user_init + " - " + "payment History"
        cl_histpay.deci1 =  to_decimal(init_fee)
        cl_histpay.char2 = remarks

        if bill:
            cl_histpay.rechnr = bill.rechnr

        mber = get_cache (Cl_member, {"gastnr": [(eq, guestno)],"memstatus": [(le, 2)]})

        sbuff = get_cache (Bediener, {"userinit": [(eq, mber.salesid)]})
        cl_histpay.codenum = mber.codenum
        cl_histpay.billgastnr = mber.gastnr
        cl_histpay.memtype = mber.membertype

        if sbuff:
            cl_histpay.number1 = sbuff.nr
        pass


    def update_membership():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        mbuff = None
        mbuff1 = None
        mbuff2 = None
        mcbuff = None
        guest1 = None
        guest2 = None
        do_it:bool = False
        Mbuff =  create_buffer("Mbuff",Cl_member)
        Mbuff1 =  create_buffer("Mbuff1",Cl_member)
        Mbuff2 =  create_buffer("Mbuff2",Cl_member)
        Mcbuff =  create_buffer("Mcbuff",Mc_fee)
        Guest1 =  create_buffer("Guest1",Guest)
        Guest2 =  create_buffer("Guest2",Guest)

        mbuff = get_cache (Cl_member, {"gastnr": [(eq, guestno)],"memstatus": [(le, 2)]})

        guest1 = get_cache (Guest, {"gastnr": [(eq, mbuff.gastnr)]})
        cl_log = Cl_log()
        db_session.add(cl_log)

        cl_log.codenum = mbuff.codenum
        cl_log.datum = get_current_date()
        cl_log.zeit = get_current_time_in_seconds()
        cl_log.user_init = user_init
        cl_log.char1 = to_string(mbuff.membertype) + " ; " + to_string(mbuff.membertype) +\
                " ; " + to_string(mbuff.memstatus) + " ; " + to_string(1) +\
                " ; " + mbuff.pict_file + " ; " + mbuff.pict_file +\
                " ; " + mbuff.load_by + " ; " + mbuff.load_by +\
                " ; " + to_string(mbuff.billgastnr, ">,>>9") + " ; " + to_string(mbuff.billgastnr, ">,>>9") +\
                " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") +\
                " ; " + to_string(mbuff.paysched) + " ; " + to_string(mbuff.paysched) +\
                " ; " + to_string(mbuff.billcycle) + " ; " + to_string(mbuff.billcycle) +\
                " ; " + to_string(mbuff.expired) + " ; " + to_string(mc_fee.bis_datum) +\
                " ; " + mbuff.user_init1 + " ; " + user_init


        pass

        if mbuff.lastbill == None:
            mbuff.last_renewed = None


        else:
            mbuff.last_renewed = mbuff.expired_date

        if mbuff.memstatus == 0:
            mbuff.memstatus = 1
            mbuff.nextbill = mc_fee.bis_datum
            mbuff.lastbill = billdate
            mbuff.expired_date = mc_fee.bis_datum


        else:
            mbuff.memstatus = 1
            mbuff.nextbill = mc_fee.bis_datum
            mbuff.lastbill = billdate
            mbuff.join_date = mc_fee.von_datum
            mbuff.expired_date = mc_fee.bis_datum


        pass
        cl_histstatus = Cl_histstatus()
        db_session.add(cl_histstatus)

        cl_histstatus.datum = get_current_date()
        cl_histstatus.codenum = mbuff.codenum
        cl_histstatus.memstatus = mbuff.memstatus
        cl_histstatus.remark = "Membership fee had been paid"
        cl_histstatus.user_init = user_init
        cl_histstatus.zeit = get_current_time_in_seconds()


        pass
        pass

        cl_memtype = get_cache (Cl_memtype, {"nr": [(eq, mbuff.membertype)]})

        if mbuff.gastnr == mbuff.main_gastnr:

            for mbuff2 in db_session.query(Mbuff2).filter(
                         (Mbuff2.main_gastnr == mbuff.main_gastnr) & (Mbuff2.gastnr != mbuff.gastnr) & (Mbuff2.memstatus <= 1)).order_by(Mbuff2._recid).all():

                mcbuff = get_cache (Mc_fee, {"activeflag": [(eq, 0)],"key": [(eq, 2)],"gastnr": [(eq, mbuff2.gastnr)],"betrag": [(eq, 0)]})

                if mcbuff:
                    pass
                    mcbuff.activeflag = 1


                    pass

                    mbuff1 = get_cache (Cl_member, {"_recid": [(eq, mbuff2._recid)]})

                    guest2 = get_cache (Guest, {"gastnr": [(eq, mbuff2.gastnr)]})

                    if guest2:
                        cl_log = Cl_log()
                        db_session.add(cl_log)

                        cl_log.codenum = mbuff1.codenum
                        cl_log.datum = get_current_date()
                        cl_log.zeit = get_current_time_in_seconds()
                        cl_log.user_init = user_init
                        cl_log.char1 = to_string(mbuff1.membertype) + " ; " + to_string(mbuff1.membertype) +\
                                " ; " + to_string(mbuff1.memstatus) + " ; " + to_string(1) +\
                                " ; " + mbuff1.pict_file + " ; " + mbuff1.pict_file +\
                                " ; " + mbuff1.load_by + " ; " + mbuff1.load_by +\
                                " ; " + to_string(mbuff1.billgastnr, ">,>>9") + " ; " + to_string(mbuff1.billgastnr, ">,>>9") +\
                                " ; " + to_string(guest2.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + to_string(guest2.kreditlimit, ">>,>>>,>>>,>>9") +\
                                " ; " + to_string(mbuff1.paysched) + " ; " + to_string(mbuff1.paysched) +\
                                " ; " + to_string(mbuff1.billcycle) + " ; " + to_string(mbuff1.billcycle) +\
                                " ; " + to_string(mbuff1.expired) + " ; " + to_string(mc_fee.bis_datum) +\
                                " ; " + mbuff1.user_init1 + " ; " + user_init


                        pass

                    if mbuff1.lastbill == None:
                        mbuff1.last_renewed = None
                        mbuff1.join_date = from_date
                    else:
                        mbuff1.last_renewed = mbuff.expired_date

                    if mbuff1.memstatus == 0:
                        mbuff1.memstatus = 1
                        mbuff1.nextbill = mc_fee.bis_datum
                        mbuff1.lastbill = billdate


                    else:
                        mbuff1.nextbill = mc_fee.bis_datum
                        mbuff1.lastbill = billdate
                        mbuff1.join_date = mc_fee.von_datum
                        mbuff1.expired_date = mc_fee.bis_datum


                    cl_histstatus = Cl_histstatus()
                    db_session.add(cl_histstatus)

                    cl_histstatus.datum = get_current_date()
                    cl_histstatus.codenum = mbuff1.codenum
                    cl_histstatus.memstatus = mbuff1.memstatus
                    cl_histstatus.remark = "Membership fee had been paid"
                    cl_histstatus.user_init = user_init
                    cl_histstatus.zeit = get_current_time_in_seconds()


                    pass
                    pass

    def update_joindate():

        nonlocal msg_str, art_init, artnr1, art_disc, art_disc1, art_tax, art_ccard, pay_art, str_art, billdate, dept, member_code, i, s, from_date, to_date, billname, active_flag, validity, memname, betrag, paid_amt, paid_flag, typenr, membertype, payment, curr_time, billgastnr, cl_member, guest, artikel, mc_fee, cl_memtype, htparam, counters, bill, bill_line, billjournal, umsatz, debitor, bediener, cl_histpay, cl_log, cl_histstatus
        nonlocal guestno, init_fee, mber_fee, user_init
        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff


        nonlocal mbuff, gbuff, gbuff1, artikel1, fbuff, tbuff

        mbuff = None
        mbuff1 = None
        mbuff2 = None
        guest1 = None
        guest2 = None
        Mbuff =  create_buffer("Mbuff",Cl_member)
        Mbuff1 =  create_buffer("Mbuff1",Cl_member)
        Mbuff2 =  create_buffer("Mbuff2",Cl_member)
        Guest1 =  create_buffer("Guest1",Guest)
        Guest2 =  create_buffer("Guest2",Guest)

        mbuff = get_cache (Cl_member, {"gastnr": [(eq, guestno)],"memstatus": [(le, 2)]})

        if mbuff:

            guest1 = get_cache (Guest, {"gastnr": [(eq, mbuff.gastnr)]})

            if guest1:

                if mc_fee.bis_datum != mbuff.expired:
                    cl_log = Cl_log()
                    db_session.add(cl_log)

                    cl_log.codenum = mbuff.codenum
                    cl_log.datum = get_current_date()
                    cl_log.zeit = get_current_time_in_seconds()
                    cl_log.user_init = user_init
                    cl_log.char1 = to_string(mbuff.membertype) + " ; " + to_string(mbuff.membertype) +\
                            " ; " + to_string(mbuff.memstatus) + " ; " + to_string(mbuff.memstatus) +\
                            " ; " + mbuff.pict_file + " ; " + mbuff.pict_file +\
                            " ; " + mbuff.load_by + " ; " + mbuff.load_by +\
                            " ; " + to_string(mbuff.billgastnr, ">,>>9") + " ; " + to_string(mbuff.billgastnr, ">,>>9") +\
                            " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + to_string(guest1.kreditlimit, ">>,>>>,>>>,>>9") +\
                            " ; " + to_string(mbuff.paysched) + " ; " + to_string(mbuff.paysched) +\
                            " ; " + to_string(mbuff.billcycle) + " ; " + to_string(mbuff.billcycle) +\
                            " ; " + to_string(mbuff.expired) + " ; " + to_string(mc_fee.bis_datum) +\
                            " ; " + mbuff.user_init1 + " ; " + user_init


                    pass

            if mbuff.last_renewed == None:
                mbuff.join_date = mc_fee.von_datum
            else:
                mbuff.last_renewed = billdate
            mbuff.nextbill = mc_fee.bis_datum
            mbuff.lastbill = billdate
            mbuff.expired_date = mc_fee.bis_datum
            pass

        if mbuff.gastnr == mbuff.main_gastnr:

            for mbuff2 in db_session.query(Mbuff2).filter(
                         (Mbuff2.main_gastnr == guestno) & (Mbuff2.gastnr != mbuff.gastnr) & (Mbuff2.memstatus <= 1)).order_by(Mbuff2._recid).all():

                mc_fee = get_cache (Mc_fee, {"activeflag": [(eq, 0)],"key": [(eq, 2)],"gastnr": [(eq, mbuff2.gastnr)]})

                if not mc_fee:

                    mbuff1 = get_cache (Cl_member, {"_recid": [(eq, mbuff2._recid)]})

                    guest2 = get_cache (Guest, {"gastnr": [(eq, mbuff2.gastnr)]})

                    if guest2:
                        cl_log = Cl_log()
                        db_session.add(cl_log)

                        cl_log.codenum = mbuff1.codenum
                        cl_log.datum = get_current_date()
                        cl_log.zeit = get_current_time_in_seconds()
                        cl_log.user_init = user_init
                        cl_log.char1 = to_string(mbuff1.membertype) + " ; " + to_string(mbuff1.membertype) +\
                                " ; " + to_string(mbuff1.memstatus) + " ; " + to_string(mbuff1.memstatus) +\
                                " ; " + mbuff1.pict_file + " ; " + mbuff1.pict_file +\
                                " ; " + mbuff1.load_by + " ; " + mbuff1.load_by +\
                                " ; " + to_string(mbuff1.billgastnr, ">,>>9") + " ; " + to_string(mbuff1.billgastnr, ">,>>9") +\
                                " ; " + to_string(guest2.kreditlimit, ">>,>>>,>>>,>>9") + " ; " + to_string(guest2.kreditlimit, ">>,>>>,>>>,>>9") +\
                                " ; " + to_string(mbuff1.paysched) + " ; " + to_string(mbuff1.paysched) +\
                                " ; " + to_string(mbuff1.billcycle) + " ; " + to_string(mbuff1.billcycle) +\
                                " ; " + to_string(mbuff1.expired) + " ; " + to_string(mc_fee.bis_datum) +\
                                " ; " + mbuff1.user_init1 + " ; " + user_init


                        pass

                    if mbuff1.lastbill == None:
                        mbuff1.last_renewed = None
                        mbuff1.join_date = mbuff.join_date
                    else:
                        mbuff1.last_renewed = mbuff.last_renewed
                    mbuff1.nextbill = mbuff.nextbill
                    mbuff1.lastbill = billdate
                    mbuff1.expired_date = mbuff.expired_date


                    pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1045)]})
    dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1046)]})
    str_art = htparam.fchar
    for i in range(1,num_entries(str_art, ";")  + 1) :
        s = entry(0, entry(i - 1, str_art, ";") , ",")

        if s == "IF":
            art_init = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        elif s == "MF":
            artnr1 = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        elif s == "IFD":
            art_disc = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        elif s == "MFD":
            art_disc1 = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        elif s == "TX":
            art_tax = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        elif s == "CC":
            art_ccard = to_int(entry(1, entry(i - 1, str_art, ";") , ","))
        art_init = 3
        artnr1 = 2
        art_tax = 5
        pay_art = 30


    init_display()
    validation()
    create_bill()

    return generate_output()