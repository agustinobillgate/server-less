from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lieferant, Fa_ordheader, Fa_op, Fa_order

def fa_polist_btn_go2bl(from_date:date, to_date:date, billdate:date, stat_order:int, lnumber:int, all_supp:bool, po_number:str, cost_list:[Cost_list], w_list:[W_list], username:[Username]):
    temp_list = []
    min_statorder:int = 0
    temp_amount:decimal = 0
    l_lieferant = fa_ordheader = fa_op = fa_order = None

    cost_list = w_list = username = temp = None

    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":str, "sorting":str})
    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":str})
    username_list, Username = create_model("Username", {"order_nr":str, "create_by":str, "modify_by":str, "close_by":str, "close_date":date, "close_time":str, "last_arrival":date, "total_amount":decimal})
    temp_list, Temp = create_model("Temp", {"sorting":str, "order_date":date, "order_nr":str, "order_type":str, "bezeich":str, "firma":str, "wabkurz":str, "released_date":date, "create_by":str, "created_date":date, "printed":date, "expected_delivery":date, "modify_by":str, "modified_date":date, "close_by":str, "close_date":date, "close_time":str, "last_arrival":date, "released_flag":bool, "supplier_nr":int, "activeflag":int, "order_desc":str, "order_name":str, "total_amount":decimal, "devnote_no":str, "arive_amount":decimal, "order_amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_list, min_statorder, temp_amount, l_lieferant, fa_ordheader, fa_op, fa_order


        nonlocal cost_list, w_list, username, temp
        nonlocal cost_list_list, w_list_list, username_list, temp_list
        return {"temp": temp_list}


    if stat_order == 0 and all_supp:

        fa_ordheader_obj_list = []
        for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == 0) &  (Fa_ordheader.Expected_Delivery >= billdate)).all():
            if fa_ordheader._recid in fa_ordheader_obj_list:
                continue
            else:
                fa_ordheader_obj_list.append(fa_ordheader._recid)

            if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                temp = Temp()
                temp_list.append(temp)

                temp.sorting = cost_list.sorting
                temp.Order_Date = fa_ordheader.Order_Date
                temp.Order_Nr = fa_ordheader.Order_Nr
                temp.Order_Type = fa_ordheader.Order_Type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.Released_Date = fa_ordheader.Released_Date
                temp.create_by = username.create_by
                temp.Created_Date = fa_ordheader.Created_Date
                temp.printed = fa_ordheader.printed
                temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.Released_Flag = fa_ordheader.Released_Flag
                temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                temp.ActiveFlag = fa_ordheader.ActiveFlag
                temp.Order_Desc = fa_ordheader.Order_Desc
                temp.Order_Name = fa_ordheader.Order_Name
                temp.total_amount = username.total_amount

                fa_op = db_session.query(Fa_op).filter(
                        (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 0 and not all_supp:

        fa_ordheader_obj_list = []
        for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == 0) &  (Fa_ordheader.supplier_nr == lnumber) &  (Fa_ordheader.Expected_Delivery >= billdate)).all():
            if fa_ordheader._recid in fa_ordheader_obj_list:
                continue
            else:
                fa_ordheader_obj_list.append(fa_ordheader._recid)

            if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                temp = Temp()
                temp_list.append(temp)

                temp.sorting = cost_list.sorting
                temp.Order_Date = fa_ordheader.Order_Date
                temp.Order_Nr = fa_ordheader.Order_Nr
                temp.Order_Type = fa_ordheader.Order_Type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.Released_Date = fa_ordheader.Released_Date
                temp.create_by = username.create_by
                temp.Created_Date = fa_ordheader.Created_Date
                temp.printed = fa_ordheader.printed
                temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.Released_Flag = fa_ordheader.Released_Flag
                temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                temp.ActiveFlag = fa_ordheader.ActiveFlag
                temp.Order_Desc = fa_ordheader.Order_Desc
                temp.Order_Name = fa_ordheader.Order_Name
                temp.total_amount = username.total_amount

                fa_op = db_session.query(Fa_op).filter(
                        (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 2 and all_supp:

        fa_ordheader_obj_list = []
        for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == 0) &  (Fa_ordheader.Expected_Delivery < billdate)).all():
            if fa_ordheader._recid in fa_ordheader_obj_list:
                continue
            else:
                fa_ordheader_obj_list.append(fa_ordheader._recid)

            if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                temp = Temp()
                temp_list.append(temp)

                temp.sorting = cost_list.sorting
                temp.Order_Date = fa_ordheader.Order_Date
                temp.Order_Nr = fa_ordheader.Order_Nr
                temp.Order_Type = fa_ordheader.Order_Type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.Released_Date = fa_ordheader.Released_Date
                temp.create_by = username.create_by
                temp.Created_Date = fa_ordheader.Created_Date
                temp.printed = fa_ordheader.printed
                temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.Released_Flag = fa_ordheader.Released_Flag
                temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                temp.ActiveFlag = fa_ordheader.ActiveFlag
                temp.Order_Desc = fa_ordheader.Order_Desc
                temp.Order_Name = fa_ordheader.Order_Name
                temp.total_amount = username.total_amount

                fa_op = db_session.query(Fa_op).filter(
                        (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 2 and not all_supp:

        fa_ordheader_obj_list = []
        for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == 0) &  (Fa_ordheader.supplier_nr == lnumber) &  (Fa_ordheader.Expected_Delivery < billdate)).all():
            if fa_ordheader._recid in fa_ordheader_obj_list:
                continue
            else:
                fa_ordheader_obj_list.append(fa_ordheader._recid)

            if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                temp = Temp()
                temp_list.append(temp)

                temp.sorting = cost_list.sorting
                temp.Order_Date = fa_ordheader.Order_Date
                temp.Order_Nr = fa_ordheader.Order_Nr
                temp.Order_Type = fa_ordheader.Order_Type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.Released_Date = fa_ordheader.Released_Date
                temp.create_by = username.create_by
                temp.Created_Date = fa_ordheader.Created_Date
                temp.printed = fa_ordheader.printed
                temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.Released_Flag = fa_ordheader.Released_Flag
                temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                temp.ActiveFlag = fa_ordheader.ActiveFlag
                temp.Order_Desc = fa_ordheader.Order_Desc
                temp.Order_Name = fa_ordheader.Order_Name
                temp.total_amount = username.total_amount

                fa_op = db_session.query(Fa_op).filter(
                        (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr

    else:

        if stat_order == 1:
            min_statorder = 1

        if stat_order == 3:
            min_statorder = 2

        if all_supp:

            fa_ordheader_obj_list = []
            for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                    (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == min_statorder)).all():
                if fa_ordheader._recid in fa_ordheader_obj_list:
                    continue
                else:
                    fa_ordheader_obj_list.append(fa_ordheader._recid)

                if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                    temp = Temp()
                    temp_list.append(temp)

                    temp.sorting = cost_list.sorting
                    temp.Order_Date = fa_ordheader.Order_Date
                    temp.Order_Nr = fa_ordheader.Order_Nr
                    temp.Order_Type = fa_ordheader.Order_Type
                    temp.bezeich = cost_list.bezeich
                    temp.firma = l_lieferant.firma
                    temp.wabkurz = w_list.wabkurz
                    temp.Released_Date = fa_ordheader.Released_Date
                    temp.create_by = username.create_by
                    temp.Created_Date = fa_ordheader.Created_Date
                    temp.printed = fa_ordheader.printed
                    temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                    temp.modify_by = username.modify_by
                    temp.modified_date = fa_ordheader.modified_date
                    temp.close_by = username.close_by
                    temp.close_date = username.close_date
                    temp.close_time = username.close_time
                    temp.last_arrival = username.last_arrival
                    temp.Released_Flag = fa_ordheader.Released_Flag
                    temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                    temp.ActiveFlag = fa_ordheader.ActiveFlag
                    temp.Order_Desc = fa_ordheader.Order_Desc
                    temp.Order_Name = fa_ordheader.Order_Name
                    temp.total_amount = username.total_amount

                    fa_op = db_session.query(Fa_op).filter(
                            (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                    if fa_op:
                        temp.devnote_no = fa_op.lscheinnr

        else:

            fa_ordheader_obj_list = []
            for fa_ordheader, w_list, cost_list, l_lieferant, username in db_session.query(Fa_ordheader, W_list, Cost_list, L_lieferant, Username).join(W_list,(W_list.nr == Fa_ordheader.currency)).join(Cost_list,(Cost_list.nr == Fa_ordheader.dept_nr)).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).join(Username,(Username.order_nr == Fa_ordheader.order_nr)).filter(
                    (Fa_ordheader.order_date >= from_date) &  (Fa_ordheader.order_date <= to_date) &  (Fa_ordheader.activeflag == min_statorder) &  (Fa_ordheader.supplier_nr == lnumber)).all():
                if fa_ordheader._recid in fa_ordheader_obj_list:
                    continue
                else:
                    fa_ordheader_obj_list.append(fa_ordheader._recid)

                if (po_number == "" or fa_ordheader.order_nr.lower()  == po_number):
                    temp = Temp()
                    temp_list.append(temp)

                    temp.sorting = cost_list.sorting
                    temp.Order_Date = fa_ordheader.Order_Date
                    temp.Order_Nr = fa_ordheader.Order_Nr
                    temp.Order_Type = fa_ordheader.Order_Type
                    temp.bezeich = cost_list.bezeich
                    temp.firma = l_lieferant.firma
                    temp.wabkurz = w_list.wabkurz
                    temp.Released_Date = fa_ordheader.Released_Date
                    temp.create_by = username.create_by
                    temp.Created_Date = fa_ordheader.Created_Date
                    temp.printed = fa_ordheader.printed
                    temp.Expected_Delivery = fa_ordheader.Expected_Delivery
                    temp.modify_by = username.modify_by
                    temp.modified_date = fa_ordheader.modified_date
                    temp.close_by = username.close_by
                    temp.close_date = username.close_date
                    temp.close_time = username.close_time
                    temp.last_arrival = username.last_arrival
                    temp.Released_Flag = fa_ordheader.Released_Flag
                    temp.Supplier_Nr = fa_ordheader.Supplier_Nr
                    temp.ActiveFlag = fa_ordheader.ActiveFlag
                    temp.Order_Desc = fa_ordheader.Order_Desc
                    temp.Order_Name = fa_ordheader.Order_Name
                    temp.total_amount = username.total_amount

                    fa_op = db_session.query(Fa_op).filter(
                            (Fa_op.docu_nr == fa_ordheader.order_nr)).first()

                    if fa_op:
                        temp.devnote_no = fa_op.lscheinnr


    for temp in query(temp_list):

        for fa_op in db_session.query(Fa_op).filter(
                (Fa_op.docu_nr == temp.order_nr) &  (Fa_op.lscheinnr == temp.devnote_no)).all():
            temp_amount = temp_amount + fa_op.warenwert
        temp.arive_amount = temp_amount
        temp_amount = 0

        for fa_order in db_session.query(Fa_order).filter(
                (Fa_order.order_nr == temp.order_nr)).all():
            temp_amount = temp_amount + fa_order.order_amount
        temp.order_amount = temp_amount
        temp_amount = 0

    return generate_output()