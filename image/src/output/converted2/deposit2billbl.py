#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Artikel, Res_line, Bill, Reservation, Htparam, Counters, Bill_line, Billjournal, Umsatz, Master, Waehrung, Exrate

def deposit2billbl(resno:int, reslinno:int):

    prepare_cache ([Artikel, Res_line, Bill, Reservation, Htparam, Counters, Bill_line, Billjournal, Umsatz, Master, Waehrung, Exrate])

    bill_date:date = None
    sys_id:string = ""
    it_is:bool = False
    inv_nr:int = 0
    deposit:Decimal = to_decimal("0.0")
    deposit_foreign:Decimal = to_decimal("0.0")
    artikel = res_line = bill = reservation = htparam = counters = bill_line = billjournal = umsatz = master = waehrung = exrate = None

    art1 = None

    Art1 = create_buffer("Art1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

        return {}

    def check_masterbill():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

        master_flag = False

        def generate_inner_output():
            return (master_flag)


        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)],"active": [(eq, True)],"flag": [(eq, 0)]})

        if master:
            master_flag = True

        return generate_inner_output()


    def update_mastbill():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

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

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

        deposit_exrate:Decimal = 1
        exchg_rate:Decimal = 1
        price_decimal:int = 0
        double_currency:bool = False

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


    bill_date = get_output(htpdate(110))

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

    art1 = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})
    bill_line = Bill_line()
    db_session.add(bill_line)

    bill_line.rechnr = inv_nr
    bill_line.artnr = artikel.artnr
    bill_line.bezeich = artikel.bezeich
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

    return generate_output()