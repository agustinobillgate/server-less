#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Bill

def ns_inv_attach_cashless_codebl(bil_flag:int, sorttype:int, gastname:string, dept:int, ba_dept:int, rechnr:int):

    prepare_cache ([Guest, Bill])

    b1_list_list = []
    fr_name:string = ""
    to_name:string = ""
    guest = bill = None

    b1_list = guest1 = None

    b1_list_list, B1_list = create_model("B1_list", {"resnr":int, "rechnr":int, "name":string, "vorname1":string, "anrede1":string, "saldo":Decimal, "printnr":int, "datum":date, "b_recid":int, "adresse1":string, "wohnort":string, "bemerk":string, "plz":string, "bill_datum":date, "qr_code":string})

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

            bill_obj_list = {}
            bill = Bill()
            guest1 = Guest()
            for bill.resnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, bill.vesrdepot2, guest1.name, guest1.vorname1, guest1.anrede1, guest1.adresse1, guest1.wohnort, guest1.bemerkung, guest1.plz, guest1._recid in db_session.query(Bill.resnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Bill.vesrdepot2, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.adresse1, Guest1.wohnort, Guest1.bemerkung, Guest1.plz, Guest1._recid).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.rechnr.desc()).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                cr_table()

        elif sorttype == 1 and gastname != "":

            if gastname.lower()  == ("*").lower() :
                to_name = "zz"
            else:
                fr_name = gastname
                to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

            bill_obj_list = {}
            bill = Bill()
            guest1 = Guest()
            for bill.resnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, bill.vesrdepot2, guest1.name, guest1.vorname1, guest1.anrede1, guest1.adresse1, guest1.wohnort, guest1.bemerkung, guest1.plz, guest1._recid in db_session.query(Bill.resnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Bill.vesrdepot2, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.adresse1, Guest1.wohnort, Guest1.bemerkung, Guest1.plz, Guest1._recid).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.name >= (fr_name).lower()) & (Bill.name <= (to_name).lower()) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.name, Bill.rechnr.desc()).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                cr_table()

        elif sorttype == 2 and rechnr == 0:

            bill_obj_list = {}
            bill = Bill()
            guest1 = Guest()
            for bill.resnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, bill.vesrdepot2, guest1.name, guest1.vorname1, guest1.anrede1, guest1.adresse1, guest1.wohnort, guest1.bemerkung, guest1.plz, guest1._recid in db_session.query(Bill.resnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Bill.vesrdepot2, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.adresse1, Guest1.wohnort, Guest1.bemerkung, Guest1.plz, Guest1._recid).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.rechnr >= rechnr) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                cr_table()

        elif sorttype == 2 and rechnr > 0:

            bill_obj_list = {}
            bill = Bill()
            guest1 = Guest()
            for bill.resnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, bill.vesrdepot2, guest1.name, guest1.vorname1, guest1.anrede1, guest1.adresse1, guest1.wohnort, guest1.bemerkung, guest1.plz, guest1._recid in db_session.query(Bill.resnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Bill.vesrdepot2, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.adresse1, Guest1.wohnort, Guest1.bemerkung, Guest1.plz, Guest1._recid).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                     (Bill.flag == bil_flag) & (Bill.rechnr == rechnr) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                if bill_obj_list.get(bill._recid):
                    continue
                else:
                    bill_obj_list[bill._recid] = True


                cr_table()

            b1_list = query(b1_list_list, first=True)

            if not b1_list:

                bill_obj_list = {}
                bill = Bill()
                guest1 = Guest()
                for bill.resnr, bill.rechnr, bill.saldo, bill.printnr, bill.datum, bill._recid, bill.vesrdepot2, guest1.name, guest1.vorname1, guest1.anrede1, guest1.adresse1, guest1.wohnort, guest1.bemerkung, guest1.plz, guest1._recid in db_session.query(Bill.resnr, Bill.rechnr, Bill.saldo, Bill.printnr, Bill.datum, Bill._recid, Bill.vesrdepot2, Guest1.name, Guest1.vorname1, Guest1.anrede1, Guest1.adresse1, Guest1.wohnort, Guest1.bemerkung, Guest1.plz, Guest1._recid).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                         (Bill.flag == bil_flag) & (Bill.rechnr >= rechnr) & (Bill.rechnr <= (rechnr + 1000)) & (Bill.resnr == 0) & (Bill.reslinnr == 1) & (Bill.billtyp == dept)).order_by(Bill.rechnr).all():
                    if bill_obj_list.get(bill._recid):
                        continue
                    else:
                        bill_obj_list[bill._recid] = True


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
        b1_list.qr_code = bill.vesrdepot2

    b1_list_list.clear()

    if bil_flag == 0:
        disp_bill_list0()

    return generate_output()