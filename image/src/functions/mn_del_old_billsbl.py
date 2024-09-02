from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Bill, Bill_line, Blinehis, Billhis

def mn_del_old_billsbl():
    i = 0
    ci_date:date = None
    htparam = bill = bill_line = blinehis = billhis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis


        return {"i": i}

    def del_old_bills():

        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis

        i:int = 0
        anz:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 160)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        bill = db_session.query(Bill).filter(
                (Bill.flag == 1) &  (Bill.datum < (ci_date - anz))).first()
        while None != bill:
            i = i + 1

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr)).all():

                if bill.rechnr != 0:
                    create_blinehis()
                db_session.delete(bill_line)

            bill = db_session.query(Bill).first()

            if bill.rechnr != 0:
                create_billhis()
            db_session.delete(bill)

            bill = db_session.query(Bill).filter(
                    (Bill.flag == 1) &  (Bill.datum < (ci_date - anz))).first()

    def create_blinehis():

        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis


        blinehis = Blinehis()
        db_session.add(blinehis)

        blinehis.artnr = bill_line.artnr
        blinehis.departement = bill_line.departement
        blinehis.bezeich = bill_line.bezeich
        blinehis.rechnr = bill_line.rechnr
        blinehis.bill_datum = bill_line.bill_datum
        blinehis.anzahl = bill_line.anzahl
        blinehis.epreis = bill_line.epreis
        blinehis.betrag = bill_line.betrag
        blinehis.fremdwbetrag = bill_line.fremdwbetrag
        blinehis.waehrungsnr = bill_line.waehrungsnr
        blinehis.zinr = bill_line.zinr
        blinehis.userinit = bill_line.userinit
        blinehis.sysdate = bill_line.sysdate
        blinehis.zeit = bill_line.zeit

        blinehis = db_session.query(Blinehis).first()


    def create_billhis():

        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis

        mwst1:decimal = 0
        billhis = Billhis()
        db_session.add(billhis)

        billhis.gastnr = bill.gastnr
        billhis.name = bill.name
        billhis.rechnr = bill.rechnr
        billhis.saldo = bill.saldo
        billhis.mwst[98] = bill.mwst[98]
        billhis.resnr = bill.resnr
        billhis.parent_nr = bill.parent_nr
        billhis.billnr = billnr
        billhis.datum = bill.datum
        billhis.zinr = bill.zinr

        if bill.resnr > 0:
            billhis.reslinnr = bill.reslinnr
        else:
            billhis.reslinnr = bill.rechnr

        billhis = db_session.query(Billhis).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_bills()

    return generate_output()