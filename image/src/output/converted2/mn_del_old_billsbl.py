#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bill, Bill_line, Blinehis, Billhis

def mn_del_old_billsbl():

    prepare_cache ([Htparam, Blinehis, Billhis])

    i = 0
    ci_date:date = None
    htparam = bill = bill_line = blinehis = billhis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis

        return {"i": i}

    def del_old_bills():

        nonlocal ci_date, htparam, bill, bill_line, blinehis, billhis

        i:int = 0
        anz:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 160)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        bill = get_cache (Bill, {"flag": [(eq, 1)],"datum": [(lt, (ci_date - anz))]})
        while None != bill:
            i = i + 1

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():

                if bill.rechnr != 0:
                    create_blinehis()
                db_session.delete(bill_line)
            pass

            if bill.rechnr != 0:
                create_billhis()
            db_session.delete(bill)

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.flag == 1) & (Bill.datum < (ci_date - timedelta(days=anz))) & (Bill._recid > curr_recid)).first()


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
        blinehis.epreis =  to_decimal(bill_line.epreis)
        blinehis.betrag =  to_decimal(bill_line.betrag)
        blinehis.fremdwbetrag =  to_decimal(bill_line.fremdwbetrag)
        blinehis.waehrungsnr = bill_line.waehrungsnr
        blinehis.zinr = bill_line.zinr
        blinehis.userinit = bill_line.userinit
        blinehis.sysdate = bill_line.sysdate
        blinehis.zeit = bill_line.zeit


        pass


    def create_billhis():

        nonlocal i, ci_date, htparam, bill, bill_line, blinehis, billhis

        mwst1:Decimal = to_decimal("0.0")
        billhis = Billhis()
        db_session.add(billhis)

        billhis.gastnr = bill.gastnr
        billhis.name = bill.name
        billhis.rechnr = bill.rechnr
        billhis.saldo =  to_decimal(bill.saldo)
        billhis.mwst[98] = bill.mwst[98]
        billhis.resnr = bill.resnr
        billhis.parent_nr = bill.parent_nr
        billhis.billnr = bill.billnr
        billhis.datum = bill.datum
        billhis.zinr = bill.zinr

        if bill.resnr > 0:
            billhis.reslinnr = bill.reslinnr
        else:
            billhis.reslinnr = bill.rechnr
        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_bills()

    return generate_output()