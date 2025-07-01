#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

order_item_list, Order_item = create_model("Order_item", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})

def pos_dashboard_initialize_postorder_webbl(order_item_list:[Order_item], post_table_no:int, post_order_no:int):
    do_it = False
    od_cancel_list_list = []
    post_order_list = []
    menu_list_list = []

    order_item = post_order = od_cancel_list = menu_list = None

    post_order_list, Post_order = create_model("Post_order", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})
    od_cancel_list_list, Od_cancel_list = create_model("Od_cancel_list", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})
    menu_list_list, Menu_list = create_model("Menu_list", {"rec_id":int, "description":string, "qty":int, "price":Decimal, "special_request":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, od_cancel_list_list, post_order_list, menu_list_list
        nonlocal post_table_no, post_order_no


        nonlocal order_item, post_order, od_cancel_list, menu_list
        nonlocal post_order_list, od_cancel_list_list, menu_list_list

        return {"do_it": do_it, "od-cancel-list": od_cancel_list_list, "post-order": post_order_list, "menu-list": menu_list_list}

    od_cancel_list_list.clear()
    post_order_list.clear()
    menu_list_list.clear()

    for order_item in query(order_item_list, filters=(lambda order_item: order_item.table_nr == post_table_no and order_item.order_nr == post_order_no)):
        od_cancel_list = Od_cancel_list()
        od_cancel_list_list.append(od_cancel_list)

        buffer_copy(order_item, od_cancel_list)

    for order_item in query(order_item_list, filters=(lambda order_item: order_item.table_nr == post_table_no and order_item.order_nr == post_order_no)):
        post_order = Post_order()
        post_order_list.append(post_order)

        buffer_copy(order_item, post_order)

    for post_order in query(post_order_list, filters=(lambda post_order: post_order.confirm  and post_order.posted == False)):
        do_it = True
        menu_list = Menu_list()
        menu_list_list.append(menu_list)

        menu_list.rec_id = post_order.art_nr
        menu_list.description = post_order.bezeich
        menu_list.qty = post_order.qty
        menu_list.special_request = post_order.sp_req

    return generate_output()