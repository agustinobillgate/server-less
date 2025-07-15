from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Arrangement, Bill, Billjournal, Guest

def extended_rmcharge():
    bill_date:date = None
    found:bool = False
    anz:int = 0
    res_line = arrangement = bill = billjournal = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, found, anz, res_line, arrangement, bill, billjournal, guest

        return {}

    bill_date

    for res_line in db_session.query(Res_line).filter(
             (Res_line.ankunft < bill_date) & (Res_line.abreise == bill_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line.zinr).all():
        found = False

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        bill = db_session.query(Bill).filter(
                 (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr) & (Bill.rechnr > 0)).first()

        if bill:

            billjournal = db_session.query(Billjournal).filter(
                     (Billjournal.bill_datum == bill_date) & (Billjournal.artnr == arrangement.argt_artikelnr) & (Billjournal.departement == 0) & (Billjournal.zinr == res_line.zinr) & (Billjournal.rechnr == bill.rechnr)).first()
            found = None != billjournal

        if not found:

            bill = db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == 0) & (Bill.rechnr > 0)).first()

            if bill:

                billjournal = db_session.query(Billjournal).filter(
                         (Billjournal.bill_datum == bill_date) & (Billjournal.artnr == arrangement.argt_artikelnr) & (Billjournal.departement == 0) & (Billjournal.zinr == res_line.zinr) & (Billjournal.rechnr == bill.rechnr)).first()
                found = None != billjournal

        if found:
            anz = anz + 1

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()
            pass

    return generate_output()