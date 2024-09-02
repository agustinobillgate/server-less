from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Res_line, Bill, History, Reservation

def bil_select2bl(case_type:int, resnr:int, bil_flag:int, master_flag:bool, sorttype:int, gastname:str, curr_gastnr:int, bill_type:int, ci_date:date):
    resname = ""
    address = ""
    city = ""
    comments = ""
    b1_list_list = []
    b2_list_list = []
    guest = res_line = bill = history = reservation = None

    guest1 = b1_list = b2_list = rline = None

    b1_list_list, B1_list = create_model("B1_list", {"rechnr":int, "name":str, "vorname1":str, "anrede1":str, "adresse1":str, "saldo":decimal, "groupname":str, "resnr":int, "printnr":int, "zinr":str, "datum":date, "wohnort":str, "plz":str, "bemerk":str, "rec_id":int})
    b2_list_list, B2_list = create_model("B2_list", {"gastnr":int, "rechnr":int, "name":str, "saldo":decimal, "groupname":str, "resnr":int, "printnr":int, "zinr":str, "datum":date})

    Guest1 = Guest
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal guest1, rline


        nonlocal guest1, b1_list, b2_list, rline
        nonlocal b1_list_list, b2_list_list
        return {"resname": resname, "address": address, "city": city, "comments": comments, "b1-list": b1_list_list, "b2-list": b2_list_list}

    def build_blist():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal guest1, rline


        nonlocal guest1, b1_list, b2_list, rline
        nonlocal b1_list_list, b2_list_list


        Rline = Res_line

        for bill in db_session.query(Bill).filter(
                (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.flag == bil_flag)).all():

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.active_flag <= 1)).first()

            if not res_line:

                rline = db_session.query(Rline).filter(
                        (Rline.resnr == bill.resnr) &  (Rline.resstatus == 8)).first()

                if not rline:

                    history = db_session.query(History).filter(
                            (History.resnr == bill.resnr) &  (History.reslinnr < 999) &  (History.zi_wechsel == False)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == bill.gastnr)).first()

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == bill.resnr)).first()
                b2_list = B2_list()
                b2_list_list.append(b2_list)

                b2_list.rechnr = bill.rechnr
                b2_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                b2_list.saldo = bill.saldo
                b2_list.resnr = bill.resnr
                b2_list.printnr = bill.printnr
                b2_list.datum = bill.datum
                b2_list.gastnr = guest.gastnr

                if reservation:
                    b2_list.groupname = reservation.groupname

                if rline:
                    b2_list.zinr = rline.zinr

                elif history:
                    b2_list.zinr = history.zinr

    def disp_bill_list0():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal guest1, rline


        nonlocal guest1, b1_list, b2_list, rline
        nonlocal b1_list_list, b2_list_list

        fr_name:str = " "
        to_name:str = ""

        if master_flag:

            return

        if sorttype == 1 and gastname != "":

            if curr_gastnr == 0:

                if gastname.lower()  == "*":
                    to_name = "zz"

                    bill_obj_list = []
                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                            (Bill.zinr == "") &  
                            (Bill.flag == bil_flag) &  
                            (func.lower(Bill.name) >= (fr_name).lower()) &  
                            (func.lower(Bill.name) <= (to_name).lower()) &  
                            (Bill.resnr > 0) &  
                            (Bill.reslinnr == 0) &  
                            (Bill.billtyp == bill_type)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()
                else:
                    to_name = chr (ord(substring(gastname, 0, 1)) + 1)

                    bill_obj_list = []
                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                            (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (func.lower(Bill.name) >= (gastname).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()
            else:

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.gastnr == curr_gastnr) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        elif sorttype == 2:

            bill_obj_list = []
            for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.rechnr == resnr) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                assign_it()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.rechnr >= resnr) &  (Bill.rechnr <= (resnr + 1000)) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        elif sorttype == 3:

            if curr_gastnr == 0:
                to_name = chr (ord(substring(gastname, 0, 1)) + 1)

                if gastname == "":

                    bill_obj_list = []
                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                            (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (func.lower(Bill.name) >= (gastname).lower()) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()

                else:

                    bill_obj_list = []
                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                            (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (func.lower(Bill.name) >= (gastname).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                        if bill._recid in bill_obj_list:
                            continue
                        else:
                            bill_obj_list.append(bill._recid)


                        assign_it()

            else:

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.gastnr == curr_gastnr) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        if guest1:
            resname = guest1.name
            address = guest1.adresse1
            city = guest1.wohnort + " " + guest1.plz
            comments = guest1.bemerkung

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == bill.resnr)).first()

            if reservation and reservation.bemerk != "":
                comments = comments + chr (10) + reservation.bemerk

    def disp_bill_list1():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal guest1, rline


        nonlocal guest1, b1_list, b2_list, rline
        nonlocal b1_list_list, b2_list_list

        fr_name:str = " "
        to_name:str = ""

        if master_flag:

            return

        if sorttype == 1 and gastname != "":

            if curr_gastnr == 0:

                if gastname.lower()  == "*":
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr (ord(substring(gastname, 0, 1)) + 1)

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (func.lower(Bill.name) >= (fr_name).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()
            else:

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.flag == bil_flag) &  (Bill.gastnr == curr_gastnr) &  (Bill.resnr > 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        elif sorttype == 2 and resnr != 0:

            bill_obj_list = []
            for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.rechnr == resnr) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                assign_it()

        elif sorttype == 3 and gastname != "":

            if curr_gastnr == 0:
                to_name = chr (ord(substring(gastname, 0, 1)) + 1)

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (func.lower(Bill.name) >= (gastname).lower()) &  (func.lower(Bill.name) <= (to_name).lower()) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()
            else:

                bill_obj_list = []
                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) &  (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") &  (Bill.flag == bil_flag) &  (Bill.gastnr == curr_gastnr) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0) &  (Bill.billtyp == bill_type)).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    assign_it()


        if guest1:
            resname = guest1.name
            address = guest1.adresse1
            city = guest1.wohnort + " " + guest1.plz
            comments = guest1.bemerkung

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == bill.resnr)).first()

            if reservation and reservation.bemerk != "":
                comments = comments + chr (10) + reservation.bemerk

    def assign_it():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal guest1, rline


        nonlocal guest1, b1_list, b2_list, rline
        nonlocal b1_list_list, b2_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.rechnr = bill.rechnr
        b1_list.name = guest1.name
        b1_list.vorname1 = guest1.vorname1
        b1_list.adresse1 = guest1.adresse1
        b1_list.anrede1 = guest1.anrede1
        b1_list.saldo = bill.saldo
        b1_list.groupname = reservation.groupname
        b1_list.resnr = bill.resnr
        b1_list.printnr = bill.printnr
        b1_list.zinr = res_line.zinr
        b1_list.datum = bill.datum
        b1_list.wohnort = guest1.wohnort
        b1_list.plz = guest1.plz
        b1_list.bemerk = guest1.bemerkung
        b1_list.rec_id = bill._recid


    if case_type == 1:

        if bil_flag == 0:
            disp_bill_list0()
        else:
            disp_bill_list1()

    elif case_type == 2:
        build_blist()

    return generate_output()