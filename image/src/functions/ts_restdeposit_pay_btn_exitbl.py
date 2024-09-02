from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Artikel, Waehrung, Guest, Bill, Counters, Bill_line, Billjournal, Umsatz, Bediener, Debitor

def ts_restdeposit_pay_btn_exitbl(pvilanguage:int, s_recid:int, selected_gastnr:int, deposit_amt:decimal, depo_artpay:int, depo_artpay_bez:str, deposit_pay:decimal, voucher_str:str, user_init:str, curr_dept:int, moved_tisch:int, pax:int, h1:int, m1:int, h2:int, m2:int, curr_date:date):
    error_flag = False
    msg_str = ""
    ns_billno = 0
    lvcarea:str = "ts_restdeposit_pay"
    exchg_rate:decimal = 1
    foreign_payment:decimal = 0
    local_payment:decimal = 0
    deposit_foreign:decimal = 0
    price_decimal:int = 0
    bill_date:date = None
    depoart:int = 0
    depobez:str = ""
    sys_id:str = ""
    htparam = artikel = waehrung = guest = bill = counters = bill_line = billjournal = umsatz = bediener = debitor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, msg_str, ns_billno, lvcarea, exchg_rate, foreign_payment, local_payment, deposit_foreign, price_decimal, bill_date, depoart, depobez, sys_id, htparam, artikel, waehrung, guest, bill, counters, bill_line, billjournal, umsatz, bediener, debitor


        return {"error_flag": error_flag, "msg_str": msg_str, "ns_billno": ns_billno}

    def create_close_ns_bill():

        nonlocal error_flag, msg_str, ns_billno, lvcarea, exchg_rate, foreign_payment, local_payment, deposit_foreign, price_decimal, bill_date, depoart, depobez, sys_id, htparam, artikel, waehrung, guest, bill, counters, bill_line, billjournal, umsatz, bediener, debitor

        guest_name:str = ""
        table_no:int = 0
        dept_no:int = 0
        curr_pax:int = 0
        ft_time:int = 0
        time_rsv_table:str = ""
        date_rsv_table:date = None

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == selected_gastnr)).first()

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


        counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 3
            counters.counter_bez = "Counter for Bill No"


        counters = counters + 1
        ns_billno = counters

        counters = db_session.query(Counters).first()
        bill.flag = 1
        bill.rechnr = ns_billno
        bill.datum = bill_date
        bill.gastnr = selected_gastnr
        billtyp = curr_dept
        bill.name = guest_name
        bill.bilname = bill.name
        bill.resnr = 0
        bill.reslinnr = 1
        bill.rgdruck = 1
        bill.saldo = 0

        if guest and guest.anredefirma != "" and guest.anredefirma != None:
            bill.name = bill.name + " " + guest.anredefirma
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = ns_billno
        bill_line.artnr = depoart
        bill_line.bezeich = depobez + "/" + voucher_str + " [" + artikel.bezeich + "]"
        bill_line.anzahl = 1
        bill_line.betrag = deposit_amt
        bill_line.fremdwbetrag = deposit_foreign
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        bill_line = db_session.query(Bill_line).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = ns_billno
        billjournal.artnr = depoart
        billjournal.anzahl = 1
        billjournal.betrag = - local_payment
        billjournal.fremdwaehrng = - foreign_payment
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.billjou_ref = artikel.artnr
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.bezeich = depobez +\
                " [#" + to_string(dept_no) + to_string(table_no) + time_rsv_table + " " + artikel.bezeich + "]" + voucher_str

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == depoart) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoart
            umsatz.datum = bill_date


        umsatz.betrag = umsatz.betrag - local_payment
        umsatz.anzahl = umsatz.anzahl + 1

        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = ns_billno
        bill_line.artnr = artikel.artnr
        bill_line.bezeich = artikel.bezeich + "/" + voucher_str
        bill_line.anzahl = 1
        bill_line.betrag = local_payment
        bill_line.fremdwbetrag = foreign_payment
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        bill_line = db_session.query(Bill_line).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = ns_billno
        billjournal.artnr = artikel.artnr
        billjournal.anzahl = 1
        billjournal.betrag = local_payment
        billjournal.fremdwaehrng = foreign_payment
        billjournal.epreis = 0
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date
        billjournal.billjou_ref = dept_no + table_no + ft_time


        billjournal.bezeich = artikel.bezeich + "[" + translateExtended ("Restaurant Deposit", lvcarea, "") + " #" + to_string(dept_no) + to_string(table_no) + time_rsv_table + "]" + voucher_str

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.departement == 0) &  (Umsatz.artnr == artikel.artnr) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = artikel.artnr
            umsatz.datum = bill_date


        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + local_payment


        if artikel.artart == 7:

            bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
            debitor = Debitor()
            db_session.add(debitor)

            debitor.rechnr = ns_billno
            debitor.artnr = artikel.artnr
            debitor.gastnr = selected_gastnr
            debitor.gastnrmember = selected_gastnr
            debitor.saldo = - local_payment
            debitor.vesrdep = - foreign_payment
            debitor.transzeit = get_current_time_in_seconds()
            debitor.rgdatum = bill_date
            debitor.bediener_nr = bediener.nr
            debitor.name = guest_name
            debitor.vesrcod = translateExtended ("Restaurant Deposit Payment #", lvcarea, "") +\
                    to_string(dept_no) + to_string(table_no) + time_rsv_table

            if voucher_str != "":
                debitor.vesrcod = debitor.vesrcod + "; " + voucher_str


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if not artikel or artikel.artart != 5:
            error_flag = True
            msg_str = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart = artikel.artnr
        depobez = artikel.bezeich

    artikel = db_session.query(Artikel).filter(
            (Artikel.departement == 0) &  ((Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.artnr == depo_artpay)).first()

    if not artikel:
        error_flag = True
        msg_str = translateExtended ("Payment article not defined.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 104)).first()
    sys_id = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    deposit_foreign = deposit_amt / exchg_rate
    foreign_payment = deposit_pay / exchg_rate
    local_payment = deposit_pay


    create_close_ns_bill()

    return generate_output()