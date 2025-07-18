#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 17-July-25
# add strip()
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Fa_ordheader, Fa_op, Mathis, Fa_artikel, Fa_order
"""
09/24/2024
"""
payload_list_data, Payload_list = create_model("Payload_list", {"from_date":date, "to_date":date, "billdate":date, "stat_order":int, "lnumber":int, "all_supp":bool, "po_number":string})
cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string, "sorting":string})
w_list_data, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
username_data, Username = create_model("Username", {"order_nr":string, "create_by":string, "modify_by":string, "close_by":string, "close_date":date, "close_time":string, "last_arrival":date, "total_amount":Decimal})

def fa_polist_btn_go_webbl(payload_list_data:[Payload_list], cost_list_data:[Cost_list], w_list_data:[W_list], username_data:[Username]):

    prepare_cache ([L_lieferant, Fa_ordheader, Fa_op, Mathis, Fa_artikel, Fa_order])
 
    temp_data = []
    temp_detail_data = []
    min_statorder:int = 0
    temp_amount:Decimal = to_decimal("0.0")
    tot_qty:int = 0
    tot_price:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    l_lieferant = fa_ordheader = fa_op = mathis = fa_artikel = fa_order = None

    cost_list = w_list = username = temp = temp_detail = payload_list = None

    temp_data, Temp = create_model("Temp", {"sorting":string, "Order_Date":date, "Order_Nr":string, "Order_Type":string, "bezeich":string, "firma":string, "wabkurz":string, 
                                            "Released_Date":date, "create_by":string, "Created_Date":date, "printed":date, "Expected_Delivery":date, 
                                            "modify_by":string, "modified_date":date, "close_by":string, "close_date":date, "close_time":string, "last_arrival":date, 
                                            "Released_Flag":bool, "Supplier_Nr":int, "activeflag":int, "Order_Desc":string, 
                                            "Order_Name":string, "total_amount":Decimal, "devnote_no":string, "arive_amount":Decimal, "order_amount":Decimal})
    temp_detail_data, Temp_detail = create_model("Temp_detail", {"COA":string, "desc1":string, "qty":int, "price":Decimal, "amount":Decimal, "order_number":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_data, temp_detail_data, min_statorder, temp_amount, tot_qty, tot_price, tot_amount, l_lieferant, fa_ordheader, fa_op, mathis, fa_artikel, fa_order


        nonlocal cost_list, w_list, username, temp, temp_detail, payload_list
        nonlocal temp_data, temp_detail_data

        return {"temp": temp_data, "temp-detail": temp_detail_data}


    payload_list = query(payload_list_data, first=True)

    if payload_list.stat_order == 0 and payload_list.all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.expected_delivery >= payload_list.billdate)).order_by(Fa_ordheader._recid).all():
            
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


            tot_qty = 0
            tot_price =  to_decimal("0")
            tot_amount =  to_decimal("0")
            print("Masuk create:", payload_list.po_number, ",", fa_ordheader.order_nr)
            # Rd, 17-July-25,
            # add strip()
            # if (payload_list.po_number ==  " " or fa_ordheader.order_nr == payload_list.po_number):
            if ((payload_list.po_number.strip()) ==  "" or fa_ordheader.order_nr == payload_list.po_number):
                print("Masuk creating")
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

                fa_order_obj_list = {}
                fa_order = Fa_order()
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                         (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                    if fa_order_obj_list.get(fa_order._recid):
                        continue
                    else:
                        fa_order_obj_list[fa_order._recid] = True


                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = fa_artikel.fibukonto
                    temp_detail.desc1 = mathis.name
                    temp_detail.qty = fa_order.order_qty
                    temp_detail.price =  to_decimal(fa_order.order_price)
                    temp_detail.amount =  to_decimal(fa_order.order_amount)
                    temp_detail.order_number = fa_order.order_nr
                    tot_qty = tot_qty + fa_order.order_qty


                    tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                temp_detail = Temp_detail()
                temp_detail_data.append(temp_detail)

                temp_detail.coa = ""
                temp_detail.desc1 = "T O T A L"
                temp_detail.qty = tot_qty
                temp_detail.price =  to_decimal(tot_price)
                temp_detail.amount =  to_decimal(tot_amount)
                temp_detail.order_number = fa_ordheader.order_nr

    elif payload_list.stat_order == 0 and not payload_list.all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.supplier_nr == payload_list.lnumber) & (Fa_ordheader.expected_delivery >= payload_list.billdate)).order_by(Fa_ordheader._recid).all():
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

            if (payload_list.po_number == "" or fa_ordheader.order_nr == payload_list.po_number):
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

                fa_order_obj_list = {}
                fa_order = Fa_order()
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                         (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                    if fa_order_obj_list.get(fa_order._recid):
                        continue
                    else:
                        fa_order_obj_list[fa_order._recid] = True


                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = fa_artikel.fibukonto
                    temp_detail.desc1 = mathis.name
                    temp_detail.qty = fa_order.order_qty
                    temp_detail.price =  to_decimal(fa_order.order_price)
                    temp_detail.amount =  to_decimal(fa_order.order_amount)
                    temp_detail.order_number = fa_order.order_nr
                    tot_qty = tot_qty + fa_order.order_qty


                    tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                temp_detail = Temp_detail()
                temp_detail_data.append(temp_detail)

                temp_detail.coa = ""
                temp_detail.desc1 = "T O T A L"
                temp_detail.qty = tot_qty
                temp_detail.price =  to_decimal(tot_price)
                temp_detail.amount =  to_decimal(tot_amount)
                temp_detail.order_number = fa_ordheader.order_nr


    elif payload_list.stat_order == 2 and payload_list.all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.expected_delivery < payload_list.billdate)).order_by(Fa_ordheader._recid).all():
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

            if (payload_list.po_number == "" or fa_ordheader.order_nr == payload_list.po_number):
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

                fa_order_obj_list = {}
                fa_order = Fa_order()
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                         (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                    if fa_order_obj_list.get(fa_order._recid):
                        continue
                    else:
                        fa_order_obj_list[fa_order._recid] = True


                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = fa_artikel.fibukonto
                    temp_detail.desc1 = mathis.name
                    temp_detail.qty = fa_order.order_qty
                    temp_detail.price =  to_decimal(fa_order.order_price)
                    temp_detail.amount =  to_decimal(fa_order.order_amount)
                    temp_detail.order_number = fa_order.order_nr
                    tot_qty = tot_qty + fa_order.order_qty


                    tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                temp_detail = Temp_detail()
                temp_detail_data.append(temp_detail)

                temp_detail.coa = ""
                temp_detail.desc1 = "T O T A L"
                temp_detail.qty = tot_qty
                temp_detail.price =  to_decimal(tot_price)
                temp_detail.amount =  to_decimal(tot_amount)
                temp_detail.order_number = fa_ordheader.order_nr


    elif payload_list.stat_order == 2 and not payload_list.all_supp:

        fa_ordheader_obj_list = {}
        for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                 (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == 0) & (Fa_ordheader.supplier_nr == payload_list.lnumber) & (Fa_ordheader.expected_delivery < payload_list.billdate)).order_by(Fa_ordheader._recid).all():
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

            if (payload_list.po_number == "" or fa_ordheader.order_nr == payload_list.po_number):
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

                fa_order_obj_list = {}
                fa_order = Fa_order()
                mathis = Mathis()
                fa_artikel = Fa_artikel()
                for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                         (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                    if fa_order_obj_list.get(fa_order._recid):
                        continue
                    else:
                        fa_order_obj_list[fa_order._recid] = True


                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = fa_artikel.fibukonto
                    temp_detail.desc1 = mathis.name
                    temp_detail.qty = fa_order.order_qty
                    temp_detail.price =  to_decimal(fa_order.order_price)
                    temp_detail.amount =  to_decimal(fa_order.order_amount)
                    temp_detail.order_number = fa_order.order_nr
                    tot_qty = tot_qty + fa_order.order_qty


                    tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                temp_detail = Temp_detail()
                temp_detail_data.append(temp_detail)

                temp_detail.coa = ""
                temp_detail.desc1 = "T O T A L"
                temp_detail.qty = tot_qty
                temp_detail.price =  to_decimal(tot_price)
                temp_detail.amount =  to_decimal(tot_amount)
                temp_detail.order_number = fa_ordheader.order_nr

    else:

        if payload_list.stat_order == 1:
            min_statorder = 1

        if payload_list.stat_order == 3:
            min_statorder = 2

        if payload_list.all_supp:

            fa_ordheader_obj_list = {}
            for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                     (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == min_statorder)).order_by(Fa_ordheader._recid).all():
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

                if (payload_list.po_number == "" or fa_ordheader.order_nr == payload_list.po_number):
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

                    fa_order_obj_list = {}
                    fa_order = Fa_order()
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                             (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                        if fa_order_obj_list.get(fa_order._recid):
                            continue
                        else:
                            fa_order_obj_list[fa_order._recid] = True


                        temp_detail = Temp_detail()
                        temp_detail_data.append(temp_detail)

                        temp_detail.coa = fa_artikel.fibukonto
                        temp_detail.desc1 = mathis.name
                        temp_detail.qty = fa_order.order_qty
                        temp_detail.price =  to_decimal(fa_order.order_price)
                        temp_detail.amount =  to_decimal(fa_order.order_amount)
                        temp_detail.order_number = fa_order.order_nr
                        tot_qty = tot_qty + fa_order.order_qty


                        tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = ""
                    temp_detail.desc1 = "T O T A L"
                    temp_detail.qty = tot_qty
                    temp_detail.price =  to_decimal(tot_price)
                    temp_detail.amount =  to_decimal(tot_amount)
                    temp_detail.order_number = fa_ordheader.order_nr

        else:

            fa_ordheader_obj_list = {}
            for fa_ordheader, l_lieferant in db_session.query(Fa_ordheader, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == Fa_ordheader.supplier_nr)).filter(
                     (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == min_statorder) & (Fa_ordheader.supplier_nr == payload_list.lnumber)).order_by(Fa_ordheader._recid).all():
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

                if (payload_list.po_number == "" or fa_ordheader.order_nr == payload_list.po_number):
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

                    fa_order_obj_list = {}
                    fa_order = Fa_order()
                    mathis = Mathis()
                    fa_artikel = Fa_artikel()
                    for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                             (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
                        if fa_order_obj_list.get(fa_order._recid):
                            continue
                        else:
                            fa_order_obj_list[fa_order._recid] = True


                        temp_detail = Temp_detail()
                        temp_detail_data.append(temp_detail)

                        temp_detail.coa = fa_artikel.fibukonto
                        temp_detail.desc1 = mathis.name
                        temp_detail.qty = fa_order.order_qty
                        temp_detail.price =  to_decimal(fa_order.order_price)
                        temp_detail.amount =  to_decimal(fa_order.order_amount)
                        temp_detail.order_number = fa_order.order_nr
                        tot_qty = tot_qty + fa_order.order_qty


                        tot_price =  to_decimal(tot_price) + to_decimal(fa_order.order_price)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                    temp_detail = Temp_detail()
                    temp_detail_data.append(temp_detail)

                    temp_detail.coa = ""
                    temp_detail.desc1 = "T O T A L"
                    temp_detail.qty = tot_qty
                    temp_detail.price =  to_decimal(tot_price)
                    temp_detail.amount =  to_decimal(tot_amount)
                    temp_detail.order_number = fa_ordheader.order_nr


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