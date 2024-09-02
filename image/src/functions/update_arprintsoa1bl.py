from functions.additional_functions import *
import decimal
from models import Bill, Queasy, H_bill, Debitor

def update_arprintsoa1bl(guestno:int, bill_list:[Bill_list]):
    bill = queasy = h_bill = debitor = None

    bill_list = None

    bill_list_list, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":decimal, "deptno":int, "do_release":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, queasy, h_bill, debitor


        nonlocal bill_list
        nonlocal bill_list_list
        return {}

    def update_bill_list():

        nonlocal bill, queasy, h_bill, debitor


        nonlocal bill_list
        nonlocal bill_list_list

        do_it:bool = False
        curr_billref:int = 0

        bill_list = query(bill_list_list, filters=(lambda bill_list :bill_list.do_release == False), first=True)

        if not bill_list:
            do_it = True

        for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.do_release)):

            if bill_list.deptNo == 0:

                bill = db_session.query(Bill).filter(
                        (Billref == bill_list.billref) &  (Bill.rechnr == bill_list.rechnr)).first()

                if bill:

                    bill = db_session.query(Bill).first()

                    if billref != 0:
                        billref = 0

                    bill = db_session.query(Bill).first()

                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 192) &  (Queasy.number1 == bill_list.rechnr) &  (Queasy.number2 == bill_list.billref)).first()

                    if queasy:

                        queasy = db_session.query(Queasy).first()
                        db_session.delete(queasy)

            else:

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.service[5] == decimal.Decimal(bill_list.billref)) &  (H_bill.departement == bill_list.deptNo) &  (H_bill.rechnr == bill_list.rechnr)).first()

                if h_bill:
                    h_bill.service[5] = 0

                h_bill = db_session.query(H_bill).first()


        if do_it:

            for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.do_release)):

                debitor = db_session.query(Debitor).filter(
                        (Debitor.gastnr == guestno) &  (Debitor.opart <= 1) &  (Debitor.saldo != 0) &  (Debitor.zahlkonto == 0) &  (Debitor.debref == bill_list.billref)).first()

                if debitor:
                    debitor.debref = 0

                debitor = db_session.query(Debitor).first()

    update_bill_list()

    return generate_output()