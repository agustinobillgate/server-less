from functions.additional_functions import *
import decimal
from functions.pos_dashboard_check_waiteraccountbl import pos_dashboard_check_waiteraccountbl
from functions.pos_dashboard_getparambl import pos_dashboard_getparambl
from functions.pos_dashboard_opened_tischbl import pos_dashboard_opened_tischbl
from functions.pos_dashboard_load_orderbl import pos_dashboard_load_orderbl
from models import Queasy

def pos_dashboard_prepare_webbl(user_init:str, init_posdept:int, bedi_username:str):
    result_msg = ""
    urlws = ""
    licensenr = 0
    dynamic_qr = False
    interval_time = 0
    asroom_service = False
    cancel_exist = False
    t_dept_list = []
    t_queasy222_list = []
    t_list_list = []
    pick_table_list = []
    order_list_list = []
    order_item_list = []
    active_waiter:bool = False
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
        nonlocal result_msg, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist, t_dept_list, t_queasy222_list, t_list_list, pick_table_list, order_list_list, order_item_list, active_waiter, queasy


        nonlocal t_list, pick_table, order_list, order_item, t_dept, t_queasy222
        nonlocal t_list_list, pick_table_list, order_list_list, order_item_list, t_dept_list, t_queasy222_list
        return {"result_msg": result_msg, "urlws": urlws, "licensenr": licensenr, "dynamic_qr": dynamic_qr, "interval_time": interval_time, "asroom_service": asroom_service, "cancel_exist": cancel_exist, "t-dept": t_dept_list, "t-queasy222": t_queasy222_list, "t-list": t_list_list, "pick-table": pick_table_list, "order-list": order_list_list, "order-item": order_item_list}

    active_waiter = get_output(pos_dashboard_check_waiteraccountbl(user_init, 1, bedi_username))

    if not active_waiter:
        result_msg = "Waiter / Cashier Account not defined."

        return generate_output()
    t_dept_list, t_queasy222_list, urlws, licensenr, dynamic_qr, interval_time, asroom_service, cancel_exist = get_output(pos_dashboard_getparambl(1))

    t_dept = query(t_dept_list, filters=(lambda t_dept :t_dept.nr == 1), first=True)
    t_list_list, pick_table_list = get_output(pos_dashboard_opened_tischbl(t_dept.nr))
    order_list_list, order_item_list = get_output(pos_dashboard_load_orderbl(t_dept.nr))

    return generate_output()