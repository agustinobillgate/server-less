#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Queasy, H_bill, Debitor
from sqlalchemy.orm.attributes import flag_modified

bill_list_data, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":Decimal, "deptno":int, "do_release":bool})

def update_arprintsoa1bl(guestno:int, bill_list_data:[Bill_list]):

    prepare_cache ([Bill, H_bill, Debitor])

    bill = queasy = h_bill = debitor = None

    bill_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, queasy, h_bill, debitor
        nonlocal guestno


        nonlocal bill_list

        return {}

    def update_bill_list():

        nonlocal bill, queasy, h_bill, debitor
        nonlocal guestno


        nonlocal bill_list

        do_it:bool = False
        curr_billref:int = 0

        bill_list = query(bill_list_data, filters=(lambda bill_list: bill_list.do_release == False), first=True)

        if not bill_list:
            do_it = True

        for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.do_release)):

            if bill_list.deptno == 0:

                bill = db_session.query(Bill).filter((Bill.billref == bill_list.billref) & (Bill.rechnr == bill_list.rechnr)).first()

                if bill:
                    db_session.refresh(bill, with_for_update=True)

                    if bill.billref != 0:
                        bill.billref = 0

                else:

                    queasy = db_session.query(Queasy).filter((Queasy.key == 192) & (Queasy.number1 == bill_list.rechnr) & (Queasy.number2 == bill_list.billref)).first()

                    if queasy:
                        db_session.refresh(queasy, with_for_update=True)
                        db_session.delete(queasy)

            else:

                h_bill = db_session.query(H_bill).filter((H_bill.service[5] == to_decimal(bill_list.billref)) & (H_bill.departement == bill_list.deptno) & (H_bill.rechnr == bill_list.rechnr)).with_for_update().first()

                if h_bill:
                    h_bill.service[5] = 0
                    flag_modified(h_bill, "service")

        if do_it:

            for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.do_release)):

                debitor = db_session.query(Debitor).filter((Debitor.gastnr == guestno) & (Debitor.opart <= 1) & (Debitor.saldo != 0) & (Debitor.zahlkonto == 0) & (Debitor.debref == bill_list.billref)).with_for_update().first()

                if debitor:
                    debitor.debref = 0

    update_bill_list()

    return generate_output()