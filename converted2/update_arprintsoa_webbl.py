#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Res_history, Bill, Queasy, H_bill, Debitor

bill_list_data, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":Decimal, "deptno":int, "do_release":bool})
t_payload_list_data, T_payload_list = create_model("T_payload_list", {"user_init":string})

def update_arprintsoa_webbl(guestno:int, bill_list_data:[Bill_list], t_payload_list_data:[T_payload_list]):

    prepare_cache ([Bediener, Res_history, Bill, H_bill, Debitor])

    bediener = res_history = bill = queasy = h_bill = debitor = None

    bill_list = t_payload_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, res_history, bill, queasy, h_bill, debitor
        nonlocal guestno


        nonlocal bill_list, t_payload_list

        return {}

    def update_bill_list():

        nonlocal bediener, res_history, bill, queasy, h_bill, debitor
        nonlocal guestno


        nonlocal bill_list, t_payload_list

        do_it:bool = False
        curr_billref:int = ""
        rechnr_list:string = ""

        bill_list = query(bill_list_data, filters=(lambda bill_list: bill_list.do_release == False), first=True)

        if not bill_list:
            do_it = True

        bediener = get_cache (Bediener, {"userinit": [(eq, t_payload_list.user_init)]})

        for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.do_release), sort_by=[("billref",False)]):

            if curr_billref == 0:
                curr_billref = bill_list.billref

            if bediener and curr_billref != bill_list.billref:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Statement Of Account"
                res_history.aenderung = "Transaction Bill Number " +\
                        substring(rechnr_list, 0, length(rechnr_list) - 2) + " has been released from Invoice No : " +\
                        to_string(curr_billref, "9999999")


                curr_billref = bill_list.billref
                rechnr_list = ""
            rechnr_list = rechnr_list + to_string(bill_list.rechnr) + ", "

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
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Statement Of Account"
        res_history.aenderung = "Transaction Bill Number " +\
                substring(rechnr_list, 0, length(rechnr_list) - 2) + " has been released from Invoice No : " +\
                to_string(curr_billref, "9999999")

        if do_it:

            for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.do_release)):

                debitor = get_cache (Debitor, {"gastnr": [(eq, guestno)],"opart": [(le, 1)],"saldo": [(ne, 0)],"zahlkonto": [(eq, 0)],"debref": [(eq, bill_list.billref)]})

                if debitor:
                    debitor.debref = 0
                pass


    t_payload_list = query(t_payload_list_data, first=True)
    update_bill_list()

    return generate_output()