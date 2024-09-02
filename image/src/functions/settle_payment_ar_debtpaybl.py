from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from models import Bediener, Debitor, Htparam, Counters, Artikel, Billjournal

def settle_payment_ar_debtpaybl(age_list:[Age_list], pay_list:[Pay_list], pvilanguage:int, outstand1:decimal, foutstand1:decimal, outstand:decimal, curr_art:int, rundung:int, foutstand:decimal, pay_date:date, balance:decimal, fbalance:decimal, user_init:str):
    f_flag = 0
    msg_str = ""
    lvcarea:str = "ar_debtpay"
    bediener = debitor = htparam = counters = artikel = billjournal = None

    age_list = pay_list = debt = debit = None

    age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ar_recid":int, "rechnr":int, "refno":int, "counters":int, "gastnr":int, "billname":str, "gastnrmember":int, "gastname":str, "zinr":str, "rgdatum":date, "user_init":str, "debt":decimal, "debt_foreign":decimal, "currency":str, "credit":decimal, "tot_debt":decimal, "vouc_nr":str, "prevdate":date, "remarks":str, "b_resname":str, "ci_date":date, "co_date":date})
    pay_list_list, Pay_list = create_model("Pay_list", {"artnr":int, "bezeich":str, "proz":decimal, "betrag":decimal, "f_amt":decimal, "currency":int, "curr_str":str, "bemerk":str, "remain_amt":decimal, "fremain_amt":decimal})

    Debt = Debitor
    Debit = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list
        return {"f_flag": f_flag, "msg_str": msg_str}

    def check_paydate():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list

        bill_date:date = None
        Debt = Debitor

        if pay_date == None:
            f_flag = 1

            return
        bill_date = get_output(htpdate(110))

        if pay_date > bill_date:
            msg_str = translateExtended ("Wrong posting date.", lvcarea, "")
            f_flag = 1

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1014)).first()

        if htparam.fdate != None and pay_date <= htparam.fdate:
            msg_str = translateExtended ("Wrong posting date: Older than last Transfer Date to G/L", lvcarea, "")
            f_flag = 1

            return

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.selected  and age_list.tot_debt != 0)):

            debt = db_session.query(Debt).filter(
                    (Debt._recid == age_list.ar_recid)).first()

            if debt.rgdatum > pay_date:
                msg_str = translateExtended ("Wrong payment date as earlier than A/R billing date.", lvcarea, "")
                f_flag = 1

                return

    def settle_payment():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list

        saldo_i:decimal = 0
        fsaldo_i:decimal = 0
        pay_amount:decimal = 0
        fpay_amount:decimal = 0
        payment1:decimal = 0
        fpayment1:decimal = 0
        pay_count:int = 0
        remain_balance:decimal = 0
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:str = ""
        ok:bool = False
        Debit = Debitor
        ok = False

        if outstand == 0:
            ok = True
        else:

            for age_list in query(age_list_list, filters=(lambda age_list :age_list.selected  and age_list.tot_debt != 0)):
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

                for age_list in query(age_list_list, filters=(lambda age_list :age_list.selected  and age_list.tot_debt != 0)):
                    anzahl = anzahl + 1


            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 110)).first()
            bill_date = htparam.fdate

            for age_list in query(age_list_list, filters=(lambda age_list :age_list.selected  and age_list.tot_debt != 0)):

                debitor = db_session.query(Debitor).filter(
                        (Debitor._recid == age_list.ar_recid)).first()

                if debitor:
                    billname = debitor.name
                saldo_i = age_list.tot_debt
                fsaldo_i = age_list.debt_foreign
                payment1 = - saldo_i
                fpayment1 = - fsaldo_i

                if outstand >= - 0.01 and outstand <= 0.01:
                    debitor.opart = 2
                count = debitor.counters

                if count == 0:

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 5)).first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 5
                        counters.counter_bez = "Counter for A/R Payment"


                    counters = counters + 1
                    debitor.counters = counters
                    count = debitor.counters

                    counters = db_session.query(Counters).first()


                elif count != 0 and (outstand >= - 0.01 and outstand <= 0.01):

                    for debit in db_session.query(Debit).filter(
                            (Debit.opart >= 1) &  (Debit.counters == count) &  (Debit.rechnr == age_list.rechnr) &  (Debit.artnr == curr_art) &  (Debit.zahlkonto > 0)).all():
                        debit.opart = 2
                        payment1 = payment1 - debit.saldo
                        fpayment1 = fpayment1 - debit.vesrdep


                if (pay_count == 0) and anzahl > 1:

                    counters = db_session.query(Counters).filter(
                            (Counters.counter_no == 31)).first()

                    if not counters:
                        counters = Counters()
                        db_session.add(counters)

                        counters.counter_no = 31
                        counters.counter_bez = "Counter for Total A/R Payment"


                    counters = counters + 1
                    pay_count = counters

                    counters = db_session.query(Counters).first()


                for pay_list in query(pay_list_list):

                    if pay_list.proz == 100:
                        pay_amount = - saldo_i
                        fpay_amount = - fsaldo_i

                        if pay_amount == 0:
                            pay_amount = payment1
                            fpay_amount = fpayment1


                    else:
                        pay_amount = saldo_i / outstand1 * pay_list.betrag
                        fpay_amount = fsaldo_i / foutstand1 * pay_list.f_amt

                        if outstand == 0:

                            if round(payment1 - pay_amount, rundung) == 0:
                                pay_amount = payment1
                        else:

                            if (pay_amount - pay_list.remain_amt) <= 0.05 or (pay_list.remain_amt - pay_amount) <= 0.05:
                                pay_amount = pay_list.remain_amt

                        if foutstand == 0:

                            if round(fpayment1 - fpay_amount, rundung) == 0:
                                fpay_amount = fpayment1
                        else:

                            if (fpay_amount - pay_list.fremain_amt) <= 0.05 or (pay_list.fremain_amt - fpay_amount) <= 0.05:
                                fpay_amount = pay_list.fremain_amt
                    debit = Debit()
                    db_session.add(debit)

                    debit.artnr = curr_art
                    debit.zinr = age_list.zinr
                    debit.gastnr = age_list.gastnr
                    debit.gastnrmember = age_list.gastnrmember
                    debit.rechnr = age_list.rechnr
                    debit.saldo = pay_amount
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
                        debit.vesrdep = fpay_amount
                    pay_list.remain_amt = pay_list.remain_amt - pay_amount
                    pay_list.fremain_amt = pay_list.fremain_amt - fpay_amount

                    if outstand != 0:
                        debit.opart = 1
                    else:
                        debit.opart = 2
                    debit.vesrdep = age_list.debt_foreign * pay_amount / age_list.debt

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.departement == 0) &  (Artikel.artnr == pay_list.artnr)).first()

                    if artikel.artart == 2 or artikel.artart == 7:
                        inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)
                    billjournal = Billjournal()
                    db_session.add(billjournal)

                    billjournal.rechnr = debit.rechnr
                    billjournal.bill_datum = pay_date
                    billjournal.artnr = pay_list.artnr
                    billjournal.anzahl = 1
                    billjournal.betrag = debit.saldo
                    billjournal.bezeich = artikel.bezeich
                    billjournal.zinr = debit.zinr
                    billjournal.zeit = get_current_time_in_seconds()
                    billjournal.bediener_nr = bediener.nr
                    billjournal.userinit = bediener.userinit

                    if pay_date != bill_date:
                        billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)
        else:
            msg_str = translateExtended ("Partial Payment for multi_selected A/R records not possible", lvcarea, "")
            f_flag = 2

    def settle_pay1():

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list

        remain_payment:decimal = 0
        fremain_payment:decimal = 0
        pay_count:int = 0
        remain_payment = - balance
        fremain_payment = - fbalance

        for age_list in query(age_list_list, filters=(lambda age_list :age_list.selected  and age_list.tot_debt != 0)):

            if age_list.tot_debt < remain_payment:
                pay_count = full_payment(age_list.ar_recid, pay_count)
                remain_payment = remain_payment - age_list.tot_debt
                fremain_payment = fremain_payment - age_list.debt_foreign


            else:

                if remain_payment != 0:
                    pay_count = partial_payment(age_list.ar_recid, - remain_payment, - fremain_payment, pay_count)

                return

    def partial_payment(ar_recid:int, payment1:decimal, fpayment1:decimal, pay_count:int):

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list

        saldo_i:decimal = 0
        pay_amount:decimal = 0
        fsaldo_i:decimal = 0
        fpay_amount:decimal = 0
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:str = ""
        Debit = Debitor

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == ar_recid)).first()

        if debitor:
            billname = debitor.name
        saldo_i = age_list.tot_debt
        fsaldo_i = age_list.debt_foreign


        count = debitor.counters

        if count == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 5)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 5
                counters.counter_bez = "Counter for A/R Payment"


            counters = counters + 1
            debitor.counters = counters
            count = debitor.counters

            counters = db_session.query(Counters).first()


        if pay_count == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 31)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 31
                counters.counter_bez = "Counter for Total A/R Payment"


            counters = counters + 1
            pay_count = counters

            counters = db_session.query(Counters).first()


        for pay_list in query(pay_list_list):

            if pay_list.proz == 100:
                pay_amount = payment1
                fpay_amount = fpayment1


            else:
                pay_amount = payment1 / balance * pay_list.betrag
                fpay_amount = fpayment1 / fbalance * pay_list.f_amt

            if (pay_amount - pay_list.remain_amt) <= 0.05 or (pay_list.remain_amt - pay_amount) <= 0.05:
                pay_amount = pay_list.remain_amt

            if (fpay_amount - pay_list.fremain_amt) <= 0.05 or (pay_list.fremain_amt - fpay_amount) <= 0.05:
                fpay_amount = pay_list.fremain_amt
            debit = Debit()
            db_session.add(debit)

            debit.artnr = curr_art
            debit.zinr = age_list.zinr
            debit.gastnr = age_list.gastnr
            debit.gastnrmember = age_list.gastnrmember
            debit.rechnr = age_list.rechnr
            debit.saldo = pay_amount
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
                fpay_amount = 0

            if fpay_amount != None:
                debit.vesrdep = fpay_amount
            pay_list.remain_amt = pay_list.remain_amt - pay_amount
            pay_list.fremain_amt = pay_list.fremain_amt - fpay_amount

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == pay_list.artnr)).first()

            if artikel.artart == 2 or artikel.artart == 7:
                inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = debit.rechnr
            billjournal.bill_datum = pay_date
            billjournal.artnr = pay_list.artnr
            billjournal.anzahl = 1
            billjournal.betrag = debit.saldo
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = debit.zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = bediener.userinit

            if pay_date != bill_date:
                billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)

    def full_payment(ar_recid:int, pay_count:int):

        nonlocal f_flag, msg_str, lvcarea, bediener, debitor, htparam, counters, artikel, billjournal
        nonlocal debt, debit


        nonlocal age_list, pay_list, debt, debit
        nonlocal age_list_list, pay_list_list

        saldo_i:decimal = 0
        fsaldo_i:decimal = 0
        pay_amount:decimal = 0
        fpay_amount:decimal = 0
        payment1:decimal = 0
        fpayment1:decimal = 0
        bill_date:date = None
        count:int = 0
        anzahl:int = 0
        billname:str = ""
        Debit = Debitor

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        debitor = db_session.query(Debitor).filter(
                (Debitor._recid == ar_recid)).first()

        if debitor:
            billname = debitor.name
        saldo_i = age_list.tot_debt
        fsaldo_i = age_list.debt_foreign
        payment1 = - saldo_i
        fpayment1 = - fsaldo_i
        debitor.opart = 2


        count = debitor.counters

        if count == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 5)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 5
                counters.counter_bez = "Counter for A/R Payment"


            counters = counters + 1
            debitor.counters = counters
            count = debitor.counters

            counters = db_session.query(Counters).first()


        elif count != 0:

            for debit in db_session.query(Debit).filter(
                    (Debit.opart >= 1) &  (Debit.counters == count) &  (Debit.rechnr == age_list.rechnr) &  (Debit.artnr == curr_art) &  (Debit.zahlkonto > 0)).all():
                debit.opart = 2
                payment1 = payment1 - debit.saldo
                fpayment1 = fpayment1 - debit.vesrdep


        if pay_count == 0:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 31)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 31
                counters.counter_bez = "Counter for Total A/R Payment"


            counters = counters + 1
            pay_count = counters

            counters = db_session.query(Counters).first()


        for pay_list in query(pay_list_list):

            if pay_list.proz == 100:
                pay_amount = - saldo_i
                fpay_amount = - fsaldo_i


            else:
                pay_amount = - saldo_i / balance * pay_list.betrag
                fpay_amount = - fsaldo_i / fbalance * pay_list.f_amt


            debit = Debit()
            db_session.add(debit)

            debit.artnr = curr_art
            debit.zinr = age_list.zinr
            debit.gastnr = age_list.gastnr
            debit.gastnrmember = age_list.gastnrmember
            debit.rechnr = age_list.rechnr
            debit.saldo = pay_amount
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
                fpay_amount = 0

            if fpay_amount != None:
                debit.vesrdep = fpay_amount
            pay_list.remain_amt = pay_list.remain_amt - pay_amount
            pay_list.fremain_amt = pay_list.fremain_amt - fpay_amount

            artikel = db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (Artikel.artnr == pay_list.artnr)).first()

            if artikel.artart == 2 or artikel.artart == 7:
                inv_ar(pay_list.artnr, age_list.zinr, age_list.gastnr, age_list.gastnrmember, age_list.rechnr, pay_amount, fpay_amount, pay_date, billname, user_init, pay_list.bemerk)
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = debit.rechnr
            billjournal.bill_datum = pay_date
            billjournal.artnr = pay_list.artnr
            billjournal.anzahl = 1
            billjournal.betrag = debit.saldo
            billjournal.bezeich = artikel.bezeich
            billjournal.zinr = debit.zinr
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener.nr
            billjournal.userinit = bediener.userinit

            if pay_date != bill_date:
                billjournal.bezeich = billjournal.bezeich + " - " + to_string(pay_date)


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    check_paydate()

    if f_flag == 0:
        settle_payment()

    return generate_output()