from functions.additional_functions import *
import decimal
from functions.pos_dashboard_cancel_reasonbl import pos_dashboard_cancel_reasonbl
from functions.pos_dashboard_cancel_orderbl import pos_dashboard_cancel_orderbl
from functions.pos_dashboard_post_menubl import pos_dashboard_post_menubl

def pos_dashboard_postorder_webbl(od_cancel_list:[Od_cancel_list], post_order:[Post_order], menu_list:[Menu_list], case_type:int, user_init:str, cancel_str:str, post_curr_dept:int, post_order_no:int, post_tischnr:int, post_session_param:str, post_language_code:int, post_bill_recid:int, post_gname:str, post_pax:int, post_guestnr:int, post_curr_room:str, post_resnr:int, post_reslinnr:int):
    post_mess_str = ""
    post_bill_number = 0

    post_order = od_cancel_list = menu_list = None

    post_order_list, Post_order = create_model("Post_order", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "art_nr":int, "posted":bool})
    od_cancel_list_list, Od_cancel_list = create_model("Od_cancel_list", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "art_nr":int, "posted":bool})
    menu_list_list, Menu_list = create_model("Menu_list", {"rec_id":int, "description":str, "qty":int, "price":decimal, "special_request":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal post_mess_str, post_bill_number


        nonlocal post_order, od_cancel_list, menu_list
        nonlocal post_order_list, od_cancel_list_list, menu_list_list
        return {"post_mess_str": post_mess_str, "post_bill_number": post_bill_number}

    if case_type == 1:
        menu_list_list.clear()
        get_output(pos_dashboard_cancel_reasonbl(od_cancel_list, user_init, cancel_str))

        for post_order in query(post_order_list, filters=(lambda post_order :post_order.confirm == False and post_order.posted == False)):
            menu_list = Menu_list()
            menu_list_list.append(menu_list)

            menu_list.rec_id = post_order.art_nr
            menu_list.DESCRIPTION = post_order.bezeich
            menu_list.qty = post_order.qty
            menu_list.special_request = post_order.sp_req


        post_mess_str = get_output(pos_dashboard_cancel_orderbl(menu_list, post_curr_dept, post_order_no, post_tischnr, post_session_param))
    else:
        get_output(pos_dashboard_cancel_reasonbl(od_cancel_list, user_init, cancel_str))
        post_bill_number, post_mess_str = get_output(pos_dashboard_post_menubl(post_language_code, post_bill_recid, post_tischnr, post_curr_dept, user_init, post_gname, post_pax, post_guestnr, post_curr_room, post_resnr, post_reslinnr, post_session_param, post_order_no, menu_list))

    return generate_output()