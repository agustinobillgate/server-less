#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Debitor, Bill, Queasy, H_bill

def release_arprintsoa1bl(guestno:int):

    prepare_cache ([Guest, Debitor, Bill, Queasy, H_bill])

    exist = False
    bill_list_list = []
    guestname:string = ""
    guest = debitor = bill = queasy = h_bill = None

    bill_list = None

    bill_list_list, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":Decimal, "deptno":int, "do_release":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exist, bill_list_list, guestname, guest, debitor, bill, queasy, h_bill
        nonlocal guestno


        nonlocal bill_list
        nonlocal bill_list_list

        return {"exist": exist, "bill-list": bill_list_list}

    def cr_bill_list():

        nonlocal exist, bill_list_list, guestname, guest, debitor, bill, queasy, h_bill
        nonlocal guestno


        nonlocal bill_list
        nonlocal bill_list_list

        for bill_list in query(bill_list_list):
            bill_list_list.remove(bill_list)

        for debitor in db_session.query(Debitor).filter(
                 (Debitor.gastnr == guestno) & (Debitor.opart <= 1) & (Debitor.saldo != 0) & (Debitor.zahlkonto == 0)).order_by(Debitor.betriebsnr, Debitor.rechnr).all():

            if debitor.betriebsnr == 0:

                bill = get_cache (Bill, {"rechnr": [(eq, debitor.rechnr)],"billref": [(ne, 0),(eq, debitor.debref)]})

                if bill and bill.rechnr != 0:

                    bill_list = query(bill_list_list, filters=(lambda bill_list: bill_list.rechnr == bill.rechnr and bill_list.billref == bill.billref), first=True)

                    if not bill_list:
                        exist = True
                        bill_list = Bill_list()
                        bill_list_list.append(bill_list)

                        bill_list.billref = bill.billref
                        bill_list.rechnr = bill.rechnr
                        bill_list.saldo =  to_decimal(debitor.saldo)
                        bill_list.deptno = debitor.betriebsnr


                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 192)],"number1": [(eq, debitor.rechnr)]})

                    if queasy:

                        bill_list = query(bill_list_list, filters=(lambda bill_list: bill_list.rechnr == queasy.number1 and bill_list.billref == queasy.number2), first=True)

                        if not bill_list:
                            exist = True
                            bill_list = Bill_list()
                            bill_list_list.append(bill_list)

                            bill_list.billref = queasy.number2
                            bill_list.rechnr = queasy.number1
                            bill_list.saldo =  to_decimal(debitor.saldo)
                            bill_list.deptno = debitor.betriebsnr


            else:

                h_bill = get_cache (H_bill, {"rechnr": [(eq, debitor.rechnr)],"departement": [(eq, debitor.betriebsnr)],"service[5]": [(ne, 0),(eq, to_decimal(debitor.debref))]})

                if h_bill and h_bill.rechnr != 0:

                    bill_list = query(bill_list_list, filters=(lambda bill_list: bill_list.rechnr == bill.rechnr), first=True)

                    if not bill_list:
                        exist = True
                        bill_list = Bill_list()
                        bill_list_list.append(bill_list)

                        bill_list.billref = to_int(h_bill.service[5])
                        bill_list.rechnr = h_bill.rechnr
                        bill_list.saldo =  to_decimal(h_bill.saldo)
                        bill_list.deptno = debitor.betriebsnr


    guest = get_cache (Guest, {"gastnr": [(eq, guestno)]})

    if guest.karteityp == 0:
        guestname = guest.name + ", " + guest.vorname1
    else:
        guestname = guest.name + ", " + guest.anredefirma
    cr_bill_list()

    return generate_output()