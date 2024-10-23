from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Bill

def bil_select1bl(bil_flag:int, sorttype:int, gastname:str, dept:int, ba_dept:int, rechnr:int):
    b1_list_list = []
    fr_name:str = ""
    to_name:str = ""
    guest = bill = None

    b1_list = guest1 = None

    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "rechnr":int, "name":str, "vorname1":str, "anrede1":str, "saldo":decimal, "printnr":int, "datum":date, "b_recid":int, "adresse1":str, "wohnort":str, "bemerk":str, "plz":str})

    Guest1 = create_buffer("Guest1",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, fr_name, to_name, guest, bill
        nonlocal bil_flag, sorttype, gastname, dept, ba_dept, rechnr
        nonlocal guest1


        nonlocal b1_list, guest1
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def disp_bill_list0():

        nonlocal b1_list_list, fr_name, to_name, guest, bill
        nonlocal bil_flag, sorttype, gastname, dept, ba_dept, rechnr
        nonlocal guest1


        nonlocal b1_list, guest1
        nonlocal b1_list_list

        if sorttype == 1 and gastname == "":

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.rechnr.desc()).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

        elif sorttype == 1 and gastname != "":

            if gastname.lower()  == ("*").lower() :
                to_name = "zz"
            else:
                fr_name = gastname
                to_name = chr (asc(substring(gastname, 0, 1)) + 1)

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (func.lower(Bill.name) >= (fr_name).lower()) & (func.lower(Bill.name) <= (to_name).lower()) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.rechnr.desc()).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

        elif sorttype == 2 and rechnr == 0:

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.rechnr >= rechnr) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

        elif sorttype == 2 and rechnr > 0:

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.rechnr == rechnr) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = []
                for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.flag == bil_flag) & (Bill.rechnr >= rechnr) & (Bill.rechnr <= (rechnr + 1000)) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    cr_table()

    def disp_bill_list1():

        nonlocal b1_list_list, fr_name, to_name, guest, bill
        nonlocal bil_flag, sorttype, gastname, dept, ba_dept, rechnr
        nonlocal guest1


        nonlocal b1_list, guest1
        nonlocal b1_list_list

        if sorttype == 1 and gastname != "":

            if gastname.lower()  == ("*").lower() :
                to_name = "zz"
            else:
                fr_name = gastname
                to_name = chr (asc(substring(gastname, 0, 1)) + 1)

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (func.lower(Bill.name) >= (fr_name).lower()) & (func.lower(Bill.name) <= (to_name).lower()) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.rechnr.desc()).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

        elif sorttype == 2 and rechnr > 0:

            bill_obj_list = []
            for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.rechnr == rechnr) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                if bill._recid in bill_obj_list:
                    continue
                else:
                    bill_obj_list.append(bill._recid)


                cr_table()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = []
                for bill, guest1 in db_session.query(Bill, Guest1).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.flag == bil_flag) & (Bill.rechnr >= rechnr) & (Bill.rechnr <= (rechnr + 100)) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                    if bill._recid in bill_obj_list:
                        continue
                    else:
                        bill_obj_list.append(bill._recid)


                    cr_table()

    def cr_table():

        nonlocal b1_list_list, fr_name, to_name, guest, bill
        nonlocal bil_flag, sorttype, gastname, dept, ba_dept, rechnr
        nonlocal guest1


        nonlocal b1_list, guest1
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.resnr = bill.resnr
        b1_list.rechnr = bill.rechnr
        b1_list.name = guest1.name
        b1_list.vorname1 = guest1.vorname1
        b1_list.anrede1 = guest1.anrede1
        b1_list.saldo =  to_decimal(bill.saldo)
        b1_list.printnr = bill.printnr
        b1_list.datum = bill.datum
        b1_list.b_recid = bill._recid
        b1_list.adresse1 = guest1.adresse1
        b1_list.wohnort = guest1.wohnort
        b1_list.bemerk = guest1.bemerk
        b1_list.plz = guest1.plz

    b1_list_list.clear()

    if bil_flag == 0:
        disp_bill_list0()
    else:
        disp_bill_list1()

    return generate_output()