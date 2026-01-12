#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from sqlalchemy import func
from decimal import Decimal
from datetime import date
from models import Guest, Res_line, Bill, History, Reservation

def bil_select2bl(case_type:int, resnr:int, bil_flag:int, master_flag:bool, sorttype:int, gastname:string, curr_gastnr:int, bill_type:int, ci_date:date):

    prepare_cache ([Guest, Res_line, Bill, History, Reservation])

    resname = ""
    address = ""
    city = ""
    comments = ""
    b1_list_data = []
    b2_list_data = []
    guest = res_line = bill = history = reservation = None

    guest1 = b1_list = b2_list = None

    b1_list_data, B1_list = create_model("B1_list", {"rechnr":int, "name":string, "vorname1":string, "anrede1":string, "adresse1":string, "saldo":Decimal, "groupname":string, "resnr":int, "printnr":int, "zinr":string, "datum":date, "wohnort":string, "plz":string, "bemerk":string, "rec_id":int})
    b2_list_data, B2_list = create_model("B2_list", {"gastnr":int, "rechnr":int, "name":string, "saldo":Decimal, "groupname":string, "resnr":int, "printnr":int, "zinr":string, "datum":date})

    Guest1 = create_buffer("Guest1",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, address, city, comments, b1_list_data, b2_list_data, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_data, b2_list_data

        return {"resname": resname, "address": address, "city": city, "comments": comments, "b1-list": b1_list_data, "b2-list": b2_list_data}
    
    def handle_string_null(input):
        if input == None:
            return ""
        return f"{input}"

    def build_blist():

        nonlocal resname, address, city, comments, b1_list_data, b2_list_data, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_data, b2_list_data

        rline = None
        Rline =  create_buffer("Rline",  Res_line)

        for bill in db_session.query(Bill).filter(
            (Bill.resnr > 0) & 
            (Bill.reslinnr == 0) & 
            (Bill.flag == bil_flag)
        ).order_by(Bill.name).yield_per(100):

            # res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"active_flag": [(le, 1)]})
            res_line = db_session.query(Res_line).filter((Res_line.resnr == bill.resnr) & (Res_line.active_flag <= 1)).first()

            if not res_line:

                # rline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"resstatus": [(eq, 8)]})
                rline = db_session.query(Rline).filter((Rline.resnr == bill.resnr) & (Rline.resstatus == 8)).first()

                if not rline:
                    # history = get_cache (History, {"resnr": [(eq, bill.resnr)],"reslinnr": [(lt, 999)],"zi_wechsel": [(eq, False)]})
                    history = db_session.query(History).filter((History.resnr == bill.resnr) & (History.reslinnr <= 999) & (History.zi_wechsel == False)).first()

                # guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
                guest = db_session.query(Guest).filter((Guest.gastnr == bill.gastnr)).first()

                # reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
                reservation = db_session.query(Reservation).filter((Reservation.resnr == bill.resnr)).first()
                b2_list = B2_list()
                b2_list_data.append(b2_list)

                b2_list.rechnr = bill.rechnr
                b2_list.name = handle_string_null(guest.name) + ", " + handle_string_null(guest.vorname1) + " " + handle_string_null(guest.anrede1)
                b2_list.saldo =  to_decimal(bill.saldo)
                b2_list.resnr = bill.resnr
                b2_list.printnr = bill.printnr
                b2_list.datum = bill.datum
                b2_list.gastnr = guest.gastnr

                if reservation:
                    b2_list.groupname = handle_string_null(reservation.groupname)

                if rline:
                    b2_list.zinr = rline.zinr

                elif history:
                    b2_list.zinr = history.zinr


    def disp_bill_list0():

        nonlocal resname, address, city, comments, b1_list_data, b2_list_data, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_data, b2_list_data

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

                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") & 
                        (Bill.flag == bil_flag) & 
                        (func.lower(Bill.name) >= (fr_name).lower()) & 
                        (func.lower(Bill.name) <= (to_name).lower()) & 
                        (Bill.resnr > 0) & 
                        (Bill.reslinnr == 0) & 
                        (Bill.billtyp == bill_type)
                    ).order_by(
                        Bill.name, 
                        Bill.rechnr.desc()
                    ).yield_per(100):
                        
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

                else:
                    to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()

                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") & 
                        (Bill.flag == bil_flag) & 
                        (func.lower(Bill.name) >= (gastname).lower()) & 
                        (func.lower(Bill.name) <= (to_name).lower()) & 
                        (Bill.resnr > 0) & 
                        (Bill.reslinnr == 0) & 
                        (Bill.billtyp == bill_type)
                    ).order_by(
                        Bill.name, 
                        Bill.rechnr.desc()
                    ).yield_per(100):
                        
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (Bill.gastnr == curr_gastnr) & 
                    (Bill.resnr > 0) & 
                    (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()


        elif sorttype == 2:

            bill_obj_list = {}
            bill = Bill()
            reservation = Reservation()
            res_line = Res_line()
            guest1 = Guest()

            for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                (Bill.zinr == "") & 
                (Bill.flag == bil_flag) & 
                (Bill.rechnr == resnr) & 
                (Bill.reslinnr == 0) & 
                (Bill.billtyp == bill_type)
            ).order_by(Bill.rechnr).yield_per(100):
                
                # if bill_obj_list.get(bill._recid):
                #     continue
                # else:
                #     bill_obj_list[bill._recid] = True


                assign_it()

            b1_list = query(b1_list_data, first=True)

            if not b1_list:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (Bill.rechnr >= resnr) & 
                    (Bill.rechnr <= (resnr + 1000)) & 
                    (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(Bill.rechnr).yield_per(100):
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


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

                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") & 
                        (Bill.flag == bil_flag) & 
                        (func.lower(Bill.name) >= (gastname).lower()) & 
                        (Bill.resnr > 0) & 
                        (Bill.reslinnr == 0) & 
                        (Bill.billtyp == bill_type)
                    ).order_by(
                        Bill.name, 
                        Bill.rechnr.desc()
                    ).yield_per(100):
                        
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

                else:

                    bill_obj_list = {}
                    bill = Bill()
                    reservation = Reservation()
                    res_line = Res_line()
                    guest1 = Guest()

                    for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                        (Bill.zinr == "") & 
                        (Bill.flag == bil_flag) & 
                        (func.lower(Bill.name) >= (gastname).lower()) & 
                        (func.lower(Bill.name) <= (to_name).lower()) & 
                        (Bill.resnr > 0) & 
                        (Bill.reslinnr == 0) & 
                        (Bill.billtyp == bill_type)
                    ).order_by(
                        Bill.name, 
                        Bill.rechnr.desc()
                    ).yield_per(100):
                        
                        # if bill_obj_list.get(bill._recid):
                        #     continue
                        # else:
                        #     bill_obj_list[bill._recid] = True


                        assign_it()

            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (Bill.gastnr == curr_gastnr) & 
                    (Bill.resnr > 0) & 
                    (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()

        if guest1:
            resname = handle_string_null(guest1.name)
            address = handle_string_null(guest1.adresse1)
            city = handle_string_null(guest1.wohnort) + " " + handle_string_null(guest1.plz)
            comments = handle_string_null(guest1.bemerkung)

            # reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
            reservation = db_session.query(Reservation).filter((Reservation.resnr == bill.resnr)).first()

            if reservation and reservation.bemerk != "":
                comments = comments + chr_unicode(10) + handle_string_null(reservation.bemerk)


    def disp_bill_list1():

        nonlocal resname, address, city, comments, b1_list_data, b2_list_data, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_data, b2_list_data

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

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (func.lower(Bill.name) >= (fr_name).lower()) & 
                    (func.lower(Bill.name) <= (to_name).lower()) & 
                    (Bill.resnr > 0) & (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()
            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.flag == bil_flag) & 
                    (Bill.gastnr == curr_gastnr) & 
                    (Bill.resnr > 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):
                    
                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()


        elif sorttype == 2 and resnr != 0:

            bill_obj_list = {}
            bill = Bill()
            reservation = Reservation()
            res_line = Res_line()
            guest1 = Guest()

            for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                (Bill.zinr == "") & 
                (Bill.flag == bil_flag) & 
                (Bill.rechnr == resnr) & 
                (Bill.reslinnr == 0) & 
                (Bill.billtyp == bill_type)
            ).order_by(Bill.rechnr).yield_per(100):
                
                # if bill_obj_list.get(bill._recid):
                #     continue
                # else:
                #     bill_obj_list[bill._recid] = True


                assign_it()

        elif sorttype == 3 and gastname != "":

            if curr_gastnr == 0:
                to_name = chr_unicode(asc(substring(gastname, 0, 1)) + 1)

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (func.lower(Bill.name) >= (gastname).lower()) & 
                    (func.lower(Bill.name) <= (to_name).lower()) & 
                    (Bill.resnr > 0) & 
                    (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):

                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()
            else:

                bill_obj_list = {}
                bill = Bill()
                reservation = Reservation()
                res_line = Res_line()
                guest1 = Guest()

                for bill, reservation, res_line, guest1 in db_session.query(Bill, Reservation, Res_line, Guest1).join(Reservation,(Reservation.resnr == Bill.resnr)).join(Res_line,(Res_line.resnr == Bill.resnr) & (Res_line.abreise == ci_date)).join(Guest1,(Guest1.gastnr == Bill.gastnr)).filter(
                    (Bill.zinr == "") & 
                    (Bill.flag == bil_flag) & 
                    (Bill.gastnr == curr_gastnr) & 
                    (Bill.resnr > 0) & 
                    (Bill.reslinnr == 0) & 
                    (Bill.billtyp == bill_type)
                ).order_by(
                    Bill.name, 
                    Bill.rechnr.desc()
                ).yield_per(100):

                    # if bill_obj_list.get(bill._recid):
                    #     continue
                    # else:
                    #     bill_obj_list[bill._recid] = True


                    assign_it()


        if guest1:
            resname = handle_string_null(guest1.name)
            address = handle_string_null(guest1.adresse1)
            city = handle_string_null(guest1.wohnort) + " " + handle_string_null(guest1.plz)
            comments = handle_string_null(guest1.bemerkung)

            # reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})
            reservation = db_session.query(Reservation).filter((Reservation.resnr == bill.resnr)).first()

            if reservation and reservation.bemerk != "":
                comments = comments + chr_unicode(10) + handle_string_null(reservation.bemerk)


    def assign_it():

        nonlocal resname, address, city, comments, b1_list_data, b2_list_data, guest, res_line, bill, history, reservation
        nonlocal case_type, resnr, bil_flag, master_flag, sorttype, gastname, curr_gastnr, bill_type, ci_date
        nonlocal guest1


        nonlocal guest1, b1_list, b2_list
        nonlocal b1_list_data, b2_list_data


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.rechnr = bill.rechnr
        b1_list.name = handle_string_null(guest1.name)
        b1_list.vorname1 = handle_string_null(guest1.vorname1)
        b1_list.adresse1 = handle_string_null(guest1.adresse1)
        b1_list.anrede1 = handle_string_null(guest1.anrede1)
        b1_list.saldo =  to_decimal(bill.saldo)
        b1_list.groupname = handle_string_null(reservation.groupname)
        b1_list.resnr = bill.resnr
        b1_list.printnr = bill.printnr
        b1_list.zinr = res_line.zinr
        b1_list.datum = bill.datum
        b1_list.wohnort = handle_string_null(guest1.wohnort)
        b1_list.plz = handle_string_null(guest1.plz)
        b1_list.bemerk = handle_string_null(guest1.bemerkung)
        b1_list.rec_id = bill._recid

    if case_type == 1:

        if bil_flag == 0:
            disp_bill_list0()
        else:
            disp_bill_list1()

    elif case_type == 2:
        build_blist()

    return generate_output()