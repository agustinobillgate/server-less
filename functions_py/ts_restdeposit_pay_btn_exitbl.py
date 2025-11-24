#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Waehrung, Guest, Bill, Counters, Bill_line, Billjournal, Umsatz, Bediener, Debitor

def ts_restdeposit_pay_btn_exitbl(pvilanguage:int, s_recid:int, selected_gastnr:int, deposit_amt:Decimal, depo_artpay:int, depo_artpay_bez:string, deposit_pay:Decimal, voucher_str:string, user_init:string, curr_dept:int, moved_tisch:int, pax:int, h1:int, m1:int, h2:int, m2:int, curr_date:date):

    prepare_cache ([Htparam, Artikel, Waehrung, Guest, Bill, Counters, Bill_line, Billjournal, Umsatz, Bediener, Debitor])

    error_flag = False
    msg_str = ""
    ns_billno = 0
    lvcarea:string = "ts-restdeposit-pay"
    exchg_rate:Decimal = 1
    foreign_payment:Decimal = to_decimal("0.0")
    local_payment:Decimal = to_decimal("0.0")
    deposit_foreign:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    bill_date:date = None
    depoart:int = 0
    depobez:string = ""
    sys_id:string = ""
    usr_id:int = 0
    htparam = artikel = waehrung = guest = bill = counters = bill_line = billjournal = umsatz = bediener = debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, msg_str, ns_billno, lvcarea, exchg_rate, foreign_payment, local_payment, deposit_foreign, price_decimal, bill_date, depoart, depobez, sys_id, usr_id, htparam, artikel, waehrung, guest, bill, counters, bill_line, billjournal, umsatz, bediener, debitor
        nonlocal pvilanguage, s_recid, selected_gastnr, deposit_amt, depo_artpay, depo_artpay_bez, deposit_pay, voucher_str, user_init, curr_dept, moved_tisch, pax, h1, m1, h2, m2, curr_date

        return {"error_flag": error_flag, "msg_str": msg_str, "ns_billno": ns_billno}

    def create_close_ns_bill():

        nonlocal error_flag, msg_str, ns_billno, lvcarea, exchg_rate, foreign_payment, local_payment, deposit_foreign, price_decimal, bill_date, depoart, depobez, sys_id, usr_id, htparam, artikel, waehrung, guest, bill, counters, bill_line, billjournal, umsatz, bediener, debitor
        nonlocal pvilanguage, s_recid, selected_gastnr, deposit_amt, depo_artpay, depo_artpay_bez, deposit_pay, voucher_str, user_init, curr_dept, moved_tisch, pax, h1, m1, h2, m2, curr_date

        guest_name:string = ""
        table_no:int = 0
        dept_no:int = 0
        curr_pax:int = 0
        ft_time:int = 0
        time_rsv_table:string = ""
        date_rsv_table:date = None

        guest = get_cache (Guest, {"gastnr": [(eq, selected_gastnr)]})

        if guest:
            guest_name = guest.name + ","

            if guest.vorname1 != "" and guest.vorname1 != None:
                guest_name = guest_name + guest.vorname1
        dept_no = curr_dept
        table_no = moved_tisch
        curr_pax = pax
        ft_time = h1 + m1 + h2 + m2
        time_rsv_table = to_string(h1, "99") + to_string(m1, "99") + to_string(h2, "99") + to_string(m2, "99")
        date_rsv_table = curr_date


        bill = Bill()
        db_session.add(bill)

        # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
        # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 3)).with_for_update().first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 3
            counters.counter_bez = "Counter for Bill No"


        counters.counter = counters.counter + 1
        ns_billno = counters.counter
        pass
        bill.flag = 1
        bill.rechnr = ns_billno
        bill.datum = bill_date
        bill.gastnr = selected_gastnr
        bill.billtyp = curr_dept
        bill.name = guest_name
        bill.bilname = bill.name
        bill.resnr = 0
        bill.reslinnr = 1
        bill.rgdruck = 1
        bill.saldo =  to_decimal("0")

        if guest and guest.anredefirma != "" and guest.anredefirma != None:
            bill.name = bill.name + " " + guest.anredefirma
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = ns_billno
        bill_line.artnr = depoart
        bill_line.bezeich = depobez + "/" + voucher_str + " [" + artikel.bezeich + "]"
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(deposit_amt)
        bill_line.fremdwbetrag =  to_decimal(deposit_foreign)
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = ns_billno
        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag =  - to_decimal(local_payment)
        billjournal.fremdwaehrng =  - to_decimal(foreign_payment)
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.bezeich = depobez +\
                " [#" + to_string(dept_no) + to_string(table_no) + time_rsv_table + " " + artikel.bezeich + "]" + voucher_str
        billjournal.betriebsnr = dept_no


        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date


        umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(local_payment)
        umsatz.anzahl = umsatz.anzahl + 1


        pass
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = ns_billno
        bill_line.artnr = artikel.artnr
        bill_line.bezeich = artikel.bezeich + "/" + voucher_str
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(local_payment)
        bill_line.fremdwbetrag =  to_decimal(foreign_payment)
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date


        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = ns_billno
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag =  to_decimal(local_payment)
        billjournal.fremdwaehrng =  to_decimal(foreign_payment)
        billjournal.epreis =  to_decimal("0")
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = dept_no + table_no + ft_time
        billjournal.betriebsnr = dept_no


        billjournal.bezeich = artikel.bezeich + "[" + translateExtended ("Restaurant Deposit", lvcarea, "") + " #" + to_string(dept_no) + to_string(table_no) + time_rsv_table + "]" + voucher_str
        pass

        umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, artikel.artnr)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(local_payment)


        pass

        if artikel.artart == 7:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            debitor = Debitor()
            db_session.add(debitor)

            debitor.rechnr = ns_billno
            debitor.artnr = artikel.artnr
            debitor.gastnr = selected_gastnr
            debitor.gastnrmember = selected_gastnr
            debitor.saldo =  - to_decimal(local_payment)
            debitor.vesrdep =  - to_decimal(foreign_payment)
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = guest_name
            debitor.vesrcod = translateExtended ("Restaurant Deposit Payment #", lvcarea, "") +\
                    to_string(dept_no) + to_string(table_no) + time_rsv_table

            if voucher_str != "":
                debitor.vesrcod = debitor.vesrcod + "; " + voucher_str
            pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_flag = True
            msg_str = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart = artikel.artnr
        depobez = artikel.bezeich

    artikel = db_session.query(Artikel).filter(
             (Artikel.departement == 0) & ((Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.artnr == depo_artpay)).first()

    if not artikel:
        error_flag = True
        msg_str = translateExtended ("Payment article not defined.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
    sys_id = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    deposit_foreign =  to_decimal(deposit_amt) / to_decimal(exchg_rate)
    foreign_payment =  to_decimal(deposit_pay) / to_decimal(exchg_rate)
    local_payment =  to_decimal(deposit_pay)


    create_close_ns_bill()

    return generate_output()