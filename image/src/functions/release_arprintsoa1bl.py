from functions.additional_functions import *
import decimal
from models import Guest, Debitor, Bill, Queasy, H_bill

def release_arprintsoa1bl(guestno:int):
    exist = False
    bill_list_list = []
    guestname:str = ""
    guest = debitor = bill = queasy = h_bill = None

    bill_list = None

    bill_list_list, Bill_list = create_model("Bill_list", {"billref":int, "rechnr":int, "saldo":decimal, "deptno":int, "do_release":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exist, bill_list_list, guestname, guest, debitor, bill, queasy, h_bill


        nonlocal bill_list
        nonlocal bill_list_list
        return {"exist": exist, "bill-list": bill_list_list}

    def cr_bill_list():

        nonlocal exist, bill_list_list, guestname, guest, debitor, bill, queasy, h_bill


        nonlocal bill_list
        nonlocal bill_list_list

        for bill_list in query(bill_list_list):
            bill_list_list.remove(bill_list)

        for debitor in db_session.query(Debitor).filter(
                (Debitor.gastnr == guestno) &  (Debitor.opart <= 1) &  (Debitor.saldo != 0) &  (Debitor.zahlkonto == 0)).all():

            if debitor.betriebsnr == 0:

                bill = db_session.query(Bill).filter(
                        (Bill.rechnr == debitor.rechnr) &  (Billref != 0) &  (Billref == debitor.debref)).first()

                if bill and bill.rechnr != 0:

                    bill_list = query(bill_list_list, filters=(lambda bill_list :bill_list.rechnr == bill.rechnr and bill_list.billref == billref), first=True)

                    if not bill_list:
                        exist = True
                        bill_list = Bill_list()
                        bill_list_list.append(bill_list)

                        bill_list.billref = billref
                        bill_list.rechnr = bill.rechnr
                        bill_list.saldo = debitor.saldo
                        bill_list.deptNo = debitor.betriebsnr


                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 192) &  (Queasy.number1 == debitor.rechnr)).first()

                    if queasy:

                        bill_list = query(bill_list_list, filters=(lambda bill_list :bill_list.rechnr == queasy.number1 and bill_list.billref == queasy.number2), first=True)

                        if not bill_list:
                            exist = True
                            bill_list = Bill_list()
                            bill_list_list.append(bill_list)

                            bill_list.billref = queasy.number2
                            bill_list.rechnr = queasy.number1
                            bill_list.saldo = debitor.saldo
                            bill_list.deptNo = debitor.betriebsnr


            else:

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.rechnr == debitor.rechnr) &  (H_bill.departement == debitor.betriebsnr) &  (H_bill.service[5] != 0) &  (H_bill.service[5] == decimal.Decimal(debitor.debref))).first()

                if h_bill and h_bill.rechnr != 0:

                    bill_list = query(bill_list_list, filters=(lambda bill_list :bill_list.rechnr == bill.rechnr), first=True)

                    if not bill_list:
                        exist = True
                        bill_list = Bill_list()
                        bill_list_list.append(bill_list)

                        bill_list.billref = to_int(h_bill.service[5])
                        bill_list.rechnr = h_bill.rechnr
                        bill_list.saldo = h_bill.saldo
                        bill_list.deptNo = debitor.betriebsnr

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == guestno)).first()

    if guest.karteityp == 0:
        guestname = guest.name + ", " + guest.vorname1
    else:
        guestname = guest.name + ", " + guest.anredefirma
    cr_bill_list()

    return generate_output()