from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Guest, Bill, Bill_line, Bediener, Reservation, History

def bil_selectbl(pvilanguage:int, sorttype:int, zinr:str, bil_int:int, curr_gastnr:int, ci_date:date, gastname:str, to_name:str, rechnr:int):
    b1_list_list = []
    actflag:int = 0
    bl_saldo:decimal = 0
    lvcarea:str = "bil_select"
    res_line = guest = bill = bill_line = bediener = reservation = history = None

    b1_list = resline = rline = guestmember = mbill = bbuff = tbuff = usr = None

    b1_list_list, B1_list = create_model("B1_list", {"zinr":str, "billnr":int, "rechnr":int, "name":str, "saldo":decimal, "resnr":int, "reslinnr":int, "datum":date, "printnr":int, "vesrcod":str, "rec_id":int, "fg_col":bool, "resname":str, "address":str, "city":str, "b_comments":str})

    Resline = Res_line
    Rline = Res_line
    Guestmember = Guest
    Mbill = Bill
    Bbuff = Bill
    Tbuff = Bill
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, reservation, history
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff, usr


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff, usr
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def disp_bill_list0():

        nonlocal b1_list_list, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, reservation, history
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff, usr


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff, usr
        nonlocal b1_list_list

        to_rechnr:int = 0
        fr_name:str = ""
        to_name:str = ""
        rmno:str = ""

        if sorttype == 1:

            if bil_int == 0:

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.active_flag == 1) &  (func.lower(Res_line.zinr) == (zinr).lower()) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                        bl_saldo = 0

                        for bill_line in db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == bill.rechnr)).all():
                            bl_saldo = bl_saldo + bill_line.betrag

                        if bill.zinr != res_line.zinr:

                            bbuff = db_session.query(Bbuff).filter(
                                    (Bbuff._recid == bill._recid)).first()
                            bbuff.zinr = res_line.zinr

                            bbuff = db_session.query(Bbuff).first()


                        if bl_saldo != bill.saldo:

                            tbuff = db_session.query(Tbuff).filter(
                                    (Tbuff._recid == bill._recid)).first()
                            tbuff.saldo = bl_saldo

                            tbuff = db_session.query(Tbuff).first()

            bill_obj_list = []
            for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                    (func.lower(Bill.zinr) >= (zinr).lower()) &  (func.lower(Bill.zinr) != "") &  (Bill.flag == bil_int)).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                assign_it()

        elif sorttype == 2:

            if curr_gastnr == 0:

                if gastname == "":
                    gastname = "a"

                if gastname.lower()  == "*":
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr (ord(substring(gastname, 0, 1)) + 1)

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (func.lower(Bill.name) >= (fr_name).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.biltyp == 0)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

                b1_list = query(b1_list_list, first=True)

                if not b1_list:

                    bill_obj_list = []
                    for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                            (Bill.zinr > "") &  (Bill.flag == bil_int) &  (func.lower(Bill.name) >= (fr_name).lower()) &  (Bill.biltyp == 0)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()

            else:

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (Bill.gastnr == curr_gastnr) &  (Bill.biltyp == 0)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

        elif sorttype == 3:
            to_rechnr = rechnr + 1000

            bill_obj_list = []
            for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                    (Bill.zinr > "") &  (Bill.flag == bil_int) &  (Bill.rechnr == rechnr)).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                assign_it()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (Bill.rechnr >= rechnr) &  (Bill.rechnr <= to_rechnr)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        elif sorttype == 4:

            for rline in db_session.query(Rline).filter(
                    (Rline.active_flag == 1) &  (Rline.resstatus != 12) &  (Rline.abreise == ci_date) &  (Rline.l_zuordnung[2] == 0)).all():

                for bill in db_session.query(Bill).filter(
                        (Bill.resnr == rline.resnr) &  (Bill.parent_nr == rline.reslinnr) &  (Bill.flag == 0)).all():
                    assign_it()

    def disp_bill_list1():

        nonlocal b1_list_list, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, reservation, history
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff, usr


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff, usr
        nonlocal b1_list_list

        to_rechnr:int = 0
        fr_name:str = ""
        to_name:str = ""
        rmno:str = ""

        if sorttype == 1:

            if zinr != "":

                if bil_int == 0:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 1) &  (func.lower(Res_line.zinr.lower()) == (zinr).lower()) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():

                        for bill in db_session.query(Bill).filter(
                                (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            bl_saldo = 0

                            for bill_line in db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == bill.rechnr)).all():
                                bl_saldo = bl_saldo + bill_line.betrag

                            if bill.zinr != res_line.zinr:

                                bbuff = db_session.query(Bbuff).filter(
                                        (Bbuff._recid == bill._recid)).first()
                                bbuff.zinr = res_line.zinr

                                bbuff = db_session.query(Bbuff).first()


                            if bl_saldo != bill.saldo:

                                bbuff = db_session.query(Bbuff).filter(
                                        (Bbuff._recid == bill._recid)).first()
                                bbuff.saldo = bl_saldo

                                bbuff = db_session.query(Bbuff).first()

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (func.lower(Bill.zinr.lower()) == (zinr).lower()) &  (Bill.flag == bil_int) &  (Bill.rechnr != 0)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

        elif sorttype == 2:

            if curr_gastnr == 0:

                if gastname == "":
                    gastname = "a"

                if gastname.lower()  == "*":
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr(ord(substring(gastname, 0, 1)) + 1)

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (func.lower(Bill.name) >= (gastname).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.biltyp == 0) &  (Bill.rechnr != 0)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

                b1_list = query(b1_list_list, first=True)

                if not b1_list:

                    bill_obj_list = []
                    for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                            (Bill.zinr > "") &  (Bill.flag == bil_int) &  (func.lower(Bill.name) >= (gastname).lower()) &  (Bill.biltyp == 0) &  (Bill.rechnr != 0)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()

            else:

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.abreise == ci_date)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (Bill.gastnr == curr_gastnr) &  (Bill.biltyp == 0) &  (Bill.rechnr != 0)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

        elif sorttype == 3:

            if rechnr != 0:

                bill_obj_list = []
                for bill, rline in db_session.query(Bill, Rline).join(Rline,(Rline.resnr == Bill.resnr) &  (Rline.reslinnr == Bill.parent_nr) &  (Rline.active_flag == actflag)).filter(
                        (Bill.zinr > "") &  (Bill.flag == bil_int) &  (Bill.rechnr == rechnr)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()

        elif sorttype == 4:

            for rline in db_session.query(Rline).filter(
                    (Rline.active_flag == 2) &  (Rline.resstatus == 8) &  (Rline.abreise == ci_date) &  (Rline.l_zuordnung[2] == 0)).all():

                for bill in db_session.query(Bill).filter(
                        (Bill.resnr == rline.resnr) &  (Bill.parent_nr == rline.reslinnr) &  (Bill.flag == 1)).all():
                    assign_it()

    def assign_it():

        nonlocal b1_list_list, actflag, bl_saldo, lvcarea, res_line, guest, bill, bill_line, bediener, reservation, history
        nonlocal resline, rline, guestmember, mbill, bbuff, tbuff, usr


        nonlocal b1_list, resline, rline, guestmember, mbill, bbuff, tbuff, usr
        nonlocal b1_list_list


        Usr = Bediener
        bl_saldo = 0

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr)).all():
            bl_saldo = bl_saldo + bill_line.betrag

        if bl_saldo != bill.saldo:

            tbuff = db_session.query(Tbuff).filter(
                    (Tbuff._recid == bill._recid)).first()
            tbuff.saldo = bl_saldo

            tbuff = db_session.query(Tbuff).first()

        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.zinr = bill.zinr
        b1_list.billnr = bill.billnr
        b1_list.rechnr = bill.rechnr
        b1_list.name = bill.name
        b1_list.saldo = bill.saldo
        b1_list.resnr = bill.resnr
        b1_list.reslinnr = bill.reslinnr
        b1_list.datum = bill.datum
        b1_list.printnr = bill.printnr
        b1_list.vesrcod = bill.vesrcod
        b1_list.rec_id = bill._recid

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == bill.resnr) &  (Mbill.reslinnr == 0)).first()

        if mbill:
            b1_list.fg_col = True

        usr = db_session.query(Usr).filter(
                (Usr.userinit == bill.vesrcod)).first()

        if usr:
            b1_list.b_comments = translateExtended ("C/O by:", lvcarea, "") + " " + usr.username + chr (10)

        if bill:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == bill.resnr)).first()

            if reservation:

                resline = db_session.query(Resline).filter(
                        (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.parent_nr)).first()
              
                if resline:

                    guestmember = db_session.query(Guestmember).filter(
                            (Guestmember.gastnr == resline.gastnrmember)).first()

                    b1_list.resname = guestmember.name + ", " + guestmember.vorname1 + " " + guestmember.anrede1
                    b1_list.address = guestmember.adresse1
                    b1_list.city = guestmember.wohnort + " " + guestmember.plz
                    b1_list.b_comments = b1_list.b_comments + translateExtended ("Departure:", lvcarea, "") + " " + to_string(resline.abreise) + chr (10)

                    if guestmember.bemerkung != "":
                        b1_list.b_comments = b1_list.b_comments + guestmember.bemerkung + chr (10)

                    if reservation.bemerk != "":
                        b1_list.b_comments = b1_list.b_comments + reservation.bemerk + chr (10)

                    if resline.bemerk != "":
                        b1_list.b_comments = b1_list.b_comments + resline.bemerk
            else:

                if bill.flag == 1:

                    history = db_session.query(History).filter(
                            (History.resnr == bill.resnr) &  (History.reslinnr == bill.parent_nr) &  (History.zi_wechsel == False)).first()

                    if history:

                        guestmember = db_session.query(Guestmember).filter(
                                (Guestmember.gastnr == history.gastnr)).first()
                        b1_list.resname = guestmember.name + ", " + guestmember.vorname1 + " " + guestmember.anrede1
                        b1_list.address = guestmember.adresse1
                        b1_list.city = guestmember.wohnort + " " + guestmember.plz
                        b1_list.b_comments = b1_list.b_comments + translateExtended ("Departure:", lvcarea, "") + " " + to_string(history.abreise) + chr (10)
                        b1_list.b_comments = b1_list.b_comments + history.bemerk


    actflag = bil_int + 1

    if bil_int == 0:
        disp_bill_list0()
    else:
        disp_bill_list1()

    return generate_output()