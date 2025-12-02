#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.i_inv_ar import *
from models import Bediener, Debitor, Htparam, Counters, Artikel, Billjournal

age_list_data, Age_list = create_model("Age_list", {"selected":bool, "ar_recid":int, "rechnr":int, "refno":int, "counters":int, "gastnr":int, "billname":string, "gastnrmember":int, "gastname":string, "zinr":string, "rgdatum":date, "user_init":string, "debt":Decimal, "debt_foreign":Decimal, "currency":string, "credit":Decimal, "tot_debt":Decimal, "vouc_nr":string, "prevdate":date, "remarks":string, "b_resname":string, "ci_date":date, "co_date":date})
pay_list_data, Pay_list = create_model("Pay_list", {"artnr":int, "bezeich":string, "proz":Decimal, "betrag":Decimal, "f_amt":Decimal, "currency":int, "curr_str":string, "bemerk":string, "remain_amt":Decimal, "fremain_amt":Decimal, "balance":Decimal})

def settle_payment_ar_debtpay_1bl(age_list_data:[Age_list], pay_list_data:[Pay_list], pvilanguage:int, outstand1:Decimal, foutstand1:Decimal, outstand:Decimal, curr_art:int, rundung:int, foutstand:Decimal, pay_date:date, balance:Decimal, fbalance:Decimal, user_init:string):

    prepare_cache ([Bediener, Debitor, Htparam, Counters, Artikel, Billjournal])

    f_flag = 0
    msg_str = ""
    lvcarea:string = "ar-debtpay"
    bediener = debitor = htparam = counters = artikel = billjournal = None

    age_list = pay_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        return {"f_flag": f_flag, "msg_str": msg_str}

    def check_paydate():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        bill_date:date = None
        debt = None
        Debt =  create_buffer("Debt",Debitor)

        if pay_date == None:
            f_flag = 1

            return
        bill_date = get_output(htpdate(110))

        if pay_date > bill_date:
            msg_str = translateExtended ("Wrong posting date.", lvcarea, "")
            f_flag = 1

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})

        if htparam.fdate != None and pay_date <= htparam.fdate:
            msg_str = translateExtended ("Wrong posting date: Older than last Transfer Date to G/L", lvcarea, "")
            f_flag = 1

            return

        for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected  and age_list.tot_debt != 0)):

            debt = get_cache (Debitor, {"_recid": [(eq, age_list.ar_recid)]})

            if debt.rgdatum > pay_date:
                msg_str = translateExtended ("Wrong payment date as earlier than A/R billing date.", lvcarea, "")
                f_flag = 1

                return


    def settle_payment():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        saldo_i:Decimal = to_decimal("0.0")
        fsaldo_i:Decimal = to_decimal("0.0")
        pay_amount:Decimal = to_decimal("0.0")
        fpay_amount:Decimal = to_decimal("0.0")
        payment1:Decimal = to_decimal("0.0")
        fpayment1:Decimal = to_decimal("0.0")
        pay_count:int = 0
        remain_balance:Decimal = to_decimal("0.0")
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:string = ""
        ok:bool = False
        debit = None
        Debit =  create_buffer("Debit",Debitor)
        ok = False

        if outstand == 0:
            ok = True
        else:

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected  and age_list.tot_debt != 0)):
                anzahl = anzahl + 1

            if anzahl == 0:

                return

            if anzahl == 1:
                ok = True
            else:
                ok = True
                settle_pay1()

                return

        if ok:

            if anzahl != 1:

                for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected  and age_list.tot_debt != 0)):
                    anzahl = anzahl + 1


            htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            bill_date = htparam.fdate

            for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected  and age_list.tot_debt != 0), sort_by=[("rechnr",False)]):

                debitor = get_cache (Debitor, {"_recid": [(eq, age_list.ar_recid)]})

                if debitor:
                    billname = debitor.name
                saldo_i =  to_decimal(age_list.tot_debt)
                fsaldo_i =  to_decimal(age_list.debt_foreign)
                payment1 =  - to_decimal(saldo_i)
                fpayment1 =  - to_decimal(fsaldo_i)

                if outstand >= - 0.01 and outstand <= 0.01:
                    debitor.opart = 2
                count = debitor.counters

                if count == 0:

                    # counters = get_cache (Counters, {"counter_no": [(eq, 5)]})
                    counters = db_session.query(Counters).filter(Counters.counter_no == 5).with_for_update().first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 5
                        counters.counter_bez = "Counter for A/R Payment"


                    counters.counters = counters.counters + 1
                    debitor.counters = counters.counters
                    count = debitor.counters

                elif count != 0 and (outstand >= - 0.01 and outstand <= 0.01):

                    for debit in db_session.query(Debit).filter(
                             (Debit.opart >= 1) & (Debit.counters == count) & (Debit.rechnr == age_list.rechnr) & (Debit.artnr == curr_art) & (Debit.zahlkonto > 0)).order_by(Debit._recid).with_for_update().all():
                        
                        debit.opart = 2
                        payment1 =  to_decimal(payment1) - to_decimal(debit.saldo)
                        fpayment1 =  to_decimal(fpayment1) - to_decimal(debit.vesrdep)

                if (pay_count == 0) and anzahl > 1:

                    counters = db_session.query(Counters).filter(Counters.counter_no == 31).with_for_update().first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 31
                        counters.counter_bez = "Counter for Total A/R Payment"


                    counters.counters = counters.counters + 1
                    pay_count = counters.counters

                for pay_list in query(pay_list_data):

                    if pay_list.proz == 100:
                        pay_amount =  - to_decimal(saldo_i)
                        fpay_amount =  - to_decimal(fsaldo_i)

                        if pay_amount == 0:
                            pay_amount =  to_decimal(payment1)
                            fpay_amount =  to_decimal(fpayment1)


                    else:
                        pay_amount =  to_decimal(saldo_i) / to_decimal(outstand1) * to_decimal(pay_list.betrag)
                        fpay_amount =  to_decimal(fsaldo_i) / to_decimal(foutstand1) * to_decimal(pay_list.f_amt)

                        if outstand == 0:

                            if round(payment1 - pay_amount, rundung) == 0:
                                pay_amount =  to_decimal(payment1)
                        else:

                            if (pay_amount - pay_list.remain_amt) <= 0.05 or (pay_list.remain_amt - pay_amount) <= 0.05:
                                pay_amount =  to_decimal(pay_list.remain_amt)

                        if foutstand == 0:

                            if round(fpayment1 - fpay_amount, rundung) == 0:
                                fpay_amount =  to_decimal(fpayment1)
                        else:

                            if (fpay_amount - pay_list.fremain_amt) <= 0.05 or (pay_list.fremain_amt - fpay_amount) <= 0.05:
                                fpay_amount =  to_decimal(pay_list.fremain_amt)
                    debit = Debitor()
                    db_session.add(debit)

                    debit.artnr = curr_art
                    debit.zinr = age_list.zinr
                    debit.gastnr = age_list.gastnr
                    debit.gastnrmember = age_list.gastnrmember
                    debit.rechnr = age_list.rechnr
                    debit.saldo =  to_decimal(pay_amount)
                    debit.zahlkonto = pay_list.artnr
                    debit.betrieb_gastmem = pay_list.currency
                    debit.counters = count
                    debit.transzeit = get_current_time_in_seconds()
                    debit.rgdatum = pay_date
                    debit.bediener_nr = bediener.nr
                    debit.name = billname
                    debit.vesrcod = pay_list.bemerk
                    debit.betrieb_gastmem = pay_list.currency
                    debit.betriebsnr = pay_count

                    if fpay_amount != None:
                        debit.vesrdep =  to_decimal(fpay_amount)
                    pay_list.remain_amt =  to_decimal(pay_list.remain_amt) - to_decimal(pay_amount)
                    pay_list.fremain_amt =  to_decimal(pay_list.fremain_amt) - to_decimal(fpay_amount)

                    if outstand != 0:
                        debit.opart = 1
                    else:
                        debit.opart = 2
                    debit.vesrdep =  to_decimal(age_list.debt_foreign) * to_decimal(pay_amount) / to_decimal(age_list.debt)

                    artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, pay_list.artnr)]})

                    if artikel.artart == 2 or artikel.artart == 7:
                        i_inv_ar.inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)

                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = debit.rechnr
                    billjournal.bill_datum = pay_date
                    billjournal.artnr = pay_list.artnr
                    billjournal.anzahl = 1
                    billjournal.betrag =  to_decimal(debit.saldo)
                    billjournal.bezeich = artikel.bezeich
                    billjournal.zinr = debit.zinr
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.bediener_nr = bediener.nr
                    billjournal.userinit = bediener.userinit

                    if pay_date != bill_date:
                        billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)

            if outstand == 0:
                check_rounding()
            else:
                msg_str = translateExtended ("Partial Payment for multi-selected A/R records not possible", lvcarea, "")
                f_flag = 2


    def settle_pay1():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        remain_payment:Decimal = to_decimal("0.0")
        fremain_payment:Decimal = to_decimal("0.0")
        pay_count:int = 0
        remain_payment =  - to_decimal(balance)
        fremain_payment =  - to_decimal(fbalance)

        for age_list in query(age_list_data, filters=(lambda age_list: age_list.selected  and age_list.tot_debt != 0), sort_by=[("tot_debt",False),("rechnr",False)]):

            if age_list.tot_debt < remain_payment:
                pay_count = full_payment(age_list.ar_recid, pay_count)
                remain_payment =  to_decimal(remain_payment) - to_decimal(age_list.tot_debt)
                fremain_payment =  to_decimal(fremain_payment) - to_decimal(age_list.debt_foreign)


            else:

                if remain_payment != 0:
                    pay_count = partial_payment(age_list.ar_recid, - remain_payment, - fremain_payment, pay_count)

                return


    def partial_payment(ar_recid:int, payment1:Decimal, fpayment1:Decimal, pay_count:int):

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        saldo_i:Decimal = to_decimal("0.0")
        pay_amount:Decimal = to_decimal("0.0")
        fsaldo_i:Decimal = to_decimal("0.0")
        fpay_amount:Decimal = to_decimal("0.0")
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:string = ""
        debit = None

        def generate_inner_output():
            return (pay_count)

        Debit =  create_buffer("Debit",Debitor)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        debitor = get_cache (Debitor, {"_recid": [(eq, ar_recid)]})

        if debitor:
            billname = debitor.name
        saldo_i =  to_decimal(age_list.tot_debt)
        fsaldo_i =  to_decimal(age_list.debt_foreign)


        count = debitor.counters

        if count == 0:

            counters = db_session.query(Counters).filter(Counters.counter_no == 5).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 5
                counters.counter_bez = "Counter for A/R Payment"


            counters.counters = counters.counters + 1
            debitor.counters = counters.counters
            count = debitor.counters

        if pay_count == 0:

            counters = db_session.query(Counters).filter(Counters.counter_no == 31).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 31
                counters.counter_bez = "Counter for Total A/R Payment"


            counters.counters = counters.counters + 1
            pay_count = counters.counters

        for pay_list in query(pay_list_data):

            if pay_list.proz == 100 or balance == pay_list.betrag:
                pay_amount =  to_decimal(payment1)
                fpay_amount =  to_decimal(fpayment1)


            else:
                pay_amount =  to_decimal(payment1) / to_decimal(balance) * to_decimal(pay_list.betrag)
                fpay_amount =  to_decimal(fpayment1) / to_decimal(fbalance) * to_decimal(pay_list.f_amt)

            if (pay_amount - pay_list.remain_amt) <= 0.05 or (pay_list.remain_amt - pay_amount) <= 0.05:
                pay_amount =  to_decimal(pay_list.remain_amt)

            if (fpay_amount - pay_list.fremain_amt) <= 0.05 or (pay_list.fremain_amt - fpay_amount) <= 0.05:
                fpay_amount =  to_decimal(pay_list.fremain_amt)
            debit = Debitor()
            db_session.add(debit)

            debit.artnr = curr_art
            debit.zinr = age_list.zinr
            debit.gastnr = age_list.gastnr
            debit.gastnrmember = age_list.gastnrmember
            debit.rechnr = age_list.rechnr
            debit.saldo =  to_decimal(pay_amount)
            debit.zahlkonto = pay_list.artnr
            debit.betrieb_gastmem = pay_list.currency
            debit.counters = count
            debit.transzeit = get_current_time_in_seconds()
            debit.rgdatum = pay_date
            debit.bediener_nr = bediener.nr
            debit.name = billname
            debit.vesrcod = pay_list.bemerk
            debit.betrieb_gastmem = pay_list.currency
            debit.opart = 1
            debit.betriebsnr = pay_count

            if fpay_amount == None:
                fpay_amount =  to_decimal("0")

            if fpay_amount != None:
                debit.vesrdep =  to_decimal(fpay_amount)
            pay_list.remain_amt =  to_decimal(pay_list.remain_amt) - to_decimal(pay_amount)
            pay_list.fremain_amt =  to_decimal(pay_list.fremain_amt) - to_decimal(fpay_amount)

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, pay_list.artnr)]})

            if artikel.artart == 2 or artikel.artart == 7:
                i_inv_ar.inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)

            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = debit.rechnr
            billjournal.bill_datum = pay_date
            billjournal.artnr = pay_list.artnr
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(debit.saldo)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = debit.zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = bediener.userinit

            if pay_date != bill_date:
                billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)

        return generate_inner_output()


    def full_payment(ar_recid:int, pay_count:int):

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, balance, fbalance, user_init


        nonlocal age_list, pay_list

        saldo_i:Decimal = to_decimal("0.0")
        fsaldo_i:Decimal = to_decimal("0.0")
        pay_amount:Decimal = to_decimal("0.0")
        fpay_amount:Decimal = to_decimal("0.0")
        payment1:Decimal = to_decimal("0.0")
        fpayment1:Decimal = to_decimal("0.0")
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:string = ""
        debit = None

        def generate_inner_output():
            return (pay_count)

        Debit =  create_buffer("Debit",Debitor)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        debitor = get_cache (Debitor, {"_recid": [(eq, ar_recid)]})

        if debitor:
            billname = debitor.name
        saldo_i =  to_decimal(age_list.tot_debt)
        fsaldo_i =  to_decimal(age_list.debt_foreign)
        payment1 =  - to_decimal(saldo_i)
        fpayment1 =  - to_decimal(fsaldo_i)
        debitor.opart = 2


        count = debitor.counters

        if count == 0:

            counters = db_session.query(Counters).filter(Counters.counter_no == 5).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 5
                counters.counter_bez = "Counter for A/R Payment"


            counters.counters = counters.counters + 1
            debitor.counters = counters.counters
            count = debitor.counters

        elif count != 0:

            for debit in db_session.query(Debit).filter(
                     (Debit.opart >= 1) & (Debit.counters == count) & (Debit.rechnr == age_list.rechnr) & (Debit.artnr == curr_art) & (Debit.zahlkonto > 0)).order_by(Debit._recid).with_for_update().all():
                
                debit.opart = 2
                payment1 =  to_decimal(payment1) - to_decimal(debit.saldo)
                fpayment1 =  to_decimal(fpayment1) - to_decimal(debit.vesrdep)
                

        if pay_count == 0:

            counters = db_session.query(Counters).filter(Counters.counter_no == 31).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 31
                counters.counter_bez = "Counter for Total A/R Payment"


            counters.counters = counters.counters + 1
            pay_count = counters.counters

        for pay_list in query(pay_list_data):

            if pay_list.proz == 100 or balance == pay_list.betrag:
                pay_amount =  - to_decimal(saldo_i)
                fpay_amount =  - to_decimal(fsaldo_i)


            else:
                pay_amount =  - to_decimal(saldo_i) / to_decimal(balance) * to_decimal(pay_list.betrag)
                fpay_amount =  - to_decimal(fsaldo_i) / to_decimal(fbalance) * to_decimal(pay_list.f_amt)


            debit = Debitor()
            db_session.add(debit)

            debit.artnr = curr_art
            debit.zinr = age_list.zinr
            debit.gastnr = age_list.gastnr
            debit.gastnrmember = age_list.gastnrmember
            debit.rechnr = age_list.rechnr
            debit.saldo =  to_decimal(pay_amount)
            debit.zahlkonto = pay_list.artnr
            debit.betrieb_gastmem = pay_list.currency
            debit.counters = count
            debit.transzeit = get_current_time_in_seconds()
            debit.rgdatum = pay_date
            debit.bediener_nr = bediener.nr
            debit.name = billname
            debit.vesrcod = pay_list.bemerk
            debit.betrieb_gastmem = pay_list.currency
            debit.opart = 2
            debit.betriebsnr = pay_count

            if fpay_amount == None:
                fpay_amount =  to_decimal("0")

            if fpay_amount != None:
                debit.vesrdep =  to_decimal(fpay_amount)
            pay_list.remain_amt =  to_decimal(pay_list.remain_amt) - to_decimal(pay_amount)
            pay_list.fremain_amt =  to_decimal(pay_list.fremain_amt) - to_decimal(fpay_amount)

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, pay_list.artnr)]})

            if artikel.artart == 2 or artikel.artart == 7:
                i_inv_ar.inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)

            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = debit.rechnr
            billjournal.bill_datum = pay_date
            billjournal.artnr = pay_list.artnr
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(debit.saldo)
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = debit.zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = bediener.userinit

            if pay_date != bill_date:
                billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)

        return generate_inner_output()


    def check_rounding():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal pvilanguage, outstand1, foutstand1, outstand, curr_art, rundung, foutstand, pay_date, fbalance, user_init


        nonlocal age_list, pay_list

        balance:Decimal = to_decimal("0.0")
        balance1:Decimal = to_decimal("0.0")
        balance2:Decimal = to_decimal("0.0")
        debt = None
        Debt =  create_buffer("Debt",Debitor)

        for age_list in query(age_list_data):
            balance =  to_decimal("0")
            balance1 =  to_decimal("0")
            balance2 =  to_decimal("0")

            for debitor in db_session.query(Debitor).filter(
                     (Debitor.zahlkonto > 0) & (Debitor.rechnr == age_list.rechnr) & (Debitor.gastnr == age_list.gastnr) & (Debitor.gastnrmember == age_list.gastnrmember)).order_by(Debitor._recid).all():
                balance =  to_decimal(balance) + to_decimal(debitor.saldo)

            debitor = get_cache (Debitor, {"zahlkonto": [(eq, 0)],"rechnr": [(eq, age_list.rechnr)],"gastnr": [(eq, age_list.gastnr)],"gastnrmember": [(eq, age_list.gastnrmember)]})

            if debitor:
                balance1 =  to_decimal(debitor.saldo)


            balance2 =  to_decimal(balance1) + to_decimal(balance)

            if balance2 == 0.01:

                debt = get_cache (Debitor, {"zahlkonto": [(gt, 0)],"rechnr": [(eq, age_list.rechnr)],"gastnr": [(eq, age_list.gastnr)],"gastnrmember": [(eq, age_list.gastnrmember)]})

                if debt:
                    debt.saldo =  to_decimal(debt.saldo) + to_decimal(balance2)

            elif balance2 == -0.01:

                debt = get_cache (Debitor, {"zahlkonto": [(gt, 0)],"rechnr": [(eq, age_list.rechnr)],"gastnr": [(eq, age_list.gastnr)],"gastnrmember": [(eq, age_list.gastnrmember)]})

                if debt:
                    debt.saldo =  to_decimal(debt.saldo) - to_decimal(balance2)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    check_paydate()

    if f_flag == 0:
        settle_payment()


    return generate_output()