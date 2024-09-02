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
    deposit:decimal = 0
    deposit_foreign:decimal = 0
    artikel = res_line = bill = reservation = htparam = counters = bill_line = billjournal = umsatz = master = waehrung = exrate = None

    art1 = mbill = None

    Art1 = Artikel
    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal art1, mbill


        nonlocal art1, mbill
        return {}

    def check_masterbill():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal art1, mbill


        nonlocal art1, mbill

        master_flag = False

        def generate_inner_output():
            return master_flag

        master = db_session.query(Master).filter(
                (Master.resnr == res_line.resnr) &  (Master.active) &  (Master.flag == 0)).first()

        if master:
            master_flag = True


        return generate_inner_output()

    def update_mastbill():

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal art1, mbill


        nonlocal art1, mbill

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

        nonlocal bill_date, sys_id, it_is, inv_nr, deposit, deposit_foreign, artikel, res_line, bill, reservation, htparam, counters, bill_line, billjournal, umsatz, master, waehrung, exrate
        nonlocal art1, mbill


        nonlocal art1, mbill

        deposit_exrate:decimal = 1
        exchg_rate:decimal = 1
        price_decimal:int = 0
        double_currency:bool = False

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

    bill_date = get_output(htpdate(110))

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

    bill = db_session.query(Bill).filter(
            (Bill.resnr == resno) &  (Bill.reslinnr == reslinno)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resno)).first()
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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

    art1 = db_session.query(Art1).filter(
            (Art1.artnr == reservation.zahlkonto) &  (Art1.departement == 0)).first()
    bill_line = Bill_line()
    db_session.add(bill_line)

    bill_line.rechnr = inv_nr
    bill_line.artnr = artikel.artnr
    bill_line.bezeich = artikel.bezeich
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

    return generate_output()