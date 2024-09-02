from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Artikel, Waehrung, Queasy, Guest, Bill, Bill_line, Counters, Billjournal, Umsatz

def ts_resplan_delete_depositbl(curr_dept:int, curr_date:date, s_recid:int, user_init:str):
    ok_flag = False
    active_deposit:bool = False
    depoart:int = 0
    depobez:str = ""
    exchg_rate:decimal = 1
    deposit_foreign:decimal = 0
    foreign_payment:decimal = 0
    sys_id:str = ""
    htparam = artikel = waehrung = queasy = guest = bill = bill_line = counters = billjournal = umsatz = None

    buffq33 = rsvtable_list = None

    Buffq33 = Queasy
    Rsvtable_list = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, active_deposit, depoart, depobez, exchg_rate, deposit_foreign, foreign_payment, sys_id, htparam, artikel, waehrung, queasy, guest, bill, bill_line, counters, billjournal, umsatz
        nonlocal buffq33, rsvtable_list


        nonlocal buffq33, rsvtable_list
        return {"ok_flag": ok_flag}

    def create_rsv_table():

        nonlocal ok_flag, active_deposit, depoart, depobez, exchg_rate, deposit_foreign, foreign_payment, sys_id, htparam, artikel, waehrung, queasy, guest, bill, bill_line, counters, billjournal, umsatz
        nonlocal buffq33, rsvtable_list


        nonlocal buffq33, rsvtable_list

        it_exist:bool = False
        guest_name:str = ""
        gastno:int = 0
        ns_billno:int = 0
        nsbill_number:int = 0
        tot_deposit:decimal = 0
        depo_amount:decimal = 0
        dept_no:int = 0
        curr_pax:int = 0
        tableno:int = 0
        ft_time:int = 0
        time_rsv_table:str = ""
        date_rsv_table:date = None
        depopay_desc:str = ""
        voucher_str:str = ""
        depopay_art:int = 0
        Buffq33 = Queasy
        Rsvtable_list = Queasy

        buffq33 = db_session.query(Buffq33).filter(
                (Buffq33._recid == s_recid)).first()

        if buffq33:
            nsbill_number = 0
            it_exist = True
            gastno = to_int(entry(2, buffq33.char2, "&&"))
            dept_no = buffq33.number1
            tableno = buffq33.number2
            ft_time = to_int(substring(buffq33.char1, 0, 8))
            time_rsv_table = substring(buffq33.char1, 0, 8)
            date_rsv_table = buffq33.date1
            depo_amount = - buffq33.deci1


            deposit_foreign = depo_amount / exchg_rate

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == gastno)).first()

            if guest:
                guest_name = guest.name + "," + guest.vorname1

            bill = db_session.query(Bill).filter(
                    (Bill.rechnr == to_int(buffq33.deci2)) &  (Bill.gastnr == gastno) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == buffq33.number1) &  (Bill.flag == 1)).first()

            if bill:

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

                if bill_line:
                    depopay_desc = bill_line.bezeich
                    depopay_art = bill_line.artnr

                    if num_entries(bill_line.bezeich, "/") > 1:
                        voucher_str = entry(1, bill_line.bezeich, "/")
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
            nsbill_number = counters

            counters = db_session.query(Counters).first()
            bill.flag = 0
            bill.rechnr = nsbill_number
            bill.datum = curr_date
            bill.gastnr = gastno
            billtyp = dept_no
            bill.name = guest_name + " " + guest.anredefirma
            bill.bilname = bill.name
            bill.resnr = 0
            bill.reslinnr = 1
            bill.rgdruck = 0
            bill.saldo = depo_amount


            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = nsbill_number
            bill_line.artnr = depoart
            bill_line.bezeich = depobez + "/" + voucher_str
            bill_line.anzahl = 1
            bill_line.betrag = depo_amount
            bill_line.fremdwbetrag = deposit_foreign
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = curr_date

            bill_line = db_session.query(Bill_line).first()
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = nsbill_number
            billjournal.artnr = depoart
            billjournal.anzahl = 1
            billjournal.betrag = depo_amount
            billjournal.fremdwaehrng = deposit_foreign
            billjournal.epreis = 0
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.billjou_ref = depopay_art
            billjournal.userinit = user_init
            billjournal.bill_datum = curr_date
            billjournal.bezeich = depobez +\
                    " [#" + to_string(dept_no) + to_string(tableno) + time_rsv_table + "]" + voucher_str

            billjournal = db_session.query(Billjournal).first()

            umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == depoart) &  (Umsatz.departement == 0) &  (Umsatz.datum == curr_date)).first()

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = depoart
                umsatz.datum = curr_date


            umsatz.betrag = umsatz.betrag + depo_amount
            umsatz.anzahl = umsatz.anzahl + 1


            rsvtable_list = db_session.query(Rsvtable_list).filter(
                        (Rsvtable_list._recid == buffq33._recid)).first()

            if rsvtable_list:
                rsvtable_list.deci2 = nsbill_number

                rsvtable_list = db_session.query(Rsvtable_list).first()


            ok_flag = True


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if artikel:
            depobez = artikel.bezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    if active_deposit:
        create_rsv_table()

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == s_recid)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()
            queasy.logi3 = False
            queasy.date3 = get_current_date()
            queasy.deci3 = get_current_time_in_seconds()
            queasy.char3 = queasy.char3 + user_init + ";"
            queasy.betriebsnr = 2

            queasy = db_session.query(Queasy).first()


    return generate_output()