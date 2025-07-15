#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.pos_dashboard_cancel_reasonbl import pos_dashboard_cancel_reasonbl
from functions.pos_dashboard_cancel_orderbl import pos_dashboard_cancel_orderbl
from functions.pos_dashboard_post_menubl import pos_dashboard_post_menubl

od_cancel_list_data, Od_cancel_list = create_model("Od_cancel_list", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})
post_order_data, Post_order = create_model("Post_order", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "art_nr":int, "posted":bool})
menu_list_data, Menu_list = create_model("Menu_list", {"rec_id":int, "description":string, "qty":int, "price":Decimal, "special_request":string})

def pos_dashboard_postorder_webbl(od_cancel_list_data:[Od_cancel_list], post_order_data:[Post_order], menu_list_data:[Menu_list], case_type:int, user_init:string, cancel_str:string, post_curr_dept:int, post_order_no:int, post_tischnr:int, post_session_param:string, post_language_code:int, post_bill_recid:int, post_gname:string, post_pax:int, post_guestnr:int, post_curr_room:string, post_resnr:int, post_reslinnr:int):
    post_mess_str = ""
    post_bill_number = 0

    post_order = od_cancel_list = menu_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal post_mess_str, post_bill_number
        nonlocal case_type, user_init, cancel_str, post_curr_dept, post_order_no, post_tischnr, post_session_param, post_language_code, post_bill_recid, post_gname, post_pax, post_guestnr, post_curr_room, post_resnr, post_reslinnr


        nonlocal post_order, od_cancel_list, menu_list

        return {"post_mess_str": post_mess_str, "post_bill_number": post_bill_number}

    if cancel_str == None:
        cancel_str = ""

    if post_session_param == None:
        post_session_param = ""

    if post_gname == None:
        post_gname = ""

    if post_curr_room == None:
        post_curr_room = ""

    if case_type == 1:
        menu_list_data.clear()
        get_output(pos_dashboard_cancel_reasonbl(od_cancel_list_data, user_init, cancel_str))

        for post_order in query(post_order_data, filters=(lambda post_order: post_order.confirm == False and post_order.posted == False)):
            menu_list = Menu_list()
            menu_list_data.append(menu_list)

            menu_list.rec_id = post_order.art_nr
            menu_list.description = post_order.bezeich
            menu_list.qty = post_order.qty
            menu_list.special_request = post_order.sp_req


        post_mess_str = get_output(pos_dashboard_cancel_orderbl(menu_list_data, post_curr_dept, post_order_no, post_tischnr, post_session_param))
    else:
        get_output(pos_dashboard_cancel_reasonbl(od_cancel_list_data, user_init, cancel_str))
        post_bill_number, post_mess_str = get_output(pos_dashboard_post_menubl(post_language_code, post_bill_recid, post_tischnr, post_curr_dept, user_init, post_gname, post_pax, post_guestnr, post_curr_room, post_resnr, post_reslinnr, post_session_param, post_order_no, menu_list_data))

    return generate_output()