from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Artikel, Res_line, Bill, Reservation, Htparam, Counters, Bill_line, Billjournal, Umsatz, Master, Waehrung, Exrate

def deposit2billbl(resno:int, reslinno:int):
    bill_date:date = None
    sys_id:str = ""
    it_is:bool = False
    inv_nr:int = 0
    deposit:decimal = to_decimal("0.0")
    deposit_foreign:decimal = to_decimal("0.0")
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

    def update_mastbill():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

        master_flag = False
        inv_nr = 0
        mbill = None

        def generate_inner_output():
            return (master_flag, inv_nr)


            master = db_session.query(Master).filter(
                     (Master.resnr == res_line.resnr) & (Master.active) & (Master.flag == 0)).first()
        Mbill =  create_buffer("Mbill",Bill)

        mbill = db_session.query(Mbill).filter(
                 (Mbill.resnr == res_line.resnr) & (Mbill.reslinnr == 0)).first()
        mbill.gesamtumsatz =  to_decimal(mbill.gesamtumsatz) + to_decimal(deposit)
        mbill.rgdruck = 0
        mbill.datum = bill_date
        mbill.saldo =  to_decimal(mbill.saldo) + to_decimal(deposit)
        mbill.mwst[98] = mbill.mwst[98] + deposit_foreign

        if mbill.rechnr == 0:

            counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 3)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 3
                counters.counter_bez = "Counter for Bill No"


            counters.counter = counters.counter + 1
            mbill.rechnr = counters.counter
            master.rechnr = mbill.rechnr
        inv_nr = mbill.rechnr

        return generate_inner_output()


    def calculate_deposit_amount():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal resno, reslinno
        nonlocal art1


        nonlocal art1

        deposit_exrate:decimal = 1
        exchg_rate:decimal = 1
        price_decimal:int = 0
        double_currency:bool = False

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 120)).first()

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

        if not artikel.pricetab:
            deposit =  - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)


        else:
            deposit_exrate =  to_decimal("1")

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == artikel.betriebsnr)).first()

            if reservation.zahldatum == bill_date:

                if waehrung:
                    deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:

                exrate = db_session.query(Exrate).filter(
                         (Exrate.artnr == artikel.betriebsnr) & (Exrate.datum == reservation.zahldatum)).first()

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

                    exrate = db_session.query(Exrate).filter(
                             (Exrate.artnr == artikel.betriebsnr) & (Exrate.datum == reservation.zahldatum2)).first()

                    if exrate:
                        deposit_exrate =  to_decimal(exrate.betrag)

                    elif waehrung:
                        deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            deposit =  to_decimal(deposit) - to_decimal(reservation.depositbez2) * to_decimal(deposit_exrate)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        deposit_foreign = to_decimal(round(deposit / exchg_rate , 2))


    bill_date = get_output(htpdate(110))

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.reslinnr == reslinno)).first()

    bill = db_session.query(Bill).filter(
             (Bill.resnr == resno) & (Bill.reslinnr == reslinno)).first()

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == resno)).first()
    reservation.bestat_datum = bill_date


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


        counters.counter = counters.counter + 1
        bill.rechnr = counters.counter
        bill.saldo =  to_decimal(bill.saldo) + to_decimal(deposit)
        bill.mwst[98] = bill.mwst[98] + deposit_foreign
        bill.rgdruck = 0


        inv_nr = bill.rechnr

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

    art1 = db_session.query(Art1).filter(
             (Art1.artnr == reservation.zahlkonto) & (Art1.departement == 0)).first()
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

    umsatz = db_session.query(Umsatz).filter(
             (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).first()

    if not umsatz:
        umsatz = Umsatz()
        db_session.add(umsatz)

        umsatz.artnr = artikel.artnr
        umsatz.datum = bill_date


    umsatz.anzahl = umsatz.anzahl + 1
    umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit)

    if bill:

        if master:
            master_flag = True

    return generate_output()