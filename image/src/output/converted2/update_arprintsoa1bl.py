#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Queasy, H_bill, Debitor

bill_list_list, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":Decimal, "deptno":int, "do_release":bool})

def update_arprintsoa1bl(guestno:int, bill_list_list:[Bill_list]):

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

        bill_list = query(bill_list_list, filters=(lambda bill_list: bill_list.do_release == False), first=True)

        if not bill_list:
            do_it = True

        for bill_list in query(bill_list_list, filters=(lambda bill_list: bill_list.do_release)):

            if bill_list.deptno == 0:

                bill = get_cache (Bill, {"billref": [(eq, bill_list.billref)],"rechnr": [(eq, bill_list.rechnr)]})

                if bill:
                    pass

                    if bill.billref != 0:
                        bill.billref = 0


                    pass
                    pass
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 192)],"number1": [(eq, bill_list.rechnr)],"number2": [(eq, bill_list.billref)]})

                    if queasy:
                        pass
                        db_session.delete(queasy)
                        pass
            else:

                h_bill = get_cache (H_bill, {"service[5]": [(eq, to_decimal(bill_list.billref))],"departement": [(eq, bill_list.deptno)],"rechnr": [(eq, bill_list.rechnr)]})

                if h_bill:
                    h_bill.service[5] = 0


                pass
                pass

        if do_it:

            for bill_list in query(bill_list_list, filters=(lambda bill_list: bill_list.do_release)):

                debitor = get_cache (Debitor, {"gastnr": [(eq, guestno)],"opart": [(le, 1)],"saldo": [(ne, 0)],"zahlkonto": [(eq, 0)],"debref": [(eq, bill_list.billref)]})

                if debitor:
                    debitor.debref = 0
                pass


    update_bill_list()

    return generate_output()