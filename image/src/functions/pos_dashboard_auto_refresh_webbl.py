from functions.additional_functions import *
import decimal
from functions.pos_dashboard_getparambl import pos_dashboard_getparambl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl
from functions.pos_dashboard_load_orderbl import pos_dashboard_load_orderbl
from functions.pos_dashboard_check_neworderbl import pos_dashboard_check_neworderbl
from models import Queasy

def pos_dashboard_auto_refresh_webbl(user_init:str, dept_no:int):
    urlws = ""
    licensenr = 0
    dynamic_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
    found_new_order = False
    ask_bill_flag = False
    t_dept_list = []
    t_queasy222_list = []
    t_list_list = []
    pick_table_list = []
    order_list_list = []
    order_item_list = []
    check_new_ordered:bool = False
    queasy = None

    t_list = pick_table = order_list = order_item = t_dept = t_queasy222 = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "tischnr":int, "bezeich":str, "normalbeleg":int, "name":str, "occupied":bool, "belegung":int, "balance":decimal, "zinr":str, "gname":str, "ask_bill":bool, "bill_print":bool, "platform":str, "allow_ctr":str, "bill_number":int, "pay_status":str})
    pick_table_list, Pick_table = create_model("Pick_table", {"dept":int, "tableno":int, "pax":int, "gname":str, "occupied":bool, "session_parameter":str, "gemail":str, "expired_session":bool, "dataqr":str, "date_time":})
    order_list_list, Order_list = create_model("Order_list", {"table_nr":int, "pax":int, "order_nr":int, "guest_name":str, "room_no":str, "order_date":str, "posted":bool, "guest_nr":int, "resnr":int, "reslinnr":int, "sessionprm":str, "billrecid":int})
    order_item_list, Order_item = create_model("Order_item", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "art_nr":int, "posted":bool})
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})
    t_queasy222_list, T_queasy222 = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, found_new_order, ask_bill_flag, t_dept_list, t_queasy222_list, t_list_list, pick_table_list, order_list_list, order_item_list, check_new_ordered, queasy


        nonlocal t_list, pick_table, order_list, order_item, t_dept, t_queasy222
        nonlocal t_list_list, pick_table_list, order_list_list, order_item_list, t_dept_list, t_queasy222_list
        return {"urlws": urlws, "licensenr": licensenr, "dynamic_qr": dynamic_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist, "found_new_order": found_new_order, "ask_bill_flag": ask_bill_flag, "t-dept": t_dept_list, "t-queasy222": t_queasy222_list, "t-list": t_list_list, "pick-table": pick_table_list, "order-list": order_list_list, "order-item": order_item_list}

    t_dept_list, t_queasy222_list, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist = get_output(pos_dashboard_getparambl(dept_no))

    t_dept = query(t_dept_list, filters=(lambda t_dept :t_dept.nr == dept_no), first=True)
    t_list_list, pick_table_list = get_output(pos_dashboard_opened_tischbl(t_dept.nr))
    order_list_list, order_item_list = get_output(pos_dashboard_load_orderbl(t_dept.nr))

    t_list = query(t_list_list, filters=(lambda t_list :t_list.ask_bill  and t_list.bill_print == False), first=True)

    if t_list:
        ask_bill_flag = True

    for order_list in query(order_list_list):
        found_new_order = get_output(pos_dashboard_check_neworderbl(order_list.sessionprm))

        if check_new_ordered :
            break
    found_new_order = check_new_ordered

    return generate_output()