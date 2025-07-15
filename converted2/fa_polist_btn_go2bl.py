#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Fa_ordheader, Fa_op, Fa_order

cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string, "sorting":string})
w_list_data, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
username_data, Username = create_model("Username", {"order_nr":string, "create_by":string, "modify_by":string, "close_by":string, "close_date":date, "close_time":string, "last_arrival":date, "total_amount":Decimal})

def fa_polist_btn_go2bl(from_date:date, to_date:date, billdate:date, stat_order:int, lnumber:int, all_supp:bool, po_number:string, cost_list_data:[Cost_list], w_list_data:[W_list], username_data:[Username]):

    prepare_cache ([L_lieferant, Fa_ordheader, Fa_op, Fa_order])

    temp_data = []
    min_statorder:int = 0
    temp_amount:Decimal = to_decimal("0.0")
    l_lieferant = fa_ordheader = fa_op = fa_order = None

    cost_list = w_list = username = temp = None

    temp_data, Temp = create_model("Temp", {"sorting":string, "order_date":date, "order_nr":string, "order_type":string, "bezeich":string, "firma":string, "wabkurz":string, "released_date":date, "create_by":string, "created_date":date, "printed":date, "expected_delivery":date, "modify_by":string, "modified_date":date, "close_by":string, "close_date":date, "close_time":string, "last_arrival":date, "released_flag":bool, "supplier_nr":int, "activeflag":int, "order_desc":string, "order_name":string, "total_amount":Decimal, "devnote_no":string, "arive_amount":Decimal, "order_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_data, min_statorder, temp_amount, l_lieferant, fa_ordheader, fa_op, fa_order
        nonlocal from_date, to_date, billdate, stat_order, lnumber, all_supp, po_number


        nonlocal cost_list, w_list, username, temp
        nonlocal temp_data

        return {"temp": temp_data}


    if stat_order == 0 and all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.expected_delivery >= billdate)).order_by(Fa_ordheader._recid).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
            if not w_list:
                continue

            cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
            if not cost_list:
                continue

            username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
            if not username:
                continue

            if fa_ordheader_obj_list.get(fa_ordheader._recid):
                continue
            else:
                fa_ordheader_obj_list[fa_ordheader._recid] = True

            if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                temp = Temp()
                temp_data.append(temp)

                temp.sorting = cost_list.sorting
                temp.order_date = fa_ordheader.order_date
                temp.order_nr = fa_ordheader.order_nr
                temp.order_type = fa_ordheader.order_type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.released_date = fa_ordheader.released_date
                temp.create_by = username.create_by
                temp.created_date = fa_ordheader.created_date
                temp.printed = fa_ordheader.printed
                temp.expected_delivery = fa_ordheader.expected_delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.released_flag = fa_ordheader.released_flag
                temp.supplier_nr = fa_ordheader.supplier_nr
                temp.activeflag = fa_ordheader.activeflag
                temp.order_desc = fa_ordheader.order_desc
                temp.order_name = fa_ordheader.order_name
                temp.total_amount =  to_decimal(username.total_amount)

                fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 0 and not all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.supplier_nr == lnumber) & (Fa_ordheader.expected_delivery >= billdate)).order_by(Fa_ordheader._recid).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
            if not w_list:
                continue

            cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
            if not cost_list:
                continue

            username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
            if not username:
                continue

            if fa_ordheader_obj_list.get(fa_ordheader._recid):
                continue
            else:
                fa_ordheader_obj_list[fa_ordheader._recid] = True

            if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                temp = Temp()
                temp_data.append(temp)

                temp.sorting = cost_list.sorting
                temp.order_date = fa_ordheader.order_date
                temp.order_nr = fa_ordheader.order_nr
                temp.order_type = fa_ordheader.order_type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.released_date = fa_ordheader.released_date
                temp.create_by = username.create_by
                temp.created_date = fa_ordheader.created_date
                temp.printed = fa_ordheader.printed
                temp.expected_delivery = fa_ordheader.expected_delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.released_flag = fa_ordheader.released_flag
                temp.supplier_nr = fa_ordheader.supplier_nr
                temp.activeflag = fa_ordheader.activeflag
                temp.order_desc = fa_ordheader.order_desc
                temp.order_name = fa_ordheader.order_name
                temp.total_amount =  to_decimal(username.total_amount)

                fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 2 and all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.expected_delivery < billdate)).order_by(Fa_ordheader._recid).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
            if not w_list:
                continue

            cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
            if not cost_list:
                continue

            username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
            if not username:
                continue

            if fa_ordheader_obj_list.get(fa_ordheader._recid):
                continue
            else:
                fa_ordheader_obj_list[fa_ordheader._recid] = True

            if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                temp = Temp()
                temp_data.append(temp)

                temp.sorting = cost_list.sorting
                temp.order_date = fa_ordheader.order_date
                temp.order_nr = fa_ordheader.order_nr
                temp.order_type = fa_ordheader.order_type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.released_date = fa_ordheader.released_date
                temp.create_by = username.create_by
                temp.created_date = fa_ordheader.created_date
                temp.printed = fa_ordheader.printed
                temp.expected_delivery = fa_ordheader.expected_delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.released_flag = fa_ordheader.released_flag
                temp.supplier_nr = fa_ordheader.supplier_nr
                temp.activeflag = fa_ordheader.activeflag
                temp.order_desc = fa_ordheader.order_desc
                temp.order_name = fa_ordheader.order_name
                temp.total_amount =  to_decimal(username.total_amount)

                fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr


    elif stat_order == 2 and not all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.supplier_nr == lnumber) & (Fa_ordheader.expected_delivery < billdate)).order_by(Fa_ordheader._recid).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
            if not w_list:
                continue

            cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
            if not cost_list:
                continue

            username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
            if not username:
                continue

            if fa_ordheader_obj_list.get(fa_ordheader._recid):
                continue
            else:
                fa_ordheader_obj_list[fa_ordheader._recid] = True

            if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                temp = Temp()
                temp_data.append(temp)

                temp.sorting = cost_list.sorting
                temp.order_date = fa_ordheader.order_date
                temp.order_nr = fa_ordheader.order_nr
                temp.order_type = fa_ordheader.order_type
                temp.bezeich = cost_list.bezeich
                temp.firma = l_lieferant.firma
                temp.wabkurz = w_list.wabkurz
                temp.released_date = fa_ordheader.released_date
                temp.create_by = username.create_by
                temp.created_date = fa_ordheader.created_date
                temp.printed = fa_ordheader.printed
                temp.expected_delivery = fa_ordheader.expected_delivery
                temp.modify_by = username.modify_by
                temp.modified_date = fa_ordheader.modified_date
                temp.close_by = username.close_by
                temp.close_date = username.close_date
                temp.close_time = username.close_time
                temp.last_arrival = username.last_arrival
                temp.released_flag = fa_ordheader.released_flag
                temp.supplier_nr = fa_ordheader.supplier_nr
                temp.activeflag = fa_ordheader.activeflag
                temp.order_desc = fa_ordheader.order_desc
                temp.order_name = fa_ordheader.order_name
                temp.total_amount =  to_decimal(username.total_amount)

                fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                if fa_op:
                    temp.devnote_no = fa_op.lscheinnr

    else:

        if stat_order == 1:
            min_statorder = 1

        if stat_order == 3:
            min_statorder = 2

        if all_supp:

            fa_ordheader_obj_list = {}
            for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                     (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == min_statorder)).order_by(Fa_ordheader._recid).all():
                w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
                if not w_list:
                    continue

                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
                if not cost_list:
                    continue

                username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
                if not username:
                    continue

                if fa_ordheader_obj_list.get(fa_ordheader._recid):
                    continue
                else:
                    fa_ordheader_obj_list[fa_ordheader._recid] = True

                if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                    temp = Temp()
                    temp_data.append(temp)

                    temp.sorting = cost_list.sorting
                    temp.order_date = fa_ordheader.order_date
                    temp.order_nr = fa_ordheader.order_nr
                    temp.order_type = fa_ordheader.order_type
                    temp.bezeich = cost_list.bezeich
                    temp.firma = l_lieferant.firma
                    temp.wabkurz = w_list.wabkurz
                    temp.released_date = fa_ordheader.released_date
                    temp.create_by = username.create_by
                    temp.created_date = fa_ordheader.created_date
                    temp.printed = fa_ordheader.printed
                    temp.expected_delivery = fa_ordheader.expected_delivery
                    temp.modify_by = username.modify_by
                    temp.modified_date = fa_ordheader.modified_date
                    temp.close_by = username.close_by
                    temp.close_date = username.close_date
                    temp.close_time = username.close_time
                    temp.last_arrival = username.last_arrival
                    temp.released_flag = fa_ordheader.released_flag
                    temp.supplier_nr = fa_ordheader.supplier_nr
                    temp.activeflag = fa_ordheader.activeflag
                    temp.order_desc = fa_ordheader.order_desc
                    temp.order_name = fa_ordheader.order_name
                    temp.total_amount =  to_decimal(username.total_amount)

                    fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                    if fa_op:
                        temp.devnote_no = fa_op.lscheinnr

        else:

            fa_ordheader_obj_list = {}
            for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                     (Fa_ordheader.order_date >= from_date) & (Fa_ordheader.order_date <= to_date) & (Fa_ordheader.activeflag == min_statorder) & (Fa_ordheader.supplier_nr == lnumber)).order_by(Fa_ordheader._recid).all():
                w_list = query(w_list_data, (lambda w_list: w_list.nr == fa_ordheader.currency), first=True)
                if not w_list:
                    continue

                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == fa_ordheader.dept_nr), first=True)
                if not cost_list:
                    continue

                username = query(username_data, (lambda username: username.order_nr == fa_ordheader.order_nr), first=True)
                if not username:
                    continue

                if fa_ordheader_obj_list.get(fa_ordheader._recid):
                    continue
                else:
                    fa_ordheader_obj_list[fa_ordheader._recid] = True

                if ((po_number).lower() == "" or fa_ordheader.order_nr.lower()  == (po_number).lower()):
                    temp = Temp()
                    temp_data.append(temp)

                    temp.sorting = cost_list.sorting
                    temp.order_date = fa_ordheader.order_date
                    temp.order_nr = fa_ordheader.order_nr
                    temp.order_type = fa_ordheader.order_type
                    temp.bezeich = cost_list.bezeich
                    temp.firma = l_lieferant.firma
                    temp.wabkurz = w_list.wabkurz
                    temp.released_date = fa_ordheader.released_date
                    temp.create_by = username.create_by
                    temp.created_date = fa_ordheader.created_date
                    temp.printed = fa_ordheader.printed
                    temp.expected_delivery = fa_ordheader.expected_delivery
                    temp.modify_by = username.modify_by
                    temp.modified_date = fa_ordheader.modified_date
                    temp.close_by = username.close_by
                    temp.close_date = username.close_date
                    temp.close_time = username.close_time
                    temp.last_arrival = username.last_arrival
                    temp.released_flag = fa_ordheader.released_flag
                    temp.supplier_nr = fa_ordheader.supplier_nr
                    temp.activeflag = fa_ordheader.activeflag
                    temp.order_desc = fa_ordheader.order_desc
                    temp.order_name = fa_ordheader.order_name
                    temp.total_amount =  to_decimal(username.total_amount)

                    fa_op = get_cache (Fa_op, {"docu_nr": [(eq, fa_ordheader.order_nr)]})

                    if fa_op:
                        temp.devnote_no = fa_op.lscheinnr


    for temp in query(temp_data):

        for fa_op in db_session.query(Fa_op).filter(
                 (Fa_op.docu_nr == temp.order_nr) & (Fa_op.lscheinnr == temp.devnote_no)).order_by(Fa_op._recid).all():
            temp_amount =  to_decimal(temp_amount) + to_decimal(fa_op.warenwert)
        temp.arive_amount =  to_decimal(temp_amount)
        temp_amount =  to_decimal("0")

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == temp.order_nr)).order_by(Fa_order._recid).all():
            temp_amount =  to_decimal(temp_amount) + to_decimal(fa_order.order_amount)
        temp.order_amount =  to_decimal(temp_amount)
        temp_amount =  to_decimal("0")

    return generate_output()