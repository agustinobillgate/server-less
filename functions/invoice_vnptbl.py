from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill_line, Guest, Queasy, Bill, Hoteldpt, Res_line, Bill_line, Artikel, H_bill, H_artikel

def invoice_vnptbl(fdate:date, tdate:date, fdept:int, tdept:int):
    rlist_list = []
    balance:decimal = to_decimal("0.0")
    counter:int = 0
    curr_datum:date = None
    curr_type:str = ""
    curr_dept:str = ""
    tot_amt:decimal = to_decimal("0.0")
    gtot_amt:decimal = to_decimal("0.0")
    h_bill_line = guest = queasy = bill = hoteldpt = res_line = bill_line = artikel = h_bill = h_artikel = None

    rlist = blist = bline = bguest = bqueasy = None

    rlist_list, Rlist = create_model("Rlist", {"counter":int, "datum":date, "gname":str, "company":str, "rno":str, "billno":int, "depart":str, "tinvoice":str, "balance":decimal})

    Blist = Rlist
    blist_list = rlist_list

    Bline = create_buffer("Bline",H_bill_line)
    Bguest = create_buffer("Bguest",Guest)
    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rlist_list, balance, counter, curr_datum, curr_type, curr_dept, tot_amt, gtot_amt, h_bill_line, guest, queasy, bill, hoteldpt, res_line, bill_line, artikel, h_bill, h_artikel
        nonlocal fdate, tdate, fdept, tdept
        nonlocal blist, bline, bguest, bqueasy


        nonlocal rlist, blist, bline, bguest, bqueasy
        nonlocal rlist_list

        return {"rlist": rlist_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 234) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy.deci1 >= to_decimal(fdept)) & (Queasy.deci1 <= to_decimal(tdept))).order_by(Queasy._recid).all():

        bill = db_session.query(Bill).filter(
                 (Bill.rechnr == queasy.number1) & (Bill.billtyp == queasy.deci1)).first()

        if bill:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.datum = bill.datum
            rlist.billno = bill.rechnr

            if bill.resnr > 0 and bill.reslinnr == 0:
                rlist.tinvoice = "Master Bill"

            elif bill.resnr > 0 and bill.reslinnr > 0:
                rlist.tinvoice = "Guest Folio"


            else:
                rlist.tinvoice = "Non Stay Guest Bill"

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == bill.billtyp)).first()

            if hoteldpt:
                rlist.depart = hoteldpt.depart

            if bill.resnr != 0:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.reslinnr)).first()

                if res_line:
                    rlist.rno = res_line.zinr

                    bguest = db_session.query(Bguest).filter(
                             (Bguest.gastnr == res_line.gastnrmember)).first()

                    if bguest:
                        rlist.gname = bguest.name + " " + bguest.vorname1

                    if res_line.gastnrmember != res_line.gastnrpay:

                        bguest = db_session.query(Bguest).filter(
                                 (Bguest.gastnr == res_line.gastnrpay)).first()

                        if bguest:
                            rlist.company = bguest.name + " " + bguest.vorname1 + " " + bguest.anrede1

            elif bill.gastnr != 0:

                bguest = db_session.query(Bguest).filter(
                         (Bguest.gastnr == bill.gastnr)).first()

                if bguest:
                    rlist.company = bguest.name + " " + bguest.vorname1 + " " + bguest.anrede1


            balance =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.anzahl != 0) & (Bill_line.betrag != 0)).order_by(Bill_line.rechnr, Bill_line.departement, Bill_line.artnr).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement)).first()

                if artikel and artikel.artart != 2 and artikel.artart != 6 and artikel.artart != 7 and artikel.artart != 5:
                    balance =  to_decimal(balance) + to_decimal(bill_line.betrag)


            rlist.balance =  to_decimal(balance)


        else:

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.rechnr == queasy.number1) & (H_bill.departement == to_int(queasy.deci1))).first()

            if h_bill:
                rlist = Rlist()
                rlist_list.append(rlist)

                rlist.billno = h_bill.rechnr
                rlist.tinvoice = "Guest Check"

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == h_bill.departement)).first()

                if hoteldpt:
                    rlist.depart = hoteldpt.depart

                if h_bill.resnr != 0:

                    res_line = db_session.query(Res_line).filter(
                             (Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

                    if res_line:
                        rlist.rno = res_line.zinr

                        bguest = db_session.query(Bguest).filter(
                                 (Bguest.gastnr == res_line.gastnrmember)).first()
                        IFABL bguest THEN
                        rlist.gname = bguest.name + " " + bguest.vorname1

                        bguest = db_session.query(Bguest).filter(
                                 (Bguest.gastnr == res_line.gastnrpay)).first()

                        if bguest:
                            rlist.company = bguest.name + " " + bguest.vorname1 + " " + bguest.anrede1

                    elif not res_line:

                        bguest = db_session.query(Bguest).filter(
                                 (Bguest.name + "," == h_bill.bilname)).first()

                        if bguest:
                            rlist.company = bguest.name + " " + bguest.vorname1 + " " + bguest.anrede1


                        else:

                            bqueasy = db_session.query(Bqueasy).filter(
                                     (Bqueasy.key == 141) & (Bqueasy.char1 == trim(substring(h_bill.bilname, len(h_bill.bilname) - 3 - 1)))).first()

                            if bqueasy:
                                rlist.gname = trim(substring(h_bill.bilname, 0, len(h_bill.bilname) - 3))


                            else:
                                rlist.gname = h_bill.bilname


                else:

                    bguest = db_session.query(Bguest).filter(
                             (Bguest.name + "," == h_bill.bilname)).first()

                    if bguest:
                        rlist.company = bguest.name + " " + bguest.vorname1 + " " + bguest.anrede1


                    else:

                        bqueasy = db_session.query(Bqueasy).filter(
                                 (Bqueasy.key == 141) & (Bqueasy.char1 == trim(substring(h_bill.bilname, len(h_bill.bilname) - 3 - 1)))).first()

                        if bqueasy:
                            rlist.gname = trim(substring(h_bill.bilname, 0, len(h_bill.bilname) - 3))


                        else:
                            rlist.gname = h_bill.bilname

                if rlist.gname == " " and rlist.company == " ":
                    rlist.gname = "KHACH LE"


                balance =  to_decimal("0")

                bline_obj_list = []
                for bline, h_artikel in db_session.query(Bline, H_artikel).join(H_artikel,(H_artikel.artnr == Bline.artnr) & (H_artikel.departement == Bline.departement)).filter(
                         (Bline.departement == h_bill.departement) & (Bline.rechnr == h_bill.rechnr) & (Bline.artnr > 0)).order_by(Bline._recid).all():
                    if bline._recid in bline_obj_list:
                        continue
                    else:
                        bline_obj_list.append(bline._recid)


                    rlist.datum = bline.bill_datum

                    if h_artikel.artart == 0 or h_artikel.artart == 8:
                        balance =  to_decimal(balance) + to_decimal(bline.betrag)


                rlist.balance =  to_decimal(balance)

    for rlist in query(rlist_list, filters=(lambda rlist: rlist.balance == 0)):
        rlist_list.remove(rlist)
    counter = 0

    for rlist in query(rlist_list, sort_by=[("tinvoice",False),("depart",False)]):

        if curr_type != "" and curr_type != rlist.tinvoice:
            blist = Blist()
            blist_list.append(blist)

            counter = counter + 1
            blist.gname = "Sub T O T A L "
            blist.counter = counter
            blist.balance =  to_decimal(tot_amt)
            tot_amt =  to_decimal("0")

        elif curr_dept != "" and curr_dept != rlist.depart:
            blist = Blist()
            blist_list.append(blist)

            counter = counter + 1
            blist.gname = "Sub T O T A L "
            blist.counter = counter
            blist.balance =  to_decimal(tot_amt)
            tot_amt =  to_decimal("0")


        counter = counter + 1
        rlist.counter = counter
        curr_type = rlist.tinvoice
        curr_dept = rlist.depart
        tot_amt =  to_decimal(tot_amt) + to_decimal(rlist.balance)
        gtot_amt =  to_decimal(gtot_amt) + to_decimal(rlist.balance)


    blist = Blist()
    blist_list.append(blist)

    counter = counter + 1
    blist.gname = "Sub T O T A L "
    blist.counter = counter
    blist.balance =  to_decimal(tot_amt)


    blist = Blist()
    blist_list.append(blist)

    counter = counter + 1
    blist.gname = "Grand T O T A L "
    blist.counter = counter
    blist.balance =  to_decimal(gtot_amt)

    return generate_output()