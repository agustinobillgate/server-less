#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Waehrung, Queasy, Guest, Bill, Bill_line, Counters, Billjournal, Umsatz

def ts_resplan_delete_depositbl(curr_dept:int, curr_date:date, s_recid:int, user_init:string):

    prepare_cache ([Htparam, Artikel, Waehrung, Queasy, Guest, Bill, Bill_line, Counters, Billjournal, Umsatz])

    ok_flag = False
    active_deposit:bool = False
    depoart:int = 0
    depobez:string = ""
    exchg_rate:Decimal = 1
    deposit_foreign:Decimal = to_decimal("0.0")
    foreign_payment:Decimal = to_decimal("0.0")
    sys_id:string = ""
    htparam = artikel = waehrung = queasy = guest = bill = bill_line = counters = billjournal = umsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, active_deposit, depoart, depobez, exchg_rate, deposit_foreign, foreign_payment, sys_id, htparam, artikel, waehrung, queasy, guest, bill, bill_line, counters, billjournal, umsatz
        nonlocal curr_dept, curr_date, s_recid, user_init

        return {"ok_flag": ok_flag}

    def create_rsv_table():

        nonlocal ok_flag, active_deposit, depoart, depobez, exchg_rate, deposit_foreign, foreign_payment, sys_id, htparam, artikel, waehrung, queasy, guest, bill, bill_line, counters, billjournal, umsatz
        nonlocal curr_dept, curr_date, s_recid, user_init

        it_exist:bool = False
        guest_name:string = ""
        gastno:int = 0
        ns_billno:int = 0
        nsbill_number:int = 0
        tot_deposit:Decimal = to_decimal("0.0")
        depo_amount:Decimal = to_decimal("0.0")
        dept_no:int = 0
        curr_pax:int = 0
        tableno:int = 0
        ft_time:int = 0
        time_rsv_table:string = ""
        date_rsv_table:date = None
        depopay_desc:string = ""
        voucher_str:string = ""
        depopay_art:int = 0
        buffq33 = None
        rsvtable_list = None
        Buffq33 =  create_buffer("Buffq33",Queasy)
        Rsvtable_list =  create_buffer("Rsvtable_list",Queasy)

        buffq33 = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

        if buffq33:
            nsbill_number = 0
            it_exist = True
            gastno = to_int(entry(2, buffq33.char2, "&&"))
            dept_no = buffq33.number1
            tableno = buffq33.number2
            ft_time = to_int(substring(buffq33.char1, 0, 8))
            time_rsv_table = substring(buffq33.char1, 0, 8)
            date_rsv_table = buffq33.date1
            depo_amount =  - to_decimal(buffq33.deci1)


            deposit_foreign =  to_decimal(depo_amount) / to_decimal(exchg_rate)

            guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

            if guest:
                guest_name = guest.name + "," + guest.vorname1

            bill = get_cache (Bill, {"rechnr": [(eq, to_int(buffq33.deci2))],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, buffq33.number1)],"flag": [(eq, 1)]})

            if bill:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

                if bill_line:
                    depopay_desc = bill_line.bezeich
                    depopay_art = bill_line.artnr

                    if num_entries(bill_line.bezeich, "/") > 1:
                        voucher_str = entry(1, bill_line.bezeich, "/")
            bill = Bill()
            db_session.add(bill)


            counters = get_cache (Counters, {"counter_no": [(eq, 3)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters.counter = counters.counter + 1
            nsbill_number = counters.counter
            pass
            bill.flag = 0
            bill.rechnr = nsbill_number
            bill.datum = curr_date
            bill.gastnr = gastno
            bill.billtyp = dept_no
            bill.name = guest_name + " " + guest.anredefirma
            bill.bilname = bill.name
            bill.resnr = 0
            bill.reslinnr = 1
            bill.rgdruck = 0
            bill.saldo =  to_decimal(depo_amount)


            bill_line = Bill_line()
            db_session.add(bill_line)

            bill_line.rechnr = nsbill_number
            bill_line.artnr = depoart
            bill_line.bezeich = depobez + "/" + voucher_str
            bill_line.anzahl = 1
            bill_line.betrag =  to_decimal(depo_amount)
            bill_line.fremdwbetrag =  to_decimal(deposit_foreign)
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.bill_datum = curr_date


            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = nsbill_number
            billjournal.artnr = depoart
            billjournal.anzahl = 1
            billjournal.betrag =  to_decimal(depo_amount)
            billjournal.fremdwaehrng =  to_decimal(deposit_foreign)
            billjournal.epreis =  to_decimal("0")
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.billjou_ref = depopay_art
            billjournal.userinit = user_init
            billjournal.bill_datum = curr_date
            billjournal.bezeich = depobez +\
                    " [#" + to_string(dept_no) + to_string(tableno) + time_rsv_table + "]" + voucher_str


            pass

            umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart)],"departement": [(eq, 0)],"datum": [(eq, curr_date)]})

            if not umsatz:
                umsatz = Umsatz()
                db_session.add(umsatz)

                umsatz.artnr = depoart
                umsatz.datum = curr_date


            umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(depo_amount)
            umsatz.anzahl = umsatz.anzahl + 1


            pass

            rsvtable_list = get_cache (Queasy, {"_recid": [(eq, buffq33._recid)]})

            if rsvtable_list:
                rsvtable_list.deci2 =  to_decimal(nsbill_number)
                pass
                pass
            ok_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if artikel:
            depobez = artikel.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if active_deposit:
        create_rsv_table()

        queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

        if queasy:
            pass
            queasy.logi3 = False
            queasy.date3 = get_current_date()
            queasy.deci3 =  to_decimal(get_current_time_in_seconds)()
            queasy.char3 = queasy.char3 + user_init + ";"
            queasy.betriebsnr = 2


            pass
            pass

    return generate_output()