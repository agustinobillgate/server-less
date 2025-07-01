#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line, Bill, History, Reservation

def bil_select2bl(case_type:int, resnr:int, bil_flag:int, master_flag:bool, sorttype:int, gastname:string, curr_gastnr:int, bill_type:int, ci_date:date):

    prepare_cache ([Guest, Res_line, Bill, History, Reservation])

    resname = ""
    address = ""
    city = ""
    comments = ""
    b1_list_list = []
    b2_list_list = []
    guest = res_line = bill = history = reservation = None

    guest1 = b1_list = b2_list = None

    b1_list_list, B1_list = create_model("B1_list", {"rechnr":int, "name":string, "vorname1":string, "anrede1":string, "adresse1":string, "saldo":Decimal, "groupname":string, "resnr":int, "printnr":int, "zinr":string, "datum":date, "wohnort":string, "plz":string, "bemerk":string, "rec_id":int})
    b2_list_list, B2_list = create_model("B2_list", {"gastnr":int, "rechnr":int, "name":string, "saldo":Decimal, "groupname":string, "resnr":int, "printnr":int, "zinr":string, "datum":date})

    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_list, b2_list_list

        return {"resname": resname, "address": address, "city": city, "comments": comments, "b1-list": b1_list_list, "b2-list": b2_list_list}

    def build_blist():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_list, b2_list_list

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.flag == bil_flag)).order_by(Bill.name).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"active_flag": [(le, 1)]})

            if not res_line:

                rline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})

                if not rline:

                    history = get_cache (History, {"resnr": [(eq, bill.resnr)],"reslinnr": [(lt, 999)],"zi_wechsel": [(eq, False)]})

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
                b2_list = B2_list()
                b2_list_list.append(b2_list)

                b2_list.rechnr = bill.rechnr
                b2_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                b2_list.saldo =  to_decimal(bill.saldo)
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
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_list, b2_list_list

        fr_name:string = " "
        to_name:string = ""

        if master_flag:

            return

        if sorttype == 1 and gastname != "":

            if curr_gastnr == 0:

                if gastname.lower()  == ("*").lower() :
                    to_name = "zz"

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()
                    for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                             (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (fr_name).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                        if bill_obj_list.get(bill._recid):
                            continue
                        else:
                            bill_obj_list[bill._recid] = True


                        assign_it()
                else:
                    to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()
                    for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                             (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (gastname).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                        if bill_obj_list.get(bill._recid):
                            continue
                        else:
                            bill_obj_list[bill._recid] = True


                        assign_it()
            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.gastnr == curr_gastnr) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()


        elif sorttype == 2:

            bill_obj_list = {}
            bill = Bill()
            reservation = Reservation()
            res_line = Res_line()
            guest1 = Guest()
            for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.rechnr == resnr) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.rechnr).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                assign_it()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.rechnr >= resnr) & (Bill.rechnr <= (resnr + 1000)) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.rechnr).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()


        elif sorttype == 3:

            if curr_gastnr == 0:
                to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                if gastname == "":

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()
                    for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                             (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (gastname).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                        if bill_obj_list.get(bill._recid):
                            continue
                        else:
                            bill_obj_list[bill._recid] = True


                        assign_it()

                else:

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()
                    for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                             (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (gastname).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                        if bill_obj_list.get(bill._recid):
                            continue
                        else:
                            bill_obj_list[bill._recid] = True


                        assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.gastnr == curr_gastnr) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()


        if guest1:
            resname = guest1.name
            address = guest1.adresse1
            city = guest1.wohnort + " " + guest1.plz
            comments = guest1.bemerkung

            reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

            if reservation and reservation.bemerk != "":
                comments = comments + chr_unicode(10) + reservation.bemerk


    def disp_bill_list1():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_list, b2_list_list

        fr_name:string = " "
        to_name:string = ""

        if master_flag:

            return

        if sorttype == 1 and gastname != "":

            if curr_gastnr == 0:

                if gastname.lower()  == ("*").lower() :
                    to_name = "zz"
                else:
                    fr_name = gastname
                    to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (fr_name).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()
            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.flag == bil_flag) & (Bill.gastnr == curr_gastnr) & (Bill.resnr > 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()


        elif sorttype == 2 and resnr != 0:

            bill_obj_list = {}
            bill = Bill()
            reservation = Reservation()
            res_line = Res_line()
            guest1 = Guest()
            for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.rechnr == resnr) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.rechnr).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                assign_it()

        elif sorttype == 3 and gastname != "":

            if curr_gastnr == 0:
                to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.name >= (gastname).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()
            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()
                for bill.resnr, bill.gastnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, reservation.groupname, reservation.bemerk, reservation._recid, res_line.zinr, res_line._recid, guest1.name, guest1.vorname1, guest1.anrede1, guest1.gastnr, guest1._recid, guest1.adresse1, guest1.wohnort, guest1.plz, guest1.bemerkung in db_session.query(Bill.resnr, Bill.gastnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Reservation.groupname, Reservation.bemerk, Reservation._recid, Res_line.zinr, Res_line._recid, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.gastnr, Guest1._recid, Guest1.adresse1, Guest1.wohnort, Guest1.plz, Guest1.bemerkung).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.zinr == "") & (Bill.flag == bil_flag) & (Bill.gastnr == curr_gastnr) & (Bill.resnr > 0) & (Bill.reslinnr == 0) & (Bill.billtyp == bill_type)).order_by(Bill.name, Bill.rechnr.desc()).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


                    assign_it()


        if guest1:
            resname = guest1.name
            address = guest1.adresse1
            city = guest1.wohnort + " " + guest1.plz
            comments = guest1.bemerkung

            reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

            if reservation and reservation.bemerk != "":
                comments = comments + chr_unicode(10) + reservation.bemerk


    def assign_it():

        nonlocal resname, address, city, comments, b1_list_list, b2_list_list, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_list, b2_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.rechnr = bill.rechnr
        b1_list.name = guest1.name
        b1_list.vorname1 = guest1.vorname1
        b1_list.adresse1 = guest1.adresse1
        b1_list.anrede1 = guest1.anrede1
        b1_list.saldo =  to_decimal(bill.saldo)
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